import random
from typing import Dict, Optional

from .attacks import intercept_resend
from .channel import noisy_channel
from .privacy import amplify
from .reconciliation import reconcile

DEFAULT_THRESHOLDS = {
    "benign_noise_max": 0.03,
    "attack_min": 0.06,
}


def bb84_protocol(
    n: int = 1000,
    attack: Optional[str] = None,
    noise_rate: float = 0.0,
    thresholds: Optional[Dict[str, float]] = None,
    seed: Optional[int] = None,
) -> Dict[str, object]:
    """
    Abstract BB84 protocol model for Q3 communication experiments.

    This is a protocol-level model. It does not simulate photons, hardware, or
    qubit-level physics.
    """
    if n <= 0:
        raise ValueError("n must be positive.")

    rng = random.Random(seed)
    thresholds = thresholds or DEFAULT_THRESHOLDS
    benign_noise_max = thresholds["benign_noise_max"]
    attack_min = thresholds["attack_min"]

    bits = [rng.choice([0, 1]) for _ in range(n)]
    bases = [rng.choice([0, 1]) for _ in range(n)]

    if attack == "intercept_resend":
        transmitted_bits, transmitted_bases = intercept_resend(bits, bases, rng=rng)
    else:
        transmitted_bits, transmitted_bases = bits, bases

    if noise_rate > 0.0:
        transmitted_bits = noisy_channel(transmitted_bits, noise_rate, rng=rng)

    bob_bases = [rng.choice([0, 1]) for _ in range(n)]

    sifted_alice = []
    sifted_bob = []
    sifted_bases = []
    for index in range(n):
        if transmitted_bases[index] == bob_bases[index]:
            sifted_alice.append(bits[index])
            sifted_bob.append(transmitted_bits[index])
            sifted_bases.append(bases[index])

    matched_bases = len(sifted_alice)
    errors = sum(1 for alice, bob in zip(sifted_alice, sifted_bob) if alice != bob)
    error_rate = errors / matched_bases if matched_bases > 0 else 0.0

    secure = error_rate <= benign_noise_max
    if error_rate <= benign_noise_max:
        threat_level = "benign_noise"
        threat_reason = "Error rate consistent with low channel noise"
    elif error_rate >= attack_min:
        threat_level = "suspected_attack"
        threat_reason = "Error rate exceeds attack suspicion threshold"
    else:
        threat_level = "unknown"
        threat_reason = "Error rate in ambiguous zone"

    reconciled_key, leakage = reconcile(sifted_alice, error_rate)
    final_key = amplify(reconciled_key, leakage)

    return {
        "raw_bits": n,
        "matched_bases": matched_bases,
        "sifted_bases": sifted_bases,
        "final_key_length": len(final_key),
        "error_rate": error_rate,
        "secure": secure,
        "threat_level": threat_level,
        "threat_reason": threat_reason,
        "seed": seed,
        "postprocessing": {
            "reconciliation_leakage": leakage,
            "post_reconciliation_length": len(reconciled_key),
            "post_amplification_length": len(final_key),
        },
    }


def qkd_decision(
    n: int = 1000,
    attack: Optional[str] = None,
    noise_rate: float = 0.0,
    thresholds: Optional[Dict[str, float]] = None,
    seed: Optional[int] = None,
) -> Dict[str, object]:
    """Legacy-friendly decision interface for protocol-level BB84 outcomes."""
    full = bb84_protocol(
        n=n,
        attack=attack,
        noise_rate=noise_rate,
        thresholds=thresholds,
        seed=seed,
    )

    return {
        "secure": full["secure"],
        "threat_level": full["threat_level"],
        "error_rate": full["error_rate"],
        "thresholds_used": thresholds or DEFAULT_THRESHOLDS,
    }

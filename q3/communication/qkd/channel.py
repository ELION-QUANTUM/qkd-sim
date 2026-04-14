import random
from typing import Iterable, List, Optional


def noisy_channel(
    bits: Iterable[int],
    noise_rate: float = 0.02,
    rng: Optional[random.Random] = None,
) -> List[int]:
    """Apply independent classical bit flips as an abstract channel-noise model."""
    if not 0.0 <= noise_rate <= 1.0:
        raise ValueError("noise_rate must be between 0 and 1.")

    generator = rng or random
    noisy_bits = []
    for bit in bits:
        if generator.random() < noise_rate:
            noisy_bits.append(1 - bit)
        else:
            noisy_bits.append(bit)
    return noisy_bits

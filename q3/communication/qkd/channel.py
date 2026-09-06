import random
from typing import Iterable, List, Optional

from .validation import probability


def noisy_channel(
    bits: Iterable[int],
    noise_rate: float = 0.02,
    rng: Optional[random.Random] = None,
) -> List[int]:
    """Apply independent classical bit flips as an abstract channel-noise model."""
    noise_rate = probability(noise_rate, "noise_rate")

    generator = rng or random
    noisy_bits = []
    for bit in bits:
        if generator.random() < noise_rate:
            noisy_bits.append(1 - bit)
        else:
            noisy_bits.append(bit)
    return noisy_bits

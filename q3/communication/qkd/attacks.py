import random
from typing import Iterable, List, Optional, Tuple


def intercept_resend(
    bits: Iterable[int],
    bases: Iterable[int],
    rng: Optional[random.Random] = None,
) -> Tuple[List[int], List[int]]:
    """Abstract intercept-resend model for protocol-level BB84 experiments."""
    generator = rng or random
    eve_bits = []
    eve_bases = []

    for bit, _basis in zip(bits, bases):
        eve_basis = generator.choice([0, 1])
        eve_bases.append(eve_basis)

        if eve_basis == 0:
            eve_bits.append(bit)
        else:
            eve_bits.append(generator.choice([0, 1]))

    return eve_bits, eve_bases

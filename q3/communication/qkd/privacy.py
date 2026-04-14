from typing import Iterable, List


def amplify(key: Iterable[int], leakage: int) -> List[int]:
    """
    Deterministic privacy-amplification estimate.

    This keeps the behavior explicit without pretending to implement a complete
    cryptographic privacy-amplification pipeline.
    """

    key_list = list(key)
    retained = max(len(key_list) - max(leakage, 0), 0)
    return key_list[:retained]

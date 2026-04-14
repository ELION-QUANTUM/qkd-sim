from typing import Iterable, List, Tuple


def reconcile(key: Iterable[int], error_rate: float) -> Tuple[List[int], int]:
    """
    Deterministic, simplified reconciliation estimate.

    This is not a production-grade error-correction implementation. It trims the
    key length by a leakage estimate proportional to the observed error rate so
    downstream simulations can reason about post-processing cost explicitly.
    """

    key_list = list(key)
    leakage = min(len(key_list), int(round(len(key_list) * error_rate)))
    reconciled = key_list[: len(key_list) - leakage]
    return reconciled, leakage

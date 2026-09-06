"""Public parameter contracts for the educational protocol model."""
import math
from collections.abc import Mapping
from numbers import Real


def probability(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite probability")
    try:
        valid = math.isfinite(value) and 0 <= value <= 1
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError(f"{name} must be a finite probability in [0, 1]")
    return float(value)


def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def threshold_copy(value, defaults):
    if value is None:
        value = defaults
    if not isinstance(value, Mapping) or set(value) != set(defaults):
        raise ValueError("thresholds must contain benign_noise_max and attack_min only")
    result = {key: probability(value[key], key) for key in defaults}
    if result['benign_noise_max'] >= result['attack_min']:
        raise ValueError("benign_noise_max must be strictly below attack_min")
    return result

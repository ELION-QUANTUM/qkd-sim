# Modeling Assumptions

This repository now contains two distinct modeling regimes:

- a mathematically grounded state-vector computation core in `q3.simulator`
- an abstract protocol-level QKD model in `q3.communication.qkd`

They should not be confused.

## Computation core assumptions

- State evolution is modeled exactly for the implemented gate set.
- The simulator is intended for small circuits only.
- Measurement is computational-basis only.
- No device noise or calibration effects are modeled.

## QKD module assumptions

- BB84 is represented at the protocol layer, not the physical layer.
- Channel noise is modeled as independent classical bit flips.
- Intercept-resend is modeled abstractly.
- Post-processing is represented through deterministic simplified estimates.

## Non-goals

This repository does not attempt to:

- reproduce laboratory QKD results
- simulate optics or hardware components
- provide production cryptographic guarantees
- claim hardware readiness

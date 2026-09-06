# Q³ Metrics

## Computation results

The state-vector backend returns:

- `statevector` — final amplitude vector before measurement collapse
- `counts` — shot counts over measured classical bitstrings
- `shots` — number of repeated measurement samples
- `memory` — per-shot measured classical strings

These outputs are suitable for small circuit validation and example-driven testing.

## QKD protocol results

The BB84 model returns:

- `raw_bits`
- `matched_bases`
- `final_key_length`
- `error_rate`
- `secure`
- `threat_level`
- `threat_reason`
- `postprocessing`

These values are protocol-level signals. They are not physical security guarantees.

## Decision interface

The legacy-friendly `qkd_decision` API intentionally stays minimal:

- `secure`
- `threat_level`
- `error_rate`
- `thresholds_used`

This is meant for higher-level decision logic, not for claiming a full cryptographic stack.

With zero basis matches, QBER (`error_rate`) is `None`, `secure` is false and
`threat_level` is `insufficient_data`. For nonempty samples, `secure` is only a
legacy QBER threshold heuristic; it is not finite-key security evidence.

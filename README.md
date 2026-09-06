# qkd-sim

`qkd-sim` now hosts the early **Q³** prototype: a Python-based experimental framework for
quantum computation, quantum communication, and system-level simulation.

The repository name is retained for continuity, but the codebase is no longer just a narrow
QKD sandbox. QKD remains in the repository as one communication module inside a broader
framework.

## What Q³ is

Q³ is an early-stage research framework with four explicit layers:

- **Language/API layer**: Python-first circuit and protocol APIs
- **Circuit layer**: typed instructions and circuit construction
- **Simulation layer**: a small state-vector backend for auditable experiments
- **Communication layer**: protocol-level QKD models built alongside the computation core

Q³ is a prototype. It is not hardware-enabled, not optimized, and not feature-complete.

## What is implemented today

- a minimal `Circuit` abstraction
- gate support for `H`, `X`, `Z`, and `CX`
- computational-basis measurement
- a small state-vector simulator for low-qubit experiments
- Bell-state and measurement examples
- an abstract BB84 protocol model under `q3.communication.qkd`
- compatibility exports for legacy `qkd` imports

## What is not implemented

- real hardware execution
- large gate libraries
- pulse control
- transpilation
- noise-aware quantum device modeling
- cryptographically complete QKD post-processing

## Repository structure

```text
q3/
  core/            # registers and gate definitions
  circuits/        # circuit abstraction
  simulator/       # state-vector backend and backend interface
  communication/   # QKD and communication-oriented modules
  compat/          # legacy qkd-sim compatibility exports

qkd/               # thin compatibility layer for existing public imports
examples/          # working examples
experiments/       # small reproducible experiment scripts
docs/              # architecture and maturity notes
tests/             # unit and integration tests
```

## Why Q³ exists

Q³ is not trying to out-market Qiskit or Cirq. The design goal is narrower and more realistic:

- keep the core small enough to audit
- combine circuit execution and communication protocols in one framework
- support hybrid classical-quantum research workflows
- expose system-level behavior without pretending unsupported hardware capability

## Primary API

```python
from q3 import Circuit, StateVectorBackend

circuit = Circuit("bell")
q = circuit.qubits(2)
m = circuit.bits(2)

circuit.h(q[0]).cx(q[0], q[1])
circuit.measure(q[0], m[0]).measure(q[1], m[1])

result = StateVectorBackend().run(circuit, shots=1024)
print(result.counts)
```

## QKD compatibility

Legacy imports continue to work:

```python
from qkd import qkd_decision
```

This path is maintained for continuity. New QKD work should use:

```python
from q3.communication.qkd import bb84_protocol, qkd_decision
```

## Quick start

Install the package and its runtime dependency (Python 3.9+):

```bash
python3 -m pip install .
```

Run the primary examples:

```bash
python3 examples/bell_state.py
python3 examples/simple_circuit.py
python3 examples/measurement_demo.py
python3 examples/bb84_protocol.py
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Documentation

- [docs/q3-overview.md](docs/q3-overview.md)
- [docs/q3-api.md](docs/q3-api.md)
- [docs/assumptions.md](docs/assumptions.md)
- [docs/metrics.md](docs/metrics.md)
- [docs/research_note.md](docs/research_note.md)
- [docs/roadmap.md](docs/roadmap.md)

## Contributing

Contribution guidance is documented in [CONTRIBUTING.md](CONTRIBUTING.md).

In short:

- keep claims aligned with implementation
- include tests when behavior changes
- prefer explicit, technically grounded additions over speculative abstractions

## License

This repository is released under the proprietary company license in [LICENSE](LICENSE).

## Correctness contracts

- Measurements must be terminal: a gate after any measurement raises `ValueError`.
  The returned statevector is the state before terminal measurement; counts and
  memory use classical bits in index order. Sequential mid-circuit measurement is
  outside this backend's scope.
- The dense backend rejects circuits above 10 qubits before allocation (one
  complex128 operator at the limit is 16 MiB, with additional temporary storage).
- Integer indices refer to this circuit. Typed references must be the objects
  returned by this circuit's registers; references from another register, even
  with the same label/index, and manually constructed references are rejected.
- Counts must be positive integers, seeds nonnegative integers or `None`, noise
  a finite probability in `[0, 1]`, and attack either `None` or `intercept_resend`.
  Thresholds require `0 <= benign_noise_max < attack_min <= 1`. Booleans are not
  numeric settings. Invalid settings raise `ValueError`.
- BB84 models Eve's basis-dependent measurement, Bob's remeasurement and public
  Alice/Bob basis sifting. The no-attack and intercept-resend models remain abstract.
- With no matched bases, `error_rate` is **None**, `secure` is **False** and
  `threat_level` is **insufficient_data**. Legacy result keys/imports are retained;
  consumers must handle the nullable QBER and the additional threat label.
- `secure=True` means only that a nonempty sample passed the legacy QBER threshold.
  It is not a cryptographic guarantee or a finite-key security assessment.
  Reconciliation and privacy amplification remain educational length heuristics.

CI installs the package, runs the unit regressions and all four public examples.
Controlled basis cases complement a seeded 40,000-bit attack check with a tolerance
of six binomial standard deviations around the model's expected 25% sifted QBER.

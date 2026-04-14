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
from q3.circuits import Circuit
from q3.simulator import StateVectorBackend

circuit = Circuit(num_qubits=2, num_clbits=2)
circuit.h(0).cx(0, 1).measure_all()

result = StateVectorBackend().run(circuit, shots=1024)
print(result["counts"])
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

Install the single runtime dependency:

```bash
python3 -m pip install numpy
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
- [docs/assumptions.md](docs/assumptions.md)
- [docs/metrics.md](docs/metrics.md)
- [docs/research_note.md](docs/research_note.md)
- [docs/roadmap.md](docs/roadmap.md)

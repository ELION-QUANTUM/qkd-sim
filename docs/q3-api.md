# Q³ v0.1 API Specification

## Language model

Q³ v0.1 is a Python-hosted embedded DSL.

This is deliberate:

- the semantics can stabilize before language-tooling work begins
- the API can be tested immediately
- the framework stays small and auditable

## Core syntax philosophy

- circuits are named
- qubits and classical bits are allocated explicitly
- gates act on typed references, not raw positional integers by default
- measurement is explicit
- execution is explicit

## Public objects

### Circuit

```python
Circuit(name: str | None = None, num_qubits: int = 0, num_clbits: int = 0)
```

Supported forms:

```python
Circuit("bell")
Circuit(num_qubits=2, num_clbits=2)
Circuit(2, num_clbits=2)   # compatibility form
```

Primary methods:

```python
qubits(size: int, label: str = "q") -> QubitRegister
bits(size: int, label: str = "c") -> ClassicalRegister
h(qubit: QubitRef | int) -> Circuit
x(qubit: QubitRef | int) -> Circuit
z(qubit: QubitRef | int) -> Circuit
cx(control: QubitRef | int, target: QubitRef | int) -> Circuit
measure(qubit: QubitRef | int, clbit: BitRef | int | None = None) -> Circuit
measure_all() -> Circuit
run(backend=None, shots: int = 1024, seed: int | None = None)
```

### Registers and references

```python
QubitRegister(size: int, label: str = "q")
ClassicalRegister(size: int, label: str = "c")
QubitRef(index: int, register: str = "q")
BitRef(index: int, register: str = "c")
```

Access pattern:

```python
q = circuit.qubits(2)
m = circuit.bits(2)

q[0]
m[0]
```

Registers are iterable, so this is valid:

```python
control, target = circuit.qubits(2)
left, right = circuit.bits(2)
```

### Backend and results

```python
StateVectorBackend(seed: int | None = None)
HardwareBackend()
RunResult(statevector, counts, shots, memory)
```

Result fields:

- `statevector`
- `counts`
- `shots`
- `memory`

`RunResult` supports both:

```python
result.counts
result["counts"]
```

## Example syntax

### Bell state

```python
from q3 import Circuit, StateVectorBackend

c = Circuit("bell")
q = c.qubits(2)
m = c.bits(2)

c.h(q[0])
c.cx(q[0], q[1])
c.measure(q[0], m[0])
c.measure(q[1], m[1])

result = StateVectorBackend().run(c, shots=1024)
print(result.counts)
```

### Single-qubit superposition

```python
c = Circuit("superposition")
q = c.qubits(1)
m = c.bits(1)

c.h(q[0])
c.measure(q[0], m[0])
```

### Basic measurement after X

```python
c = Circuit("measure_one")
q = c.qubits(1)
m = c.bits(1)

c.x(q[0])
c.measure(q[0], m[0])
```

## Qiskit comparison

Qiskit-style:

```python
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
```

Q³-style:

```python
c = Circuit("bell")
q = c.qubits(2)
m = c.bits(2)

c.h(q[0]).cx(q[0], q[1])
```

The meaningful difference is not cosmetic. Q³ centers named resource allocation and typed
references instead of a numeric container mindset.

## Error-handling philosophy

Q³ v0.1 rejects invalid usage early:

- invalid qubit index -> `IndexError`
- invalid classical bit index -> `IndexError`
- repeated register allocation -> `ValueError`
- invalid `CX` control/target combination -> `ValueError`
- unsupported hardware execution -> `NotImplementedError`

The framework does not silently create registers or silently coerce invalid usage.

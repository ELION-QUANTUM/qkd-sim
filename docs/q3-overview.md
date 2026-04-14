# Q³ Overview

## What Q³ is

Q³ is an experimental quantum programming framework for three related problem areas:

- quantum computation
- quantum communication
- system-level simulation

In this repository, Q³ is implemented as a Python-first prototype. It is not a standalone
compiled language and it is not a hardware runtime.

## Current architecture

Q³ is structured into four layers:

### 1. Language/API layer

The public interface is a small Python API:

- `QubitRegister`
- `ClassicalRegister`
- `QubitRef`
- `BitRef`
- `Circuit`
- `StateVectorBackend`

### 2. Circuit abstraction layer

Circuits are stored as typed instructions with:

- operation name
- target qubits
- optional control qubits
- optional classical destination for measurements

### 3. Simulation backend

The only implemented backend is a state-vector simulator for small experiments.

Current supported gates:

- `H`
- `X`
- `Z`
- `CX`

Measurement support:

- computational basis
- shot-based sampling
- per-shot collapse logic
- structured `RunResult` output

### 4. Communication layer

QKD modules live under `q3.communication.qkd`.

The current BB84 implementation is an abstract protocol model. It is useful for protocol-level
reasoning and reproducible experiments, but it does not simulate optics, hardware, or quantum
device physics.

## What problem Q³ is trying to solve

Current frameworks often separate computation tooling from communication tooling, or they grow
into large ecosystems quickly. Q³ is deliberately smaller.

Its design goals are:

- one framework for circuit experiments and communication protocols
- a compact core that is easy to audit
- explicit layering between circuits, simulation, and protocol logic
- hybrid workflows where classical decision code can consume quantum or QKD outputs

## How Q³ differs from existing tools

Q³ is not broader or more mature than Qiskit or Cirq. It differs in scope and structure:

- it keeps the computation core intentionally small
- it includes QKD communication work in the same framework
- it emphasizes modular layering over breadth
- it is designed as a research prototype, not a production ecosystem

## Current limitations

Q³ is still early-stage.

Current limitations:

- simulation-only
- no hardware execution
- no transpiler
- no advanced noise modeling
- small gate set
- not optimized for performance
- not feature-complete

The QKD module also remains abstract:

- protocol-level, not physical
- no device or optics model
- no complete cryptographic post-processing stack

## Current status

This repository now provides a credible prototype foundation:

- real circuit construction
- mathematically grounded state-vector simulation
- Bell-state and measurement examples
- QKD modeled as a communication subsystem

It does not yet provide a complete quantum software stack.

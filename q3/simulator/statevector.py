from __future__ import annotations

from collections import Counter
from typing import Dict, Optional, Protocol

import numpy as np

from q3.core.gates import I, SINGLE_QUBIT_GATES


class Backend(Protocol):
    def run(self, circuit, shots: int = 1024, seed: Optional[int] = None) -> Dict:
        ...


class HardwareBackend:
    """Reserved backend interface for future hardware connectors."""

    def run(self, circuit, shots: int = 1024, seed: Optional[int] = None) -> Dict:
        raise NotImplementedError(
            "Hardware execution is not implemented in this repository."
        )


class StateVectorBackend:
    """Small state-vector backend for auditable early-stage experiments."""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed

    def run(self, circuit, shots: int = 1024, seed: Optional[int] = None) -> Dict:
        if shots <= 0:
            raise ValueError("shots must be a positive integer.")

        rng = np.random.default_rng(self.seed if seed is None else seed)
        state = self._zero_state(circuit.num_qubits)
        measurements = []

        for instruction in circuit.instructions:
            if instruction.name == "MEASURE":
                measurements.append(instruction)
                continue
            state = self._apply_instruction(state, circuit.num_qubits, instruction)

        final_state = state.copy()
        counts = Counter()
        memory = []

        if measurements:
            for _ in range(shots):
                shot_state = final_state.copy()
                classical = [0] * circuit.num_clbits
                for instruction in measurements:
                    bit, shot_state = self._measure_qubit(
                        shot_state,
                        circuit.num_qubits,
                        instruction.targets[0],
                        rng,
                    )
                    classical[instruction.clbit] = bit

                bitstring = "".join(str(bit) for bit in classical)
                counts[bitstring] += 1
                memory.append(bitstring)

        return {
            "statevector": final_state,
            "counts": dict(counts),
            "shots": shots,
            "memory": memory,
        }

    @staticmethod
    def _zero_state(num_qubits: int) -> np.ndarray:
        state = np.zeros(2**num_qubits, dtype=complex)
        state[0] = 1.0 + 0.0j
        return state

    def _apply_instruction(self, state, num_qubits, instruction):
        if instruction.name in SINGLE_QUBIT_GATES:
            return self._apply_single_qubit_gate(
                state,
                num_qubits,
                instruction.targets[0],
                SINGLE_QUBIT_GATES[instruction.name],
            )
        if instruction.name == "CX":
            return self._apply_cx(
                state,
                num_qubits,
                instruction.controls[0],
                instruction.targets[0],
            )
        raise ValueError(f"Unsupported instruction: {instruction.name}")

    def _apply_single_qubit_gate(
        self, state: np.ndarray, num_qubits: int, target: int, gate: np.ndarray
    ) -> np.ndarray:
        operator = np.array([[1.0 + 0.0j]])
        for qubit in range(num_qubits):
            factor = gate if qubit == target else I
            operator = np.kron(operator, factor)
        return operator @ state

    def _apply_cx(
        self, state: np.ndarray, num_qubits: int, control: int, target: int
    ) -> np.ndarray:
        dimension = 2**num_qubits
        operator = np.zeros((dimension, dimension), dtype=complex)
        for basis in range(dimension):
            bits = [
                (basis >> (num_qubits - 1 - qubit)) & 1
                for qubit in range(num_qubits)
            ]
            if bits[control] == 1:
                bits[target] ^= 1

            output_index = 0
            for bit in bits:
                output_index = (output_index << 1) | bit

            operator[output_index, basis] = 1.0 + 0.0j

        return operator @ state

    def _measure_qubit(
        self,
        state: np.ndarray,
        num_qubits: int,
        qubit: int,
        rng: np.random.Generator,
    ):
        mask = 1 << (num_qubits - 1 - qubit)
        probabilities = np.abs(state) ** 2
        prob_zero = float(
            np.sum(probabilities[[index for index in range(len(state)) if (index & mask) == 0]])
        )
        outcome = 0 if rng.random() < prob_zero else 1

        collapsed = state.copy()
        for index in range(len(collapsed)):
            bit = 1 if (index & mask) else 0
            if bit != outcome:
                collapsed[index] = 0.0 + 0.0j

        norm = np.linalg.norm(collapsed)
        if norm == 0:
            raise RuntimeError("Measurement collapse produced a zero-norm state.")
        collapsed /= norm
        return outcome, collapsed

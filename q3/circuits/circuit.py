from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Instruction:
    name: str
    targets: Tuple[int, ...]
    controls: Tuple[int, ...] = ()
    clbit: Optional[int] = None


class Circuit:
    """Minimal quantum circuit abstraction for Q3."""

    def __init__(self, num_qubits: int, num_clbits: int = 0):
        if num_qubits <= 0:
            raise ValueError("Circuit must contain at least one qubit.")
        if num_clbits < 0:
            raise ValueError("Number of classical bits cannot be negative.")

        self.num_qubits = num_qubits
        self.num_clbits = num_clbits
        self.instructions = []

    def _validate_qubit(self, index: int) -> None:
        if index < 0 or index >= self.num_qubits:
            raise IndexError(f"Qubit index out of range: {index}")

    def _validate_clbit(self, index: int) -> None:
        if self.num_clbits == 0:
            raise ValueError(
                "Circuit has no classical register. "
                "Create it with num_clbits > 0 before measuring."
            )
        if index < 0 or index >= self.num_clbits:
            raise IndexError(f"Classical bit index out of range: {index}")

    def append(self, instruction: Instruction) -> "Circuit":
        for target in instruction.targets:
            self._validate_qubit(target)
        for control in instruction.controls:
            self._validate_qubit(control)
        if instruction.clbit is not None:
            self._validate_clbit(instruction.clbit)
        self.instructions.append(instruction)
        return self

    def h(self, qubit: int) -> "Circuit":
        return self.append(Instruction(name="H", targets=(qubit,)))

    def x(self, qubit: int) -> "Circuit":
        return self.append(Instruction(name="X", targets=(qubit,)))

    def z(self, qubit: int) -> "Circuit":
        return self.append(Instruction(name="Z", targets=(qubit,)))

    def cx(self, control: int, target: int) -> "Circuit":
        if control == target:
            raise ValueError("Control and target qubits must differ for CX.")
        return self.append(
            Instruction(name="CX", targets=(target,), controls=(control,))
        )

    def measure(self, qubit: int, clbit: Optional[int] = None) -> "Circuit":
        if clbit is None:
            clbit = qubit
        return self.append(
            Instruction(name="MEASURE", targets=(qubit,), clbit=clbit)
        )

    def measure_all(self) -> "Circuit":
        if self.num_clbits < self.num_qubits:
            raise ValueError(
                "measure_all requires at least as many classical bits as qubits."
            )
        for qubit in range(self.num_qubits):
            self.measure(qubit, qubit)
        return self

    def run(self, backend=None, shots: int = 1024, seed: Optional[int] = None):
        if backend is None:
            from q3.simulator import StateVectorBackend

            backend = StateVectorBackend(seed=seed)
        return backend.run(self, shots=shots, seed=seed)

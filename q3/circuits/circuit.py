from dataclasses import dataclass
from typing import Optional, Tuple, Union

from q3.core.registers import BitLike, ClassicalRegister, QubitLike, QubitRegister


@dataclass(frozen=True)
class Instruction:
    name: str
    targets: Tuple[int, ...]
    controls: Tuple[int, ...] = ()
    clbit: Optional[int] = None


class Circuit:
    """Minimal quantum circuit abstraction for Q3."""

    def __init__(
        self,
        name: Optional[Union[str, int]] = None,
        num_qubits: int = 0,
        num_clbits: int = 0,
    ):
        if isinstance(name, int):
            if num_qubits != 0:
                raise ValueError(
                    "If the first argument is an integer, do not also pass num_qubits."
                )
            num_qubits = name
            name = None

        if num_qubits < 0:
            raise ValueError("Number of qubits cannot be negative.")
        if num_clbits < 0:
            raise ValueError("Number of classical bits cannot be negative.")

        self.name = name or "circuit"
        self.num_qubits = num_qubits
        self.num_clbits = num_clbits
        self.instructions = []
        self._qubit_register = None
        self._classical_register = None

        if num_qubits > 0:
            self._qubit_register = QubitRegister(num_qubits)
        if num_clbits > 0:
            self._classical_register = ClassicalRegister(num_clbits)

    def qubits(self, size: int, label: str = "q") -> QubitRegister:
        if self._qubit_register is not None:
            raise ValueError("This circuit already has a qubit register.")
        register = QubitRegister(size=size, label=label)
        self._qubit_register = register
        self.num_qubits = len(register)
        return register

    def bits(self, size: int, label: str = "c") -> ClassicalRegister:
        if self._classical_register is not None:
            raise ValueError("This circuit already has a classical register.")
        register = ClassicalRegister(size=size, label=label)
        self._classical_register = register
        self.num_clbits = len(register)
        return register

    def _coerce_qubit(self, qubit: QubitLike) -> int:
        return qubit if isinstance(qubit, int) else qubit.index

    def _coerce_clbit(self, clbit: BitLike) -> int:
        return clbit if isinstance(clbit, int) else clbit.index

    def _validate_qubit(self, index: int) -> None:
        if index < 0 or index >= self.num_qubits:
            raise IndexError(f"Qubit index out of range: {index}")

    def _validate_clbit(self, index: int) -> None:
        if self.num_clbits == 0:
            raise ValueError(
                "Circuit has no classical register. "
                "Create it with bits(...) or num_clbits > 0 before measuring."
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

    def h(self, qubit: QubitLike) -> "Circuit":
        return self.append(
            Instruction(name="H", targets=(self._coerce_qubit(qubit),))
        )

    def x(self, qubit: QubitLike) -> "Circuit":
        return self.append(
            Instruction(name="X", targets=(self._coerce_qubit(qubit),))
        )

    def z(self, qubit: QubitLike) -> "Circuit":
        return self.append(
            Instruction(name="Z", targets=(self._coerce_qubit(qubit),))
        )

    def cx(self, control: QubitLike, target: QubitLike) -> "Circuit":
        control_index = self._coerce_qubit(control)
        target_index = self._coerce_qubit(target)
        if control_index == target_index:
            raise ValueError("Control and target qubits must differ for CX.")
        return self.append(
            Instruction(
                name="CX",
                targets=(target_index,),
                controls=(control_index,),
            )
        )

    def measure(
        self,
        qubit: QubitLike,
        clbit: Optional[BitLike] = None,
    ) -> "Circuit":
        qubit_index = self._coerce_qubit(qubit)
        if clbit is None:
            clbit_index = qubit_index
        else:
            clbit_index = self._coerce_clbit(clbit)
        return self.append(
            Instruction(name="MEASURE", targets=(qubit_index,), clbit=clbit_index)
        )

    def measure_all(self) -> "Circuit":
        if self.num_clbits < self.num_qubits:
            raise ValueError(
                "measure_all requires at least as many classical bits as qubits."
            )
        for qubit_index in range(self.num_qubits):
            self.measure(qubit_index, qubit_index)
        return self

    def run(self, backend=None, shots: int = 1024, seed: Optional[int] = None):
        if backend is None:
            from q3.simulator import StateVectorBackend

            backend = StateVectorBackend(seed=seed)
        return backend.run(self, shots=shots, seed=seed)

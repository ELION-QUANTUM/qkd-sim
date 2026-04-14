from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3 import Circuit, StateVectorBackend


def main() -> None:
    circuit = Circuit("single_x")
    q = circuit.qubits(1)
    m = circuit.bits(1)
    circuit.x(q[0]).measure(q[0], m[0])

    result = StateVectorBackend(seed=21).run(circuit, shots=256)

    print("Single-qubit X gate example")
    print("Counts:", result.counts)
    print("Statevector:", result.statevector)


if __name__ == "__main__":
    main()

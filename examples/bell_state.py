from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3 import Circuit, StateVectorBackend


def main() -> None:
    circuit = Circuit("bell")
    q = circuit.qubits(2)
    m = circuit.bits(2)
    circuit.h(q[0]).cx(q[0], q[1])
    circuit.measure(q[0], m[0]).measure(q[1], m[1])

    result = StateVectorBackend(seed=7).run(circuit, shots=2048)

    print("Bell-state counts")
    for bitstring, count in sorted(result.counts.items()):
        print(f"{bitstring}: {count}")
    print("")
    print("Statevector:")
    print(result.statevector)


if __name__ == "__main__":
    main()

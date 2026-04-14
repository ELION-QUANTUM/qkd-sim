from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from q3 import Circuit, StateVectorBackend


def main() -> None:
    circuit = Circuit("measure_h")
    q = circuit.qubits(1)
    m = circuit.bits(1)
    circuit.h(q[0]).measure(q[0], m[0])

    result = StateVectorBackend(seed=11).run(circuit, shots=1000)

    print("Measurement demo for H|0>")
    print("Counts:", result.counts)
    print("Memory sample:", result.memory[:10])


if __name__ == "__main__":
    main()

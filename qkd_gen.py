from qiskit import QuantumCircuit
from qiskit_aer import Aer
from random import randint

backend = Aer.get_backend("aer_simulator")

class qkd_generation:

    def __init__(self, num):
        self.num = num

        self.alice_bits  = [randint(0,1) for _ in range(num)]
        self.alice_basis = [randint(0,1) for _ in range(num)]
        self.bob_basis   = [randint(0,1) for _ in range(num)]
        self.bob_results = []

    def circuit_create(self):

        for i in range(self.num):

            qc = QuantumCircuit(1,1)

            if self.alice_bits[i] == 1:
                qc.x(0)

            if self.alice_basis[i] == 1:
                qc.h(0)

            if self.bob_basis[i] == 1:
                qc.h(0)

            qc.measure(0,0)

            job = backend.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()

            measured = list(counts.keys())[0]

            self.bob_results.append(int(measured))

        return self.bob_results
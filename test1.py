from qiskit import QuantumCircuit   
from qiskit_aer import Aer 

bd=Aer.get_backend("statevector_simulator")

# Binary data from IoT (DHT11 temperature = 29°C)
binary_data = "00011101"

n = len(binary_data)
qc = QuantumCircuit(n, n)

# Encode bits into qubits
for i, bit in enumerate(binary_data):
    if bit == "1":
        qc.x(i)

# Measure all qubits
qc.measure(range(n), range(n))

job=bd.run(qc,shot=1023)
result=job.result()

counts=result.get_counts()  # getting number of times that string was observed 

measured_binary = list(counts.keys())[0]
decoded_temp = int(measured_binary[::-1], 2)

print("Measured Binary:", measured_binary)
print("Decoded Temperature:", decoded_temp, "°C")
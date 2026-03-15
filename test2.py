import random
import socket
from qiskit import QuantumCircuit
from qiskit_aer import Aer

# ---------------- QKD KEY GENERATION ----------------
key = [1,0,1,1,0,0,1,0,1,0,1,0,0,1,1,0]
key_pos = 0

# ---------------- XOR DECRYPTION ----------------



def xor_decrypt(data_bits, key, pos):

    out = []

    for b in data_bits:
        out.append(b ^ key[pos % len(key)])
        pos += 1

    return out, pos


# ---------------- SERVER ----------------

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("Server listening...")

while True:

    conn, addr = server.accept()
    print("Client:", addr)

    data = conn.recv(1024).decode().strip()

    print("Encrypted bits:", data)

    enc_bits = [int(b) for b in data]

    key = [1,0,1,1,0,0,1,0,1,0,1,0,0,1,1,0]

    print("QKD key:", key)

    dec_bits, key_pos = xor_decrypt(enc_bits, key, key_pos)
    
    binary = "".join(str(b) for b in dec_bits)

    value = int(binary,2)

    print("Decrypted sensor value:", value)

    conn.close()
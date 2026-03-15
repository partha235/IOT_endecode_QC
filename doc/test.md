# **QKD (Quantum Key Distribution)** 

The most common QKD protocol is **BB84**, proposed by
Charles H. Bennett and Gilles Brassard.

---

# 🧠 What QKD Does

QKD is used to **securely generate a secret key** between two parties.



Even if someone intercepts the communication, the disturbance will be detected.

---

# ⚛️ BB84 Protocol Idea

Alice randomly chooses:

• **bit value** → 0 or 1
• **basis** → Z or X

Bob randomly chooses a basis to measure.

If bases match → keep the bit
If bases differ → discard

Final shared bits become the **secret key**.

---

# 🧪 BB84 Example Using Qiskit

Using **Qiskit**.

```python
import random
from qiskit import QuantumCircuit
from qiskit_aer import Aer

n = 16

alice_bits = [random.randint(0,1) for _ in range(n)]
alice_basis = [random.randint(0,1) for _ in range(n)]

bob_basis = [random.randint(0,1) for _ in range(n)]

backend = Aer.get_backend("aer_simulator")

bob_results = []

for i in range(n):

    qc = QuantumCircuit(1,1)

    # Alice encode bit
    if alice_bits[i] == 1:
        qc.x(0)

    # Alice encode basis
    if alice_basis[i] == 1:
        qc.h(0)

    # Bob measurement basis
    if bob_basis[i] == 1:
        qc.h(0)

    qc.measure(0,0)

    job = backend.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()

    measured = list(counts.keys())[0]

    bob_results.append(int(measured))

# Key generation
shared_key = []

for i in range(n):
    if alice_basis[i] == bob_basis[i]:
        shared_key.append(alice_bits[i])

print("Alice bits:", alice_bits)
print("Alice basis:", alice_basis)
print("Bob basis:", bob_basis)
print("Shared key:", shared_key)
```

---

# Example Output

```
Alice bits:  [1,0,1,1,0,1...]
Alice basis: [0,1,1,0,1,0...]
Bob basis:   [0,0,1,0,0,0...]

Shared key: [1,1,1,0,1]
```

This key can be used to **encrypt your hidden message**.

---

> “Quantum Key Distribution is used to generate a secure symmetric key for IoT message protection.”

---



Ahh 👍 now I understand your architecture better. You actually have **two separate systems**, which is a good design.

---

# 🧠 Your Project Architecture

### 1️⃣ ESP32-CAM System (Steganography)

```
ESP32-CAM
   │
Capture image
   │
Hide message in image (LSB)
   │
Send image to server
   │
Server extracts message
```

This part is **image steganography**.

---

### 2️⃣ ESP32-WROOM Sensor System (QKD Security)

```
Sensor (DHT11 / other)
       │
ESP32-WROOM
       │
Send sensor data
       │
Server runs QKD (BB84)
       │
Generate secure key
       │
Encrypt / decrypt sensor data
```

This part demonstrates **quantum secure communication**.

---

# 🔐 Where QKD Fits

The QKD key can encrypt sensor data before sending.

Example:

```
Temperature = 29°C
Binary = 00011101

QKD key = 10101010

Encrypted data = XOR
                 ↓
                10110111
```

Receiver decrypts using the **same QKD key**.

---

# 🧪 Example Python for Sensor Encryption

After generating the QKD key:

```python
def xor_encrypt(data_bits, key):

    encrypted = []

    for i in range(len(data_bits)):
        encrypted.append(data_bits[i] ^ key[i % len(key)])

    return encrypted
```

Example use:

```python
sensor_data = [0,0,0,1,1,1,0,1]   # 29°C
key = shared_key[:8]

encrypted = xor_encrypt(sensor_data, key)

print("Encrypted:", encrypted)
```

---

# 📡 Final System

Your project becomes:

```
SYSTEM 1
ESP32-CAM
↓
Image steganography
↓
Server decode

SYSTEM 2
ESP32-WROOM + Sensor
↓
Sensor data
↓
QKD (BB84) key generation
↓
Encrypted transmission
↓
Secure decoding
```

---

# 🎓 Good Project Title

Possible titles:

* **Quantum Key Distribution for Secure IoT Sensor Communication**
* **Hybrid IoT Security using QKD and Image Steganography**
* **Quantum-Secured IoT Data Transmission System**

---

# 🚀 If you want to make it much stronger

You could add **one more feature**:

⚛️ **Eavesdropper detection (Eve attack) in BB84**

That shows:

```
If someone intercepts the quantum channel
→ error rate increases
→ communication detected as compromised
```

That is the **main advantage of QKD** and impresses professors a lot.

---

Great 👍 let’s focus on **System 2 (ESP32-WROOM + Sensor + QKD)** and explain it clearly **without code**.

---

# 🧠 Goal of System 2

Securely transmit **sensor data from an ESP32 device** using a key generated through **Quantum Key Distribution (QKD)**.

The QKD protocol most commonly used is **BB84**, proposed by
Charles H. Bennett and Gilles Brassard.

The quantum simulation can be implemented using
Qiskit on the server.

---

# 🏗 System Architecture

```
Sensor (DHT11 / etc)
        │
        │  sensor reading
        ▼
ESP32-WROOM  (IoT device)
        │
        │  encrypted data
        ▼
Network (WiFi)
        │
        ▼
Server / PC
        │
        │  QKD key generation
        ▼
Secure sensor data recovery
```

Two things happen:

1️⃣ **QKD generates a secure key**
2️⃣ **Sensor data is encrypted using that key**

---

# ⚛️ Step 1: Sensor Data Collection

The ESP32 reads data from a sensor such as:

* Temperature
* Humidity
* Pressure
* Distance

Example:

```
Temperature = 29°C
```

The value is converted into **binary form** so it can be encrypted.

Example:

```
29 → 00011101
```

Binary format is easier for encryption operations.

---

# ⚛️ Step 2: Quantum Key Distribution

The server runs a **QKD simulation** to generate a **shared secret key**.

Two logical parties exist:

```
Alice → Sender
Bob   → Receiver
```

In your project:

```
ESP32  = Alice
Server = Bob
```

But the quantum operations are simulated on the server.

---

# ⚛️ Step 3: BB84 Key Generation

The BB84 protocol works like this.

### 1️⃣ Alice prepares random bits

Example:

```
Bits:   1 0 1 1 0 0 1 0
```

### 2️⃣ Alice chooses random bases

Two possible bases:

```
Z basis → |0⟩ |1⟩
X basis → |+⟩ |-⟩
```

Example:

```
Basis: Z X X Z Z X Z X
```

Each bit is encoded into a **quantum state**.

---

### 3️⃣ Bob randomly chooses measurement bases

Bob does not know Alice's bases.

Example:

```
Bob basis: X X Z Z X X Z Z
```

He measures the qubits using these bases.

---

### 4️⃣ Basis comparison

Alice and Bob compare bases over a **classical channel**.

Rules:

```
If bases match → keep bit
If bases differ → discard bit
```

Example:

```
Alice basis: Z X X Z Z X Z X
Bob basis:   X X Z Z X X Z Z

Matching positions → keep
```

These remaining bits form the **shared secret key**.

Example key:

```
10101
```

---

# ⚛️ Step 4: Encryption of Sensor Data

Now the sensor data is encrypted using the generated key.

Encryption uses a simple operation such as **XOR**.

Example:

```
Sensor data  : 00011101
QKD key      : 10101010
Encrypted    : 10110111
```

This encrypted data is transmitted.

---

# ⚛️ Step 5: Transmission

The ESP32 sends the encrypted sensor value to the server.

```
ESP32 → encrypted data → server
```

Even if someone intercepts the transmission, the data is unreadable.

---

# ⚛️ Step 6: Decryption

The server already has the **same QKD key**.

So it performs XOR again:

```
Encrypted data : 10110111
QKD key        : 10101010
Decrypted      : 00011101
```

Converted back to decimal:

```
00011101 → 29°C
```

Original sensor data is recovered.

---

# 🔐 Security Advantage

The key advantage of QKD is **eavesdropping detection**.

If a hacker tries to intercept the quantum states:

```
measurement disturbs the quantum system
```

This causes **bit errors**.

Alice and Bob detect this error rate and know that the channel is compromised.

This property is based on **quantum mechanics principles**.

---

# 🎯 What Your Second System Demonstrates

Your second system shows:

```
IoT Sensor
      │
Quantum Key Distribution
      │
Secure Key
      │
Encrypted Sensor Data
      │
Secure Transmission
```

This demonstrates **quantum-secured IoT communication**.

---

# 📊 Final Project Structure

Your full project now has **two independent security systems**.

```
SYSTEM 1
ESP32-CAM
Image steganography
Hidden message transmission

SYSTEM 2
ESP32-WROOM + Sensor
Quantum key distribution
Encrypted sensor data
```

---

If you want, I can also explain **one extremely important thing** next:

👉 **How to explain this whole system in a viva or project presentation in 2 minutes** (very useful for exams).



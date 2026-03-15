# IoT Encode Decode with Quantum Computer

This repo contains code for decoding and encoding IoT data by using Quantum computing. 

The **Quantum key Distribution** Protocol was used  for data transfer protection. 

Here is a clean, simple, and professional **README.md** file for your ESP32 Weather Station project with simulated QKD encryption.  
It's written in clear Markdown, easy to read, and suitable for GitHub or any documentation.

```markdown
# ESP32 Weather Station with Simulated QKD Encryption

A MicroPython-based IoT project that reads temperature from a BMP280 sensor on an ESP32, scales it, encrypts the data using a long shared secret key (simulating a Quantum Key Distribution / QKD-derived one-time pad), and sends it securely over TCP to a server.

**Educational demo**: Shows how a theoretically secure QKD key could protect real sensor data in an IoT environment.

## Features

- Reads temperature from BMP280 sensor  
- Scales temperature to 1 decimal place (e.g. 23.4 °C → 234)  
- Converts value to 16-bit binary  
- Encrypts using XOR with a long, rolling shared key (simulated QKD key)  
- Automatically reconnects to Wi-Fi if connection is lost  
- Sends encrypted binary string over plain TCP socket  
- Simple and lightweight – runs on standard ESP32 boards

## Hardware Requirements

- ESP32 development board (e.g. ESP32 DevKitC, NodeMCU-32S)  
- BMP280 temperature & pressure sensor (I²C)  
- Wires for I²C: SDA → GPIO 15, SCL → GPIO 2 (adjustable in code)  
- Stable 3.3V power supply

## Software Requirements

- MicroPython firmware for ESP32 (latest stable recommended)  
- Thonny, rshell, or mpremote for uploading code & libraries  
- BMP280 MicroPython library (`bmp280.py`)

Recommended libraries:  
- https://github.com/dafvid/micropython-bmp280  
- or https://github.com/robert-hh/BME280 (use `bme280_float.py` – works with BMP280)

## Installation

1. Flash MicroPython firmware to your ESP32  
2. Upload `bmp280.py` (or `bme280_float.py`) to the board root or `/lib` folder  
3. Upload `main.py` (this project code) to the board  
4. Edit Wi-Fi credentials, server IP, and port in the code:

```python
SSID = "your_wifi"
PASSWORD = "your_password"
SERVER_IP = "192.168.1.7"
PORT = 5000
```

5. Reset the ESP32 – it should connect and start sending data every 10 seconds

## How the "QKD Simulation" Works

- A 1024-bit (128-byte) random key is generated using `os.urandom()` (hardware TRNG on ESP32)  
- This simulates a long secret key shared via real Quantum Key Distribution  
- Each temperature reading is converted to 16 bits  
- XOR-encrypted using a rolling position in the key (stream-cipher style)  
- Key position advances after each use – never reused within the key length  
- In real QKD: fresh key material would be fetched periodically from a quantum device

**Important**: This is **not** production-grade security – it's an educational simulation. Real QKD requires quantum hardware and authenticated channels.

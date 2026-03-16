import random
import socket
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qkd_gen import qkd_generation
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# ---------------- QKD KEY GENERATION ----------------
key_gen = qkd_generation(16)
key = key_gen.circuit_create()
print(key)
key_pos = 0

latest_temp = 0
latest_hum = 0
latest_press = 0


import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class WebHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        html = f"""<!DOCTYPE html>
            <html>
            <head>
            <title>ESP32 Quantum IoT Dashboard</title>
            <meta http-equiv="refresh" content="2">

            <style>

            body{{
            background:#0d1117;
            color:#c9d1d9;
            font-family:Arial;
            text-align:center;
            margin:0;
            padding:20px;
            }}

            h1{{
            color:#00d4ff;
            text-shadow:0 0 10px #00d4ff;
            }}

            .container{{
            display:flex;
            justify-content:center;
            gap:30px;
            flex-wrap:wrap;
            margin-top:40px;
            }}

            .card{{
            background:#161b22;
            padding:30px;
            width:220px;
            border-radius:15px;
            font-size:22px;
            transition:0.3s;
            box-shadow:0 0 15px rgba(0,0,0,0.6);
            }}

            .card:hover{{
            transform:translateY(-10px) scale(1.05);
            box-shadow:0 0 25px rgba(0,212,255,0.5);
            }}

            .value{{
            font-size:45px;
            font-weight:bold;
            margin-top:10px;
            }}

            .temp{{color:#ff6b6b;}}
            .hum{{color:#4ecdc4;}}
            .press{{color:#f9ca24;}}

            .bar{{
            height:10px;
            background:#222;
            border-radius:10px;
            margin-top:15px;
            overflow:hidden;
            }}

            .fill{{
            height:100%;
            border-radius:10px;
            }}

            .temp-fill{{background:#ff6b6b;width:{{latest_temp*2}}%;}}
            .hum-fill{{background:#4ecdc4;width:{{latest_hum}}%;}}
            .press-fill{{background:#f9ca24;width:{{latest_press/12}}%;}}

            .footer{{
            margin-top:40px;
            opacity:0.6;
            font-size:14px;
            }}

            </style>
            </head>

            <body>

            <h1>Quantum Secured IoT Dashboard</h1>

            <div class="container">

            <div class="card">
             🌡️Temperature
            <div class="value temp">{latest_temp} °C</div>
            <div class="bar"><div class="fill temp-fill"></div></div>
            </div>

            <div class="card">
             🌬️Humidity
            <div class="value hum">{latest_hum} %</div>
            <div class="bar"><div class="fill hum-fill"></div></div>
            </div>

            <div class="card">
             🗜️Pressure
            <div class="value press">{latest_press} hPa</div>
            <div class="bar"><div class="fill press-fill"></div></div>
            </div>

            </div>

            <div class="footer">
            Auto refresh every 2 seconds
            </div>

            </body>
            </html>
                    """

        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(html.encode())


def start_web_server():
    httpd = HTTPServer(("0.0.0.0", 8080), WebHandler)
    print("Web server running on port 8080")
    httpd.serve_forever()


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

threading.Thread(target=start_web_server, daemon=True).start()

while True:

    conn, addr = server.accept()
    print("Client:", addr)

    data = conn.recv(1024).decode().strip()

    print("Encrypted bits:", data)

    enc_bits = [int(b) for b in data]

    print("QKD key:", key)

    dec_bits, key_pos = xor_decrypt(enc_bits, key, key_pos)
    
    # Convert decrypted bits to binary string
    binary = "".join(str(b) for b in dec_bits)
    
    # Split sensors
    temp_bits  = binary[0:16]
    hum_bits   = binary[16:32]
    press_bits = binary[32:48]
    
    # Convert to integers
    temp_val  = int(temp_bits, 2)
    hum_val   = int(hum_bits, 2)
    press_val = int(press_bits, 2)
    
    # Convert back to real values
    temp  = temp_val / 10
    hum   = hum_val / 10
    press = press_val / 10
    
    # global latest_temp, latest_hum, latest_press

    latest_temp = temp
    latest_hum = hum
    latest_press = press
    print("Temperature:", latest_temp, "°C")
    print("Humidity:", latest_hum, "%")
    print("Pressure:", latest_press, "hPa")

    conn.close()
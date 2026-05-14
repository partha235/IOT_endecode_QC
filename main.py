import network
import socket
import camera
import time
import urandom
import machine

# ================= WIFI ACCESS POINT =================
AP_SSID = "ESP32_CAM"
AP_PASSWORD = "12345678"   # minimum 8 characters

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

print("Starting Access Point...")

while not ap.active():
    pass

print("AP Started")
print("Connect to WiFi:", AP_SSID)
print("IP Address:", ap.ifconfig()[0])

# ================= SERVER CONFIG =================
# IMPORTANT: This should be your PC IP after connecting to ESP32 WiFi
SERVER_IP = "192.168.4.2"
PORT = 5000

# ================= WORD LIST =================
words = ["rock","arch","black hat","tree","water","fish"]

# ================= UTILS =================
def int_to_bits(value, bits):
    out = []
    for i in range(bits):
        out.append((value >> (bits - 1 - i)) & 1)
    return out

def embed_message(img_bytes, message):

    msg_bytes = message.encode()
    msg_len = len(msg_bytes)

    data = bytearray(img_bytes)

    bits = []

    # store message length (16 bits)
    bits += int_to_bits(msg_len, 16)

    offset = 500  # skip JPEG header

    # store message bits
    for b in msg_bytes:
        for i in range(8):
            bits.append((b >> (7 - i)) & 1)

    # embed bits into image
    for i in range(len(bits)):
        if offset + i < len(data):
            data[offset + i] = (data[offset + i] & 0xFE) | bits[i]

    return bytes(data)

# ================= CAMERA INIT =================
camera.init(0, format=camera.JPEG, framesize=camera.FRAME_QQVGA)

print("Camera ready")

# ================= MAIN LOOP =================
while True:

    print("Capturing image...")

    buf = camera.capture()

    print("Image size:", len(buf))

    # choose random words
    w1 = words[urandom.getrandbits(3) % len(words)]
    w2 = words[urandom.getrandbits(3) % len(words)]

    message = w1 + "," + w2

    print("Hidden message:", message)

    new_img = embed_message(buf, message)

    # convert image to HEX
    hex_data = ""

    for b in new_img:
        hex_data += "%02x" % b

    try:
        print("Connecting to server...")

        s = socket.socket()
        s.connect((SERVER_IP, PORT))

        print("Sending image...")

        chunk = 1024

        for i in range(0, len(hex_data), chunk):
            s.send(hex_data[i:i+chunk])

        s.close()

        print("Image sent")

    except Exception as e:
        print("Send failed:", e)

    print("Waiting 30 seconds...\n")

    time.sleep(30)
import json
import struct
import os

# ==========================
# File Paths
# ==========================

INPUT_FILE = "../Output/led_data.json"
OUTPUT_FILE = "../Output/logo.holo"

# ==========================
# Check Input
# ==========================

if not os.path.exists(INPUT_FILE):
    print("❌ led_data.json not found!")
    exit()

# ==========================
# Load LED Data
# ==========================

with open(INPUT_FILE, "r") as file:
    led_data = json.load(file)

angle_count = len(led_data)
led_count = len(led_data[0])

print("LED Count   :", led_count)
print("Angles      :", angle_count)

# ==========================
# Create HOLO File
# ==========================

with open(OUTPUT_FILE, "wb") as holo:

    # Magic Number
    holo.write(b'HOLO')

    # Version
    holo.write(struct.pack("B",1))

    # LED Count
    holo.write(struct.pack("<H",led_count))

    # Angle Count
    holo.write(struct.pack("<H",angle_count))

    # Frame Count
    holo.write(struct.pack("<H",1))

    # FPS
    holo.write(struct.pack("B",30))

    # Brightness
    holo.write(struct.pack("B",255))

    # ==========================
    # LED Data
    # ==========================

    for angle in led_data:

        for led in angle:

            r,g,b = led

            holo.write(struct.pack("BBB",r,g,b))

print("\n✅ HOLO file created successfully!")
print("Saved :", OUTPUT_FILE)

print("\nFile Information")
print("----------------------")
print("LEDs       :",led_count)
print("Angles     :",angle_count)
print("Frames     : 1")
print("FPS        : 30")
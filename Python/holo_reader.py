import struct
import os

INPUT_FILE = "../Output/logo.holo"

if not os.path.exists(INPUT_FILE):
    print("HOLO file not found!")
    exit()

with open(INPUT_FILE, "rb") as file:

    magic = file.read(4).decode()

    version = struct.unpack("B", file.read(1))[0]

    led_count = struct.unpack("<H", file.read(2))[0]

    angle_count = struct.unpack("<H", file.read(2))[0]

    frame_count = struct.unpack("<H", file.read(2))[0]

    fps = struct.unpack("B", file.read(1))[0]

    brightness = struct.unpack("B", file.read(1))[0]

print("========== HOLO FILE ==========")

print("Magic Number :", magic)

print("Version      :", version)

print("LED Count    :", led_count)

print("Angles       :", angle_count)

print("Frames       :", frame_count)

print("FPS          :", fps)

print("Brightness   :", brightness)

print("===============================")
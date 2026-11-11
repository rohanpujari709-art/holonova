import cv2
import json
import os

# ==============================
# File Paths
# ==============================

input_path = "../Output\polar_image.jpg"
output_path = "../Output/led_data.json"

# ==============================
# Check if Polar Image Exists
# ==============================

if not os.path.exists(input_path):
    print("❌ Polar image not found!")
    exit()

# ==============================
# Load Polar Image
# ==============================

polar = cv2.imread(input_path)

if polar is None:
    print("❌ Failed to load polar image!")
    exit()

print("✅ Polar image loaded successfully")

# ==============================
# Get Image Size
# ==============================

height, width, channels = polar.shape

print("\nImage Information")
print("-----------------------")
print("LED Count      :", height)
print("Angle Count    :", width)
print("Color Channels :", channels)

# ==============================
# Convert Polar Image to LED Data
# ==============================

led_data = []

for angle in range(width):

    angle_data = []

    for led in range(height):

        # OpenCV stores pixels as BGR
        b, g, r = polar[led, angle]

        rgb = [
            int(r),
            int(g),
            int(b)
        ]

        angle_data.append(rgb)

    led_data.append(angle_data)

# ==============================
# Save LED Data
# ==============================

with open(output_path, "w") as file:
    json.dump(led_data, file)

print("\n✅ LED Data Generated Successfully")
print("Saved to:", output_path)

# ==============================
# Display Sample Data
# ==============================

print("\nFirst Angle (Angle 0)")
print("-----------------------")

for i in range(min(5, len(led_data[0]))):
    print(f"LED {i+1}: {led_data[0][i]}")

print("\nTotal Angles :", len(led_data))
print("LEDs Per Angle :", len(led_data[0]))
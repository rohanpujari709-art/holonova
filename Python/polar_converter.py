import cv2
import os

# -----------------------------
# STEP 1 : Read Image
# -----------------------------
image = cv2.imread("../Images/test.jpg")

if image is None:
    print("Image not found!")
    exit()

print("Image Loaded Successfully!")

# -----------------------------
# STEP 2 : Resize Image
# -----------------------------
image = cv2.resize(image, (256, 256))

print("Image Resized to 256 x 256")

# -----------------------------
# STEP 3 : Get Image Center
# -----------------------------
height, width = image.shape[:2]

center = (width // 2, height // 2)

print("Center:", center)

# -----------------------------
# STEP 4 : Maximum Radius
# -----------------------------
radius = min(center)

print("Radius:", radius)

# -----------------------------
# STEP 5 : Convert Rectangle to Polar
# -----------------------------
polar = cv2.warpPolar(
    image,
    (360, radius),
    center,
    radius,
    cv2.WARP_FILL_OUTLIERS
)

print("Polar Conversion Completed")

# -----------------------------
# STEP 6 : Create Output Folder
# -----------------------------
os.makedirs("../Output", exist_ok=True)

# -----------------------------
# STEP 7 : Save Image
# -----------------------------
cv2.imwrite("../Output/polar_image.jpg", polar)

print("Polar Image Saved Successfully")
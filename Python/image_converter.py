import cv2

# Read image
image = cv2.imread("../Images/test.jpg")

if image is None:
    print("Image not found!")
    exit()

# Resize image
image = cv2.resize(image, (128, 128))

# Open output file
file = open("../Output/rgb_data.txt", "w")

height, width, _ = image.shape

for y in range(height):
    for x in range(width):

        # OpenCV stores colors as BGR
        b, g, r = image[y, x]

        file.write(f"{r},{g},{b}\n")

file.close()

print("RGB data saved successfully!")
import cv2
import os

# Input and Output folders
frame_folder = "../Output/frames"
output_folder = "../Output/rgb_frames"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get all frame images
frames = sorted(os.listdir(frame_folder))

# Process each frame
for frame_name in frames:

    # Process only JPG, JPEG, or PNG files
    if frame_name.lower().endswith((".jpg", ".jpeg", ".png")):

        # Read the frame
        image_path = os.path.join(frame_folder, frame_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not read {frame_name}")
            continue

        # Resize the frame
        image = cv2.resize(image, (128, 128))

        # Create output text filename
        txt_name = os.path.splitext(frame_name)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_name)

        # Write RGB values
        with open(txt_path, "w") as file:

            height, width, _ = image.shape

            for y in range(height):
                for x in range(width):

                    # OpenCV stores colors as BGR
                    b, g, r = image[y, x]

                    file.write(f"{r},{g},{b}\n")

        print(f"{frame_name} converted successfully!")

print("\nAll frames converted successfully!")
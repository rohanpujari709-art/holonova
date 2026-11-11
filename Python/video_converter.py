import cv2
import os

video = cv2.VideoCapture("../Videos/test.mp4")

output_folder = "../Output/frames"
os.makedirs(output_folder, exist_ok=True)

count = 0

while True:
    ret, frame = video.read()

    if not ret:
        break

    frame = cv2.resize(frame, (128, 128))

    cv2.imwrite(f"{output_folder}/frame_{count}.jpg", frame)

    count += 1

video.release()

print(f"{count} frames extracted successfully!")
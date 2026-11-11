import cv2
import os



def frame_to_rgb(frame):

    # Resize frame for LED matrix
    frame = cv2.resize(
        frame,
        (128,128)
    )


    height, width, _ = frame.shape


    rgb_data = []


    for y in range(height):

        row = []


        for x in range(width):

            b,g,r = frame[y,x]


            row.append([
                int(r),
                int(g),
                int(b)
            ])


        rgb_data.append(row)


    return rgb_data





def image_to_rgb_json(image_path):


    image = cv2.imread(image_path)


    if image is None:
        raise Exception("Image not found")


    return frame_to_rgb(image)







def video_to_rgb_json(video_path):


    cap = cv2.VideoCapture(video_path)


    if not cap.isOpened():

        raise Exception(
            "Video not found"
        )


    frames = []


    while True:


        success, frame = cap.read()


        if not success:
            break



        rgb_frame = frame_to_rgb(frame)


        frames.append(rgb_frame)



    cap.release()



    return frames
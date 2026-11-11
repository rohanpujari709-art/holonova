from PIL import Image
import numpy as np


def convert_image_to_led(image_path):

    img = Image.open(image_path)

    # Resize according to LED matrix size
    img = img.resize((32,32))

    img = img.convert("RGB")

    pixels = np.array(img)

    led_data = pixels.tolist()

    return led_data
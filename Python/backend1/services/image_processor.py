from PIL import Image


def prepare_image(image_path):
    img = Image.open(image_path)

    # Convert to RGBA
    img = img.convert("RGBA")

    # Resize for the holographic fan
    img = img.resize((256, 256))

    return img
from PIL import Image


def generate_led_matrix(image):
    """
    Convert a PIL image into a 2D RGB matrix.
    """

    width, height = image.size

    matrix = []

    for y in range(height):
        row = []

        for x in range(width):
            r, g, b, a = image.getpixel((x, y))

            row.append({
                "r": r,
                "g": g,
                "b": b,
                "a": a
            })

        matrix.append(row)

    return matrix
import math


def convert_to_radial(image):
    """
    Convert a square image into radial slices.

    Returns:
        List of 360 slices.
        Each slice contains RGBA pixels from the center outward.
    """

    width, height = image.size

    center_x = width // 2
    center_y = height // 2

    max_radius = min(center_x, center_y)

    radial_data = []

    # 360 degrees
    for angle in range(360):

        radians = math.radians(angle)

        slice_pixels = []

        # From center to edge
        for radius in range(max_radius):

            x = int(center_x + radius * math.cos(radians))
            y = int(center_y + radius * math.sin(radians))

            if 0 <= x < width and 0 <= y < height:
                r, g, b, a = image.getpixel((x, y))

                slice_pixels.append({
                    "r": r,
                    "g": g,
                    "b": b,
                    "a": a
                })

        radial_data.append(slice_pixels)

    return radial_data
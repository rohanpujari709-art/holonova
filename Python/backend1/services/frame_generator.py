def generate_frame(radial_data):
    """
    Create one hologram frame.

    Each frame contains:
    - total slices
    - pixels per slice
    - radial pixel data
    """

    frame = {
        "total_slices": len(radial_data),
        "pixels_per_slice": len(radial_data[0]),
        "data": radial_data
    }

    return frame
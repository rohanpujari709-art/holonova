import json
import os

OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def build_holo_file(frame, filename):
    """
    Build a HoloNova project file.

    This is the first version of the HoloNova format.
    """

    holo = {
        "version": "1.0",
        "device": "HoloNova Fan",
        "frame_count": 1,
        "frames": [
            frame
        ]
    }

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename + ".holo.json"
    )

    with open(output_path, "w") as f:
        json.dump(holo, f)

    return output_path
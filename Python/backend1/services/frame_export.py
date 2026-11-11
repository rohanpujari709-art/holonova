import json
import os

OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def save_frame(frame, filename):
    path = os.path.join(
        OUTPUT_FOLDER,
        filename + "_frame.json"
    )

    with open(path, "w") as f:
        json.dump(frame, f)

    return path
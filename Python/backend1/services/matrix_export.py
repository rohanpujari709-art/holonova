import os
import json

OUTPUT_FOLDER = "data"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def save_matrix(matrix, filename):
    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename + ".json"
    )

    with open(output_path, "w") as f:
        json.dump(matrix, f)

    return output_path
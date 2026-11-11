import os
from fastapi import UploadFile

UPLOAD_DIR = "Images"

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_image(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    return file.filename
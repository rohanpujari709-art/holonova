from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

import os
import uuid
import shutil
import traceback

from dotenv import load_dotenv
from supabase import create_client
from PIL import Image


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is missing from .env")


print("SUPABASE URL:", SUPABASE_URL)
print("SUPABASE KEY:", "FOUND" if SUPABASE_KEY else "MISSING")


# ============================================================
# SUPABASE CLIENT
# ============================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = "Images"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# ============================================================
# LED MATRIX SIZE
# ============================================================

LED_WIDTH = 128
LED_HEIGHT = 128


# ============================================================
# IMAGE -> LED RGB DATA
# ============================================================

def image_to_led_data(image_path: str):

    print()
    print("--------------------------------------")
    print("Converting image to LED data")
    print("--------------------------------------")

    image = Image.open(image_path)

    print(
        "Original image size:",
        image.size
    )

    image = image.convert("RGB")

    image = image.resize(
        (
            LED_WIDTH,
            LED_HEIGHT
        )
    )

    print(
        "LED image size:",
        image.size
    )

    pixels = list(
        image.getdata()
    )

    led_data = []

    index = 0

    for y in range(LED_HEIGHT):

        row = []

        for x in range(LED_WIDTH):

            r, g, b = pixels[index]

            row.append(
                [
                    int(r),
                    int(g),
                    int(b)
                ]
            )

            index += 1

        led_data.append(row)

    print(
        "LED rows:",
        len(led_data)
    )

    print(
        "LED columns:",
        len(led_data[0])
    )

    return led_data


# ============================================================
# UPLOAD ENDPOINT
# ============================================================

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_path = None
    hologram_id = None

    try:

        print()
        print("======================================")
        print("       HOLONOVA UPLOAD START")
        print("======================================")

        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="No file selected"
            )

        print(
            "Original filename:",
            file.filename
        )

        # ----------------------------------------------------
        # CREATE HOLOGRAM ID
        # ----------------------------------------------------

        hologram_id = str(
            uuid.uuid4()
        )

        print(
            "Hologram ID:",
            hologram_id
        )

        # ----------------------------------------------------
        # FILE EXTENSION
        # ----------------------------------------------------

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp"
        }

        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Please upload JPG, JPEG, PNG, GIF or WEBP."
                )
            )

        # ----------------------------------------------------
        # SAVE FILE LOCALLY
        # ----------------------------------------------------

        new_filename = (
            hologram_id + extension
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            new_filename
        )

        print(
            "Saving file to:",
            file_path
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        if not os.path.exists(file_path):

            raise Exception(
                "Uploaded file was not created"
            )

        file_size = os.path.getsize(
            file_path
        )

        print(
            "File size:",
            file_size,
            "bytes"
        )

        # ----------------------------------------------------
        # GENERATE LED DATA
        # ----------------------------------------------------

        led_data = image_to_led_data(
            file_path
        )

        print(
            "LED data generated successfully"
        )

        # ----------------------------------------------------
        # INSERT HOLOGRAM AS PROCESSING
        # ----------------------------------------------------

        hologram_record = {

            "id":
                hologram_id,

            "image_name":
                file.filename,

            "total_frames":
                1,

            "width":
                LED_WIDTH,

            "height":
                LED_HEIGHT,

            "status":
                "processing"
        }

        hologram_response = (
            supabase
            .table("holograms")
            .insert(
                hologram_record
            )
            .execute()
        )

        print(
            "HOLOGRAM INSERT RESPONSE:",
            hologram_response.data
        )

        # ----------------------------------------------------
        # INSERT LED FRAME
        # ----------------------------------------------------

        led_frame_record = {

            "hologram_id":
                hologram_id,

            "frame_number":
                1,

            "led_data":
                led_data
        }

        led_response = (
            supabase
            .table("led_frames")
            .insert(
                led_frame_record
            )
            .execute()
        )

        print(
            "LED FRAME INSERT RESPONSE:",
            led_response.data
        )

        # ----------------------------------------------------
        # UPDATE STATUS TO COMPLETED
        # ----------------------------------------------------

        update_response = (
            supabase
            .table("holograms")
            .update(
                {
                    "status":
                        "completed"
                }
            )
            .eq(
                "id",
                hologram_id
            )
            .execute()
        )

        print()
        print(
            "STATUS UPDATE RESPONSE:",
            update_response.data
        )

        # ----------------------------------------------------
        # VERIFY STATUS FROM SUPABASE
        # ----------------------------------------------------

        verify_response = (
            supabase
            .table("holograms")
            .select(
                "id,image_name,status,width,height,total_frames"
            )
            .eq(
                "id",
                hologram_id
            )
            .execute()
        )

        print(
            "STATUS AFTER UPDATE:",
            verify_response.data
        )

        # ----------------------------------------------------
        # MAKE SURE UPDATE ACTUALLY WORKED
        # ----------------------------------------------------

        if not verify_response.data:

            raise Exception(
                "Unable to verify hologram after upload"
            )

        final_record = (
            verify_response.data[0]
        )

        final_status = (
            final_record.get("status")
        )

        if final_status != "completed":

            raise Exception(
                "Hologram status update failed. "
                f"Current status: {final_status}"
            )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print()
        print("======================================")
        print("       HOLOGRAM CREATED")
        print("======================================")

        print(
            "Hologram ID:",
            hologram_id
        )

        print(
            "Frames:",
            1
        )

        print(
            "Resolution:",
            f"{LED_WIDTH} x {LED_HEIGHT}"
        )

        print(
            "Final status:",
            final_status
        )

        print()

        return JSONResponse(

            status_code=200,

            content={

                "success":
                    True,

                "message":
                    "Hologram created successfully",

                "hologram_id":
                    hologram_id,

                "filename":
                    file.filename,

                "saved_file":
                    new_filename,

                "file_size":
                    file_size,

                "total_frames":
                    1,

                "width":
                    LED_WIDTH,

                "height":
                    LED_HEIGHT,

                "status":
                    final_status
            }
        )


    # ========================================================
    # FASTAPI ERROR
    # ========================================================

    except HTTPException:

        raise


    # ========================================================
    # GENERAL ERROR
    # ========================================================

    except Exception as e:

        print()
        print("======================================")
        print("          UPLOAD ERROR")
        print("======================================")

        print(
            "Exception:",
            str(e)
        )

        print()
        print("Traceback:")

        traceback.print_exc()

        if (
            file_path
            and os.path.exists(file_path)
        ):

            try:

                os.remove(file_path)

            except Exception:

                pass

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    # ========================================================
    # CLOSE FILE
    # ========================================================

    finally:

        try:

            await file.close()

        except Exception:

            pass


# ============================================================
# GET ALL HOLOGRAMS
# ============================================================

@router.get("/holograms")
def get_holograms():

    try:

        response = (
            supabase
            .table("holograms")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return {
            "success":
                True,

            "holograms":
                response.data
        }

    except Exception as e:

        print(
            "GET HOLOGRAMS ERROR:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# GET ONE HOLOGRAM API
# ============================================================

@router.get(
    "/api/hologram/{hologram_id}"
)
def get_hologram(
    hologram_id: str
):

    try:

        response = (
            supabase
            .table("holograms")
            .select("*")
            .eq(
                "id",
                hologram_id
            )
            .execute()
        )

        if not response.data:

            raise HTTPException(
                status_code=404,
                detail="Hologram not found"
            )

        return {
            "success":
                True,

            "hologram":
                response.data[0]
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            "GET HOLOGRAM ERROR:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# LED FRAME API
#
# NOTE:
# /led-frame/{id} is handled by led_router.py.
# This API uses /api/led-frame/{id} so there is no route clash.
# ============================================================

@router.get(
    "/api/led-frame/{hologram_id}"
)
def get_led_frame_api(
    hologram_id: str
):

    try:

        response = (
            supabase
            .table("led_frames")
            .select("*")
            .eq(
                "hologram_id",
                hologram_id
            )
            .order(
                "frame_number"
            )
            .execute()
        )

        return {
            "success":
                True,

            "frames":
                response.data
        }

    except Exception as e:

        print(
            "GET LED FRAME ERROR:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
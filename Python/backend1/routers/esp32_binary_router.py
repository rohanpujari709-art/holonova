from fastapi import APIRouter, Response, HTTPException

from services.storage_service import get_led_frames


router = APIRouter(
    prefix="/api/esp32",
    tags=["ESP32 Binary"]
)



@router.get("/binary/{hologram_id}")
async def get_binary_frame(hologram_id: str):

    frames = get_led_frames(hologram_id)


    if not frames:
        raise HTTPException(
            status_code=404,
            detail="Frame not found"
        )


    led_data = frames[0]["led_data"]


    rgb_bytes = bytearray()


    for row in led_data:

        for pixel in row:

            rgb_bytes.append(pixel[0])  # R
            rgb_bytes.append(pixel[1])  # G
            rgb_bytes.append(pixel[2])  # B



    return Response(
        content=bytes(rgb_bytes),
        media_type="application/octet-stream"
    )
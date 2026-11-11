from fastapi import APIRouter, HTTPException

from services.storage_service import get_led_frames


router = APIRouter(
    prefix="/api/esp32",
    tags=["ESP32"]
)


@router.get("/frame/{hologram_id}")
async def get_frame(hologram_id: str):

    frames = get_led_frames(hologram_id)

    if not frames:
        raise HTTPException(
            status_code=404,
            detail="Frame not found"
        )


    frame = frames[0]


    return {
        "frame_number": frame["frame_number"],
        "led_data": frame["led_data"],
        "status": "ready"
    }
from fastapi import APIRouter, HTTPException
from supabase_client import supabase


router = APIRouter()


@router.get("/led-frame/{hologram_id}")
def get_led_frame(hologram_id: str):

    try:

        response = (
            supabase
            .table("led_frames")
            .select("*")
            .eq("hologram_id", hologram_id)
            .execute()
        )


        return response.data


    except Exception as e:

        print("LED FRAME ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
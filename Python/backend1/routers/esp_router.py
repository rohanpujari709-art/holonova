from fastapi import APIRouter, HTTPException
import os

from dotenv import load_dotenv
from supabase import create_client


# ==========================================
# ROUTER
# ==========================================

router = APIRouter()


# ==========================================
# SUPABASE
# ==========================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL missing")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY missing")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================
# ESP8266 TEST
# ==========================================

@router.get("/esp/test")
def esp_test():

    return {
        "success": True,
        "message": "ESP8266 API WORKING"
    }


# ==========================================
# ESP8266 GET LATEST LED DATA
# ==========================================

@router.get("/esp/led_data")
def get_esp_led_data():

    try:

        # Find latest completed hologram
        hologram_response = (
            supabase
            .table("holograms")
            .select("id,image_name,status")
            .eq("status", "completed")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        if not hologram_response.data:
            raise HTTPException(
                status_code=404,
                detail="No completed hologram found"
            )

        hologram = hologram_response.data[0]
        hologram_id = hologram["id"]

        # Get first LED frame
        frame_response = (
            supabase
            .table("led_frames")
            .select("frame_number,led_data")
            .eq("hologram_id", hologram_id)
            .order("frame_number")
            .limit(1)
            .execute()
        )

        if not frame_response.data:
            raise HTTPException(
                status_code=404,
                detail="No LED frame found"
            )

        frame = frame_response.data[0]

        return {
            "success": True,
            "hologram_id": hologram_id,
            "image_name": hologram["image_name"],
            "frame_number": frame["frame_number"],
            "led_data": frame["led_data"]
        }

    except HTTPException:
        raise

    except Exception as e:

        print("ESP ROUTER ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
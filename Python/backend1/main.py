from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ============================================================
# IMPORT ROUTERS
# ============================================================

from routers.upload_router import router as upload_router
from routers.led_router import router as led_router
from routers.dashboard_router import router as dashboard_router


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="HoloNova API",
    description="Backend API for the HoloNova LED Hologram System",
    version="1.0.0"
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ============================================================
# HTML TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# INCLUDE ROUTERS
# ============================================================

app.include_router(upload_router)
app.include_router(led_router)
app.include_router(dashboard_router)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ============================================================
# UPLOAD PAGE
# ============================================================

@app.get("/upload-page")
async def upload_page(request: Request):

    return templates.TemplateResponse(
        "upload.html",
        {
            "request": request
        }
    )


# ============================================================
# HOLOGRAM PREVIEW PAGE
# ============================================================

@app.get("/hologram/{hologram_id}")
async def hologram_page(
    request: Request,
    hologram_id: str
):

    return templates.TemplateResponse(
        "hologram.html",
        {
            "request": request,
            "hologram_id": hologram_id
        }
    )


# ============================================================
# GALLERY PAGE
# ============================================================

@app.get("/gallery")
async def gallery_page(request: Request):

    return templates.TemplateResponse(
        "gallery.html",
        {
            "request": request
        }
    )


# ============================================================
# ABOUT PAGE
# ============================================================

@app.get("/about")
async def about_page(request: Request):

    return templates.TemplateResponse(
        "about.html",
        {
            "request": request
        }
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "success": True,
        "status": "ok",
        "application": "HoloNova",
        "message": "HoloNova Backend Running",
        "version": "1.0.0"
    }
# ESP8266 TEST ROUTE
@app.get("/esp-test")
def esp_test():
    return {
        "success": True,
        "message": "HoloNova ESP8266 connection working"
    }
# ============================================================
# ESP8266 - GET ONE RGB ROW
# ============================================================

@app.get("/esp-row/{hologram_id}/{row}")
def esp_row(hologram_id: str, row: int):

    # ESP8266 should request rows from 0 to 127 only
    if row < 0 or row > 127:
        return {
            "success": False,
            "message": "Row must be between 0 and 127"
        }

    try:
        # Import the same Supabase client already used by HoloNova
        from routers.upload_router import supabase

        response = (
            supabase.table("led_frames")
            .select("frame_number,led_data")
            .eq("hologram_id", hologram_id)
            .order("frame_number")
            .limit(1)
            .execute()
        )

        if not response.data:
            return {
                "success": False,
                "message": "LED frame not found"
            }

        led_data = response.data[0]["led_data"]

        return {
            "success": True,
            "hologram_id": hologram_id,
            "row": row,
            "pixels": led_data[row]
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

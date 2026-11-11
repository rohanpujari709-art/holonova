from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from services.storage_service import (
    get_dashboard_stats,
    get_all_holograms
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/dashboard")
async def dashboard(request: Request):

    stats = get_dashboard_stats()

    holograms = get_all_holograms()


    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "stats": stats,
            "holograms": holograms
        }
    )
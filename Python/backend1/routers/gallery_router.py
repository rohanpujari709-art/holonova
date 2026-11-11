from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.storage_service import (
    get_all_holograms,
    delete_hologram
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# Gallery page
@router.get("/gallery")
async def gallery(request: Request):

    holograms = get_all_holograms()

    return templates.TemplateResponse(
        "gallery.html",
        {
            "request": request,
            "holograms": holograms
        }
    )



# Delete hologram
@router.get("/delete-hologram/{hologram_id}")
async def delete(hologram_id: str):

    delete_hologram(hologram_id)

    return RedirectResponse(
        url="/gallery",
        status_code=303
    )
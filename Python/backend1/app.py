from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.upload_router import router

app = FastAPI(
    title="HoloNova API",
    description="Backend API for HoloNova",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "HoloNova Backend Running"
    }
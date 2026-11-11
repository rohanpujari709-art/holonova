from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers are inside Python/backend1/routers
from backend1.routers import upload_router
from backend1.routers import esp_router


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="HoloNova API",
    description="Backend API for HoloNova holographic display system",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REGISTER ROUTERS
# ============================================================

app.include_router(upload_router.router)
app.include_router(esp_router.router)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "HoloNova Backend Running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "success": True,
        "status": "online",
        "system": "HoloNova"
    }
# ============================================================
# ESP8266 CONNECTION TEST
# ============================================================

@app.get("/esp-test")
def esp_test():
    return {
        "success": True,
        "message": "HoloNova ESP8266 connection working"
    }
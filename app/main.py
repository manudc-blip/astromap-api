from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from app.routers.health import router as health_router
from app.routers.cities import router as cities_router
from app.routers.theme import router as theme_router

app = FastAPI(
    title="AstroMap API",
    version="1.0.0",
    description="API backend pour le moteur AstroMap de GéoAstro.",
)

STATIC_GLYPHS_DIR = Path(__file__).resolve().parent / "static" / "Glyphes_PNG"
app.mount("/glyphes", StaticFiles(directory=STATIC_GLYPHS_DIR), name="glyphes")

# À resserrer plus tard sur ton vrai domaine
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://geoastro.org",
        "https://www.geoastro.org",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(cities_router)
app.include_router(theme_router)

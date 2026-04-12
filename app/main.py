from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.cities import router as cities_router
from app.routers.theme import router as theme_router
from fastapi import HTTPException
from init_pg_schema import main as init_pg_schema_main

app = FastAPI(
    title="AstroMap API",
    version="1.0.0",
    description="API backend pour le moteur AstroMap de GéoAstro.",
)

@app.get("/_internal/init-db-manudc-20260412")
def init_db_once():
    try:
        init_pg_schema_main()
        return {"ok": True, "message": "Schéma PostgreSQL créé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

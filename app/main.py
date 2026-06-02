import os
from fastapi import FastAPI, Header, HTTPException, Depends
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from app.routers.health import router as health_router
from app.routers.cities import router as cities_router
from app.routers.theme import router as theme_router
from app.routers.ret import router as ret_router
from app.routers.transits import router as transits_router
from app.routers.aspects import router as aspects_router
from app.routers.interpretation import router as interpretation_router

app = FastAPI(
    title="AstroMap API",
    version="1.0.0",
    description="API backend pour le moteur AstroMap de GéoAstro.",
)

JWT_SECRET = os.getenv("JWT_SECRET", "change_me")

def require_astromap_access(
    authorization: str | None = Header(default=None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token d'accès manquant.")

    token = authorization.replace("Bearer ", "").strip()

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"],
            issuer="geoastro",
            audience="geoastro-software"
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Token d'accès invalide ou expiré.")

    permissions = payload.get("permissions", [])
    target = payload.get("target")

    if target != "astromap":
        raise HTTPException(status_code=403, detail="Token non valable pour AstroMap.")

    if "astromap_full" not in permissions:
        raise HTTPException(status_code=403, detail="Permission AstroMap manquante.")

    return payload

STATIC_GLYPHS_DIR = Path(__file__).resolve().parent / "static" / "Glyphes_SVG"
app.mount("/glyphes", StaticFiles(directory=STATIC_GLYPHS_DIR), name="glyphes")

# À resserrer plus tard sur ton vrai domaine
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://geoastro.org",
        "https://www.geoastro.org",
        "https://astromap-web.vercel.app",
        "https://astromap-web-git-main-manuel-dcs-projects.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(cities_router)
app.include_router(
    theme_router,
    dependencies=[Depends(require_astromap_access)]
)
app.include_router(
    ret_router,
    dependencies=[Depends(require_astromap_access)]
)
app.include_router(
    transits_router,
    dependencies=[Depends(require_astromap_access)]
)
app.include_router(
    aspects_router,
    dependencies=[Depends(require_astromap_access)]
)
app.include_router(
    interpretation_router,
    dependencies=[Depends(require_astromap_access)]
)

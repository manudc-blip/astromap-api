from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from astromap.core.theme import Theme

app = FastAPI(title="AstroMap API")


class ThemeRequest(BaseModel):
    name: str = "Unknown"
    datetime_local: str
    latitude: float
    longitude: float
    tz: str
    house_system: str = "Placidus"


@app.get("/")
def root():
    return {"message": "AstroMap API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/theme/test")
def theme_test():
    """
    Endpoint de test minimal pour vérifier que le moteur AstroMap
    tourne bien sur Railway.
    """
    try:
        result = Theme.compute(
            name="Albert Einstein",
            datetime_local="1879-03-14 11:30",
            latitude=48.8566,
            longitude=2.3522,
            tz="Europe/Paris",
            settings={"house_system": "Placidus"},
        )
        return result.to_json()

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "type": type(e).__name__,
            },
        )


@app.post("/theme/compute")
def theme_compute(payload: ThemeRequest):
    """
    Calcul réel d'un thème à partir des paramètres envoyés par le front.
    """
    try:
        result = Theme.compute(
            name=payload.name,
            datetime_local=payload.datetime_local,
            latitude=payload.latitude,
            longitude=payload.longitude,
            tz=payload.tz,
            settings={"house_system": payload.house_system},
        )
        return result.to_json()

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "type": type(e).__name__,
            },
        )

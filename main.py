from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from astromap.core.theme import Theme

app = FastAPI(title="AstroMap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://geoastro.org",
        "https://www.geoastro.org",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ThemeRequest(BaseModel):
    name: str
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

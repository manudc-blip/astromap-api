from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import ThemeRequest
from app.services.transits_service import compute_transits_payload


router = APIRouter(prefix="/transits", tags=["transits"])


class TransitsRequest(ThemeRequest):
    transit_datetime_local: str
    aspect_mode: str = "TN"


@router.post("")
def compute_transits(payload: TransitsRequest):
    try:
        data = compute_transits_payload(
            name=payload.name or "",
            natal_datetime_local=payload.datetime_local,
            transit_datetime_local=payload.transit_datetime_local,
            latitude=payload.latitude,
            longitude=payload.longitude,
            tz=payload.tz,
            settings=payload.settings.model_dump(),
            aspect_mode=payload.aspect_mode,
        )
        return data

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul des transits: {exc}",
        ) from exc

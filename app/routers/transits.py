from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from app.schemas import ThemeRequest
from app.services.transits_service import compute_transits_payload
from astromap.core.transits_svg import render_transits_svg


router = APIRouter(prefix="/transits", tags=["transits"])


class TransitsRequest(ThemeRequest):
    transit_datetime_local: str
    aspect_mode: str = "TN"

@router.post("/svg")
def compute_transits_svg(payload: TransitsRequest) -> Response:
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

        lang = "fr"
        settings_dict = payload.settings.model_dump()
        if str(settings_dict.get("language", "fr")).lower().startswith("en"):
            lang = "en"
        
        svg = render_transits_svg(
            data["natal"],
            data["transit"],
            width=1400,
            height=900,
            language=lang,
            aspect_mode=payload.aspect_mode,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        )

        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG des transits: {exc}",
        ) from exc

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

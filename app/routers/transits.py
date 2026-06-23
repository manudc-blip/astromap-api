from fastapi import APIRouter, Depends, HTTPException, Response
from functools import lru_cache
import json

from app.security import get_access_mode, require_trial_einstein

from app.schemas import ThemeRequest
from app.services.transits_service import compute_transits_payload
from astromap.core.transits_svg import render_transits_svg


router = APIRouter(prefix="/transits", tags=["transits"])

def _transits_cache_key(payload: "TransitsRequest") -> str:
    return json.dumps(
        {
            "name": payload.name or "",
            "natal_datetime_local": payload.datetime_local,
            "transit_datetime_local": payload.transit_datetime_local,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "tz": payload.tz,
            "settings": payload.settings.model_dump(),
            "aspect_mode": payload.aspect_mode,
        },
        sort_keys=True,
        ensure_ascii=False,
    )

@lru_cache(maxsize=256)
def _compute_transits_payload_cached(cache_key: str):
    data = json.loads(cache_key)

    return compute_transits_payload(
        name=data["name"],
        natal_datetime_local=data["natal_datetime_local"],
        transit_datetime_local=data["transit_datetime_local"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        tz=data["tz"],
        settings=data["settings"],
        aspect_mode=data["aspect_mode"],
    )


def get_cached_transits_payload(payload: "TransitsRequest"):
    return _compute_transits_payload_cached(_transits_cache_key(payload))


class TransitsRequest(ThemeRequest):
    transit_datetime_local: str
    aspect_mode: str = "TN"

@router.post("/svg")
def compute_transits_svg(
    payload: TransitsRequest,
    mode: str = Depends(get_access_mode),
) -> Response:
    try:
        require_trial_einstein(payload, mode)
        data = get_cached_transits_payload(payload)

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
def compute_transits(
    payload: TransitsRequest,
    mode: str = Depends(get_access_mode),
):
    try:
        require_trial_einstein(payload, mode)
        data = get_cached_transits_payload(payload)
        return data

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul des transits: {exc}",
        ) from exc

@router.post("/svg-publication")
def compute_transits_svg_publication(
    payload: TransitsRequest,
    mode: str = Depends(get_access_mode),
) -> Response:
    try:
        require_trial_einstein(payload, mode)
        data = get_cached_transits_payload(payload)

        lang = "fr"
        settings_dict = payload.settings.model_dump()
        if str(settings_dict.get("language", "fr")).lower().startswith("en"):
            lang = "en"

        svg = render_transits_svg(
            data["natal"],
            data["transit"],
            width=650,
            height=650,
            language=lang,
            aspect_mode=payload.aspect_mode,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
            inline_glyphs=True,
            inline_glyphs=True,
            show_footer=False,
        )

        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG publication des transits: {exc}",
        ) from exc

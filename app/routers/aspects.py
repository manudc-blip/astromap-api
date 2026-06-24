from fastapi import APIRouter, Depends, HTTPException, Response
from functools import lru_cache
import json

from app.schemas import ThemeRequest, ThemeResponse
from app.services.aspects_service import compute_aspects_payload, compute_aspects_svg
from app.security import get_access_mode, require_trial_einstein

router = APIRouter(prefix="/aspects", tags=["aspects"])

def _aspects_cache_key(payload: ThemeRequest) -> str:
    return json.dumps(
        {
            "name": payload.name or "",
            "datetime_local": payload.datetime_local,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "tz": payload.tz,
            "settings": payload.settings.model_dump(),
        },
        sort_keys=True,
        ensure_ascii=False,
    )


@lru_cache(maxsize=256)
def _compute_aspects_payload_cached(cache_key: str):
    data = json.loads(cache_key)

    return compute_aspects_payload(
        name=data["name"],
        datetime_local=data["datetime_local"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        tz=data["tz"],
        settings=data["settings"],
    )


def get_cached_aspects_payload(payload: ThemeRequest):
    return _compute_aspects_payload_cached(_aspects_cache_key(payload))

@router.post("", response_model=ThemeResponse)
def compute_aspects(
    payload: ThemeRequest,
    mode: str = Depends(get_access_mode),
) -> ThemeResponse:
    try:
        require_trial_einstein(payload, mode)
        data = get_cached_aspects_payload(payload)

        return ThemeResponse(data=data)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul des aspects: {exc}",
        ) from exc


@router.post("/svg")
def compute_aspects_svg_route(
    payload: ThemeRequest,
    mode: str = Depends(get_access_mode),
) -> Response:
    try:
        require_trial_einstein(payload, mode)
        data = get_cached_aspects_payload(payload)

        lang = "fr"
        settings_dict = payload.settings.model_dump()
        if str(settings_dict.get("language", "fr")).lower().startswith("en"):
            lang = "en"

        svg = compute_aspects_svg(
            data,
            width=1400,
            height=900,
            language=lang,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        )
        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG des aspects: {exc}",
        ) from exc

@router.post("/svg-publication")
def compute_aspects_svg_publication_route(
    payload: ThemeRequest,
    mode: str = Depends(get_access_mode),
) -> Response:
    try:
        require_trial_einstein(payload, mode)
        data = get_cached_aspects_payload(payload)

        lang = "fr"
        settings_dict = payload.settings.model_dump()
        if str(settings_dict.get("language", "fr")).lower().startswith("en"):
            lang = "en"

        svg = compute_aspects_svg(
            data,
            width=650,
            height=650,
            language=lang,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
            inline_glyphs=True,
            show_footer=True,
            show_title=False,
        )

        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG publication des aspects: {exc}",
        ) from exc

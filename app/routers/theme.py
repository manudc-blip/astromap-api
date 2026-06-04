from fastapi import APIRouter, HTTPException, Response, Depends
from app.security import get_access_mode, require_trial_einstein
from app.services.ret_service import render_ret_svg_from_payload
from app.services.aspects_service import compute_aspects_svg
from app.services.aspects_service import compute_aspects_svg
from app.services.interpretation_service import compute_interpretation_html_from_theme_payload

from app.schemas import ThemeRequest, ThemeResponse
from app.services.theme_service import compute_theme_payload
from astromap.core.ecliptic_svg import (
    render_ecliptic_svg,
    build_ecliptic_render_layout,
)
from astromap.core.domitude_svg import render_domitude_svg
from functools import lru_cache
import json

router = APIRouter(prefix="/theme", tags=["theme"])

def _payload_cache_key(payload: ThemeRequest) -> str:
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
def _compute_theme_payload_cached(cache_key: str):
    data = json.loads(cache_key)

    return compute_theme_payload(
        name=data["name"],
        datetime_local=data["datetime_local"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        tz=data["tz"],
        settings=data["settings"],
    )


def get_cached_theme_payload(payload: ThemeRequest):
    return _compute_theme_payload_cached(_payload_cache_key(payload))

@lru_cache(maxsize=256)
def _render_domitude_svg_cached(cache_key: str, lang: str) -> str:
    data = _compute_theme_payload_cached(cache_key)

    return render_domitude_svg(
        data,
        width=1400,
        height=900,
        language=lang,
        show_title=True,
        asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
    )


def get_cached_domitude_svg(payload: ThemeRequest, lang: str) -> str:
    return _render_domitude_svg_cached(_payload_cache_key(payload), lang)

def _get_lang_from_payload(payload: ThemeRequest) -> str:
    settings_dict = payload.settings.model_dump()
    if str(settings_dict.get("language", "fr")).lower().startswith("en"):
        return "en"
    return "fr"

@router.post("/full")
def compute_theme_full(
    payload: ThemeRequest,
    mode: str = Depends(get_access_mode),
):
    require_trial_einstein(payload, mode)

    try:
        lang = _get_lang_from_payload(payload)

        theme_data = get_cached_theme_payload(payload)

        ecliptic_layout = build_ecliptic_render_layout(
            theme_data,
            width=1200,
            height=900,
            language=lang,
            show_title=True,
            show_houses=True,
            show_aspects=True,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        )

        domitude_svg = get_cached_domitude_svg(payload, lang)

settings_dict = payload.settings.model_dump()

ret_svg = render_ret_svg_from_payload(
    theme_data,
    settings=settings_dict,
)

aspects_svg = compute_aspects_svg(
    theme_data,
            width=1400,
            height=900,
            language=lang,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        )

interpretation_html = compute_interpretation_html_from_theme_payload(
    theme_data,
    settings=settings_dict,
)

        return {
            "data": theme_data,
            "ecliptic_layout": ecliptic_layout,
            "domitude_svg": domitude_svg,
            "ret_svg": ret_svg,
            "aspects_svg": aspects_svg,
            "interpretation_html": interpretation_html,
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul complet du thème: {exc}",
        ) from exc

@router.post("", response_model=ThemeResponse)
def compute_theme(payload: ThemeRequest, mode: str = Depends(get_access_mode)) -> ThemeResponse:
    require_trial_einstein(payload, mode)
    try:
        data = get_cached_theme_payload(payload)
        return ThemeResponse(data=data)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul du thème: {exc}",
        ) from exc


@router.post("/svg")
def compute_theme_svg(payload: ThemeRequest, mode: str = Depends(get_access_mode)) -> Response:
    require_trial_einstein(payload, mode)
    try:
        data = get_cached_theme_payload(payload)

        lang = "fr"
        settings_dict = payload.settings.model_dump()
        if str(settings_dict.get("language", "fr")).lower().startswith("en"):
            lang = "en"

        svg = render_ecliptic_svg(
            data,
            width=1200,
            height=900,
            language=lang,
            show_title=True,
            show_houses=True,
            show_aspects=True,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        )

        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG: {exc}",
        ) from exc


@router.post("/ecliptic-layout")
def compute_theme_ecliptic_layout(payload: ThemeRequest, mode: str = Depends(get_access_mode)):
    require_trial_einstein(payload, mode)
    try:
        data = get_cached_theme_payload(payload)

        lang = "fr"
        settings_dict = payload.settings.model_dump()
        if str(settings_dict.get("language", "fr")).lower().startswith("en"):
            lang = "en"

        layout = build_ecliptic_render_layout(
            data,
            width=1200,
            height=900,
            language=lang,
            show_title=True,
            show_houses=True,
            show_aspects=True,
            asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        )

        return layout

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération layout écliptique: {exc}",
        ) from exc


@router.post("/domitude-svg")
def compute_theme_domitude_svg(payload: ThemeRequest, mode: str = Depends(get_access_mode)) -> Response:
    require_trial_einstein(payload, mode)
    try:
        data = get_cached_theme_payload(payload)

        lang = "fr"
        settings_dict = payload.settings.model_dump()
        if str(settings_dict.get("language", "fr")).lower().startswith("en"):
            lang = "en"

        svg = get_cached_domitude_svg(payload, lang)

        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG domitude: {exc}",
        ) from exc

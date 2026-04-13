from fastapi import APIRouter, HTTPException, Response

from app.schemas import ThemeRequest, ThemeResponse
from app.services.theme_service import compute_theme_payload
from astromap.core.ecliptic_svg import render_ecliptic_svg

router = APIRouter(prefix="/theme", tags=["theme"])


@router.post("", response_model=ThemeResponse)
def compute_theme(payload: ThemeRequest) -> ThemeResponse:
    try:
        data = compute_theme_payload(
            name=payload.name or "",
            datetime_local=payload.datetime_local,
            latitude=payload.latitude,
            longitude=payload.longitude,
            tz=payload.tz,
            settings=payload.settings.model_dump(),
        )
        return ThemeResponse(data=data)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul du thème: {exc}",
        ) from exc


@router.post("/svg")
def compute_theme_svg(payload: ThemeRequest) -> Response:
    try:
        data = compute_theme_payload(
            name=payload.name or "",
            datetime_local=payload.datetime_local,
            latitude=payload.latitude,
            longitude=payload.longitude,
            tz=payload.tz,
            settings=payload.settings.model_dump(),
        )

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
            asset_base_url="/glyphes",
        )

        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG: {exc}",
        ) from exc

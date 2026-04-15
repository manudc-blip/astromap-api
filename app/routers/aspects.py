from fastapi import APIRouter, HTTPException, Response

from app.schemas import ThemeRequest, ThemeResponse
from app.services.aspects_service import compute_aspects_payload, compute_aspects_svg

router = APIRouter(prefix="/aspects", tags=["aspects"])


@router.post("", response_model=ThemeResponse)
def compute_aspects(payload: ThemeRequest) -> ThemeResponse:
    try:
        data = compute_aspects_payload(
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
            detail=f"Erreur interne lors du calcul des aspects: {exc}",
        ) from exc


@router.post("/svg")
def compute_aspects_svg_route(payload: ThemeRequest) -> Response:
    try:
        data = compute_aspects_payload(
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

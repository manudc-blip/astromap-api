from fastapi import APIRouter, HTTPException, Response

from app.schemas import ThemeRequest
from app.services.ret_service import compute_ret_svg

router = APIRouter(prefix="/ret", tags=["ret"])


@router.post("/svg")
def compute_ret_svg_route(payload: ThemeRequest) -> Response:
    try:
        svg = compute_ret_svg(
            name=payload.name or "",
            datetime_local=payload.datetime_local,
            latitude=payload.latitude,
            longitude=payload.longitude,
            tz=payload.tz,
            settings=payload.settings.model_dump(),
        )
        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG RET/HP: {exc}",
        ) from exc

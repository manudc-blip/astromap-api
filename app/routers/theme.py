from fastapi import APIRouter, HTTPException

from app.schemas import ThemeRequest, ThemeResponse
from app.services.theme_service import compute_theme_payload

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

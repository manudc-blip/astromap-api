from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from app.security import get_access_mode, require_trial_einstein

from app.schemas import ThemeRequest
from app.services.interpretation_service import (
    compute_interpretation_payload,
    compute_interpretation_html,
)

router = APIRouter(prefix="/interpretation", tags=["interpretation"])


@router.post("")
def compute_interpretation(
    payload: ThemeRequest,
    mode: str = Depends(get_access_mode),
):
    try:
        require_trial_einstein(payload, mode)
        data = compute_interpretation_payload(
            name=payload.name or "",
            datetime_local=payload.datetime_local,
            latitude=payload.latitude,
            longitude=payload.longitude,
            tz=payload.tz,
            settings=payload.settings.model_dump(),
        )
        return {"data": data}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul de l'interprétation: {exc}",
        ) from exc


@router.post("/html", response_class=HTMLResponse)
def compute_interpretation_html_route(
    payload: ThemeRequest,
    mode: str = Depends(get_access_mode),
):
    try:
        require_trial_einstein(payload, mode)
        return compute_interpretation_html(
            name=payload.name or "",
            datetime_local=payload.datetime_local,
            latitude=payload.latitude,
            longitude=payload.longitude,
            tz=payload.tz,
            settings=payload.settings.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du rendu HTML de l'interprétation: {exc}",
        ) from exc

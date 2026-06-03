from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from functools import lru_cache
import json
from app.security import get_access_mode, require_trial_einstein

from app.schemas import ThemeRequest
from app.services.interpretation_service import (
    compute_interpretation_payload,
    compute_interpretation_html,
)

router = APIRouter(prefix="/interpretation", tags=["interpretation"])

def _interpretation_cache_key(payload: ThemeRequest) -> str:
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
def _compute_interpretation_html_cached(cache_key: str) -> str:
    data = json.loads(cache_key)

    return get_cached_interpretation_html(payload)


def get_cached_interpretation_html(payload: ThemeRequest) -> str:
    return _compute_interpretation_html_cached(_interpretation_cache_key(payload))

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

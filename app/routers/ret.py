from fastapi import APIRouter, Depends, HTTPException, Response

from app.schemas import ThemeRequest
from app.services.ret_service import compute_ret_svg
from app.security import get_access_mode, require_trial_einstein
from functools import lru_cache
import json

router = APIRouter(prefix="/ret", tags=["ret"])

def _ret_cache_key(payload: ThemeRequest) -> str:
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
def _compute_ret_svg_cached(cache_key: str) -> str:
    data = json.loads(cache_key)

    return compute_ret_svg(
        name=data["name"],
        datetime_local=data["datetime_local"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        tz=data["tz"],
        settings=data["settings"],
    )


def get_cached_ret_svg(payload: ThemeRequest) -> str:
    return _compute_ret_svg_cached(_ret_cache_key(payload))

@router.post("/svg")
def compute_ret_svg_route(
    payload: ThemeRequest,
    mode: str = Depends(get_access_mode),
) -> Response:
    try:
        require_trial_einstein(payload, mode)
        svg = get_cached_ret_svg(payload)

        return Response(content=svg, media_type="image/svg+xml")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la génération SVG RET/HP: {exc}",
        ) from exc

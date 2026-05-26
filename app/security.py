import os

from fastapi import Header, HTTPException

from app.schemas import ThemeRequest


TRIAL_DATETIME_LOCAL = "1879-03-14 11:30"
TRIAL_LATITUDE = 48.3984
TRIAL_LONGITUDE = 9.9916
TRIAL_TZ = "Europe/Berlin"

COORD_TOLERANCE = 0.01


def get_access_mode(
    x_geoastro_mode: str | None = Header(default="trial"),
    x_geoastro_access_key: str | None = Header(default=None),
) -> str:
    mode = (x_geoastro_mode or "trial").lower().strip()

    if mode not in {"trial", "full"}:
        raise HTTPException(status_code=403, detail="Mode d'accès invalide.")

    if mode == "full":
        expected_key = os.getenv("GEOASTRO_FULL_ACCESS_KEY")

        if not expected_key:
            raise HTTPException(
                status_code=403,
                detail="Mode complet non configuré côté serveur.",
            )

        if x_geoastro_access_key != expected_key:
            raise HTTPException(
                status_code=403,
                detail="Mode complet non autorisé.",
            )

    return mode


def require_trial_einstein(payload: ThemeRequest, mode: str) -> None:
    if mode == "full":
        return

    if payload.datetime_local != TRIAL_DATETIME_LOCAL:
        raise HTTPException(
            status_code=403,
            detail="Mode essai : seule la date de démonstration est autorisée.",
        )

    if abs(payload.latitude - TRIAL_LATITUDE) > COORD_TOLERANCE:
        raise HTTPException(
            status_code=403,
            detail="Mode essai : latitude non autorisée.",
        )

    if abs(payload.longitude - TRIAL_LONGITUDE) > COORD_TOLERANCE:
        raise HTTPException(
            status_code=403,
            detail="Mode essai : longitude non autorisée.",
        )

    if payload.tz != TRIAL_TZ:
        raise HTTPException(
            status_code=403,
            detail="Mode essai : fuseau horaire non autorisé.",
        )

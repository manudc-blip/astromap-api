from fastapi import HTTPException, Header
from app.schemas import ThemeRequest

TRIAL_NAME = "Albert Einstein"
TRIAL_DATETIME_LOCAL = "1879-03-14 11:30"
TRIAL_LATITUDE = 48.8566
TRIAL_LONGITUDE = 2.3522
TRIAL_TZ = "Europe/Paris"

COORD_TOLERANCE = 0.01


def get_access_mode(x_geoastro_mode: str | None = Header(default="trial")) -> str:
    mode = (x_geoastro_mode or "trial").lower().strip()

    if mode not in {"trial", "full"}:
        raise HTTPException(status_code=403, detail="Mode d'accès invalide.")

    return mode


def require_trial_einstein(payload: ThemeRequest, mode: str) -> None:
    if mode == "full":
        # Temporaire : plus tard, on remplacera ceci par une vraie vérification JWT/Stripe.
        raise HTTPException(
            status_code=403,
            detail="Mode complet non disponible sans authentification serveur.",
        )

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

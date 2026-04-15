from app.services.theme_service import compute_theme_payload
from astromap.core.interpretation import build_interpretation_payload


def compute_interpretation_payload(
    *,
    name: str,
    datetime_local: str,
    latitude: float,
    longitude: float,
    tz: str,
    settings: dict,
) -> dict:
    theme_payload = compute_theme_payload(
        name=name,
        datetime_local=datetime_local,
        latitude=latitude,
        longitude=longitude,
        tz=tz,
        settings=settings,
    )

    language = "fr"
    if str(settings.get("language", "fr")).lower().startswith("en"):
        language = "en"

    return build_interpretation_payload(theme_payload, language=language)

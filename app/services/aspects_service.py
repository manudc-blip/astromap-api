from app.services.theme_service import compute_theme_payload
from astromap.core.aspects_svg import render_aspects_svg


def compute_aspects_payload(
    *,
    name: str,
    datetime_local: str,
    latitude: float,
    longitude: float,
    tz: str,
    settings: dict,
):
    return compute_theme_payload(
        name=name,
        datetime_local=datetime_local,
        latitude=latitude,
        longitude=longitude,
        tz=tz,
        settings=settings,
    )


def compute_aspects_svg(
    payload: dict,
    *,
    width: int = 1400,
    height: int = 900,
    language: str = "fr",
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    return render_aspects_svg(
        payload,
        width=width,
        height=height,
        language=language,
        asset_base_url=asset_base_url,
    )

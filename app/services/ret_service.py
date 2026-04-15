from astromap.core.ret_svg import render_ret_svg
from app.services.theme_service import compute_theme_payload


def compute_ret_svg(
    *,
    name: str,
    datetime_local: str,
    latitude: float,
    longitude: float,
    tz: str,
    settings: dict,
) -> str:
    data = compute_theme_payload(
        name=name,
        datetime_local=datetime_local,
        latitude=latitude,
        longitude=longitude,
        tz=tz,
        settings=settings,
    )

    lang = "fr"
    if str(settings.get("language", "fr")).lower().startswith("en"):
        lang = "en"

    return render_ret_svg(
        data,
        dom_payload=data,
        width=1400,
        height=900,
        language=lang,
        asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
    )

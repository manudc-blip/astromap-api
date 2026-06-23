from app.services.theme_service import compute_theme_payload
from astromap.core.ret_svg import render_ret_svg


def _get_lang(settings: dict) -> str:
    if str(settings.get("language", "fr")).lower().startswith("en"):
        return "en"
    return "fr"


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

    return render_ret_svg(
        data,
        dom_payload=data,
        width=1400,
        height=900,
        language=_get_lang(settings),
        asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        inline_glyphs=False,
        show_footer=False,
        show_title=True,
    )


def render_ret_svg_from_payload(
    data: dict,
    *,
    settings: dict,
    inline_glyphs: bool = False,
    show_footer: bool = False,
    show_title: bool = True,
    width: int = 1400,
    height: int = 900,
) -> str:
    return render_ret_svg(
        data,
        dom_payload=data,
        width=width,
        height=height,
        language=_get_lang(settings),
        asset_base_url="https://astromap-api-production.up.railway.app/glyphes",
        inline_glyphs=inline_glyphs,
        show_footer=show_footer,
        show_title=show_title,
    )

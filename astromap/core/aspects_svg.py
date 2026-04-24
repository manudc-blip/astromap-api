from __future__ import annotations

from html import escape
from typing import Any

from .aspects import detect_aspects

TITLE_COLOR = "#1f4fa3"

ASPECT_COLORS = {
    "CONJ": "#FFD27F",
    "OPP":  "#FF9999",
    "SQR":  "#FF9999",
    "TRI":  "#A6C8FF",
    "SEX":  "#A6C8FF",
}

ASPECT_SYMBOLS = {
    "CONJ": "☌",
    "OPP": "☍",
    "SQR": "□",
    "TRI": "△",
    "SEX": "✶",
}

PLANET_FILES = {
    "Soleil": "Soleil.svg",
    "Lune": "Lune.svg",
    "Mercure": "Mercure.svg",
    "Vénus": "Venus.svg",
    "Mars": "Mars.svg",
    "Jupiter": "Jupiter.svg",
    "Saturne": "Saturne.svg",
    "Uranus": "Uranus.svg",
    "Neptune": "Neptune.svg",
    "Pluton": "Pluton.svg",
    "Sun": "Soleil.svg",
    "Moon": "Lune.svg",
    "Mercury": "Mercure.svg",
    "Venus": "Venus.svg",
    "Saturn": "Saturne.svg",
    "Pluto": "Pluton.svg",
}

ASPECT_FILES = {
    "CONJ": "Conjonction.svg",
    "OPP": "Opposition.svg",
    "SQR": "Carré.svg",
    "TRI": "Trigone.svg",
    "SEX": "Sextile.svg",
}

def _fmt(v: float) -> str:
    return f"{v:.2f}"


def _svg_text(
    x,
    y,
    text,
    *,
    size=12,
    fill="#111111",
    weight="normal",
    anchor="middle",
    baseline="middle",
    family="Segoe UI, Arial, sans-serif",
) -> str:
    return (
        f'<text x="{_fmt(x)}" y="{_fmt(y)}" '
        f'font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="{baseline}">'
        f"{escape(str(text))}</text>"
    )


def _svg_line(x1, y1, x2, y2, stroke="#000", width=1) -> str:
    return (
        f'<line x1="{_fmt(x1)}" y1="{_fmt(y1)}" '
        f'x2="{_fmt(x2)}" y2="{_fmt(y2)}" '
        f'stroke="{stroke}" stroke-width="{width}" />'
    )


def _svg_rect(x, y, w, h, *, fill="none", stroke="#000", width=1) -> str:
    return (
        f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(w)}" height="{_fmt(h)}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" />'
    )


def _svg_image(href: str, x_center: float, y_center: float, size_px: float) -> str:
    half = size_px / 2.0
    return (
        f'<image href="{escape(href)}" '
        f'x="{_fmt(x_center - half)}" y="{_fmt(y_center - half)}" '
        f'width="{_fmt(size_px)}" height="{_fmt(size_px)}" '
        f'preserveAspectRatio="xMidYMid meet" />'
    )


def _planet_href(asset_base_url: str, planet_name: str) -> str | None:
    fn = PLANET_FILES.get(planet_name)
    return f"{asset_base_url}/Planetes/{fn}" if fn else None

def _aspect_href(asset_base_url: str, aspect_type: str) -> str | None:
    fn = ASPECT_FILES.get(aspect_type)
    return f"{asset_base_url}/Aspects/{fn}" if fn else None
    
def _orb_to_str(orb: float | None) -> str:
    if orb is None:
        return ""
    v = abs(float(orb))
    deg = int(v)
    minutes = int(round((v - deg) * 60))
    if minutes == 60:
        deg += 1
        minutes = 0
    return f"{deg}°{minutes:02d}'"


def _ordered_planet_names(planets: list[dict[str, Any]]) -> list[str]:
    raw = [p.get("name") for p in planets if p.get("name")]
    moon_candidates = {"Lune", "Moon"}
    sun_candidates = {"Soleil", "Sun"}

    moon_name = next((n for n in raw if n in moon_candidates), None)
    sun_name = next((n for n in raw if n in sun_candidates), None)

    rest = [n for n in raw if n not in {moon_name, sun_name}]
    out = []
    if moon_name:
        out.append(moon_name)
    if sun_name:
        out.append(sun_name)
    out.extend(rest)
    return out


def render_aspects_svg(
    payload: dict[str, Any],
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    planets: list[dict[str, Any]] = payload.get("planets", []) or []
    aspects: list[dict[str, Any]] = payload.get("aspects", []) or []

    if not planets:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
            f'<rect width="100%" height="100%" fill="#FFFFFF" />'
            f'{_svg_text(width/2, height/2, "Aucune planète", size=18, fill="#666")}'
            f"</svg>"
        )

    if not aspects:
        aspects = detect_aspects(planets)

    planet_names = _ordered_planet_names(planets)
    n = len(planet_names)

    aspect_map: dict[tuple[str, str], dict[str, Any]] = {}
    for a in aspects:
        p1 = a.get("p1")
        p2 = a.get("p2")
        if not p1 or not p2:
            continue
        if p1 not in planet_names or p2 not in planet_names:
            continue
        aspect_map[tuple(sorted((p1, p2)))] = a

    title = "Aspects planétaires" if language == "fr" else "Planetary aspects"

    top_margin = 70
    left_margin = 170
    right_margin = 20
    bottom_margin = 70

    grid_width = width - left_margin - right_margin
    grid_height = height - top_margin - bottom_margin
    grid_size = min(grid_width, grid_height)

    cell = grid_size / (n + 1)
    if cell < 25:
        cell = 25
        grid_size = cell * (n + 1)

    x0 = left_margin
    y0 = top_margin
    x_right = x0 + (n + 1) * cell
    y_bottom = y0 + (n + 1) * cell

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
        _svg_text(
            width / 2,
            24,
            title,
            size=24,
            fill=TITLE_COLOR,
            weight="700",
            baseline="hanging",
            family="Segoe UI, Arial, sans-serif",
        ),
    ]

    # Fond grille
    for k in range(n + 2):
        y_line = y0 + k * cell
        x_line = x0 + k * cell

        if k == 0 or k == n + 1:
            color = "#808080"
            line_w = 2
        elif k == 1:
            color = "#808080"
            line_w = 1.5
        else:
            color = "#d0d0d0"
            line_w = 1

        parts.append(_svg_line(x0, y_line, x_right, y_line, stroke=color, width=line_w))
        parts.append(_svg_line(x_line, y0, x_line, y_bottom, stroke=color, width=line_w))

    # Entêtes planètes
    glyph_size = cell * 0.50
    fallback_size = max(8, int(cell * 0.30))

    for idx, name in enumerate(planet_names):
        col = idx + 1
        row = idx + 1

        cx = x0 + col * cell + cell / 2
        cy = y0 + cell / 2
        href = _planet_href(asset_base_url, name)
        if href:
            parts.append(_svg_image(href, cx, cy, glyph_size))
        else:
            parts.append(_svg_text(cx, cy, name, size=fallback_size, weight="700"))

        cx = x0 + cell / 2
        cy = y0 + row * cell + cell / 2
        if href:
            parts.append(_svg_image(href, cx, cy, glyph_size))
        else:
            parts.append(_svg_text(cx, cy, name, size=fallback_size, weight="700"))

    # Diagonale
    parts.append(
        _svg_line(
            x0 + cell,
            y0 + cell,
            x0 + (n + 1) * cell,
            y0 + (n + 1) * cell,
            stroke="#c0c0c0",
            width=1,
        )
    )

    # Cases aspects
    for i, name_row in enumerate(planet_names):
        for j, name_col in enumerate(planet_names):
            if i == j:
                continue

            asp = aspect_map.get(tuple(sorted((name_row, name_col))))
            if not asp:
                continue

            kind = asp.get("type", "")
            orb = asp.get("orb")
            color = ASPECT_COLORS.get(kind, "#E0E0E0")
            symbol = ASPECT_SYMBOLS.get(kind, kind)
            orb_str = _orb_to_str(orb)

            row = i + 1
            col = j + 1

            x1 = x0 + col * cell
            y1 = y0 + row * cell
            x2 = x1 + cell
            y2 = y1 + cell

            parts.append(
                _svg_rect(
                    x1 + 1,
                    y1 + 1,
                    (x2 - x1) - 2,
                    (y2 - y1) - 2,
                    fill=color,
                    stroke="#FFFFFF",
                    width=1,
                )
            )

            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            href_a = _aspect_href(asset_base_url, kind)

            if href_a:
                parts.append(_svg_image(href_a, cx, cy - cell * 0.03, cell * 0.44))
            else:
                parts.append(
                    _svg_text(
                        cx,
                        cy - cell * 0.03,
                        symbol,
                        size=max(13, int(cell * 0.44)),
                        weight="700",
                        family="Segoe UI Symbol, Arial Unicode MS, Segoe UI, Arial, sans-serif",
                    )
                )
            
            parts.append(
                _svg_text(
                    cx,
                    cy + cell * 0.33,
                    orb_str,
                    size=max(8, int(cell * 0.17)),
                    fill="#111111",
                )
            )

    # Repassage contours
    parts.append(
        _svg_rect(
            x0,
            y0,
            (n + 1) * cell,
            (n + 1) * cell,
            fill="none",
            stroke="#808080",
            width=2,
        )
    )
    parts.append(_svg_line(x0, y0 + cell, x_right, y0 + cell, stroke="#808080", width=1.5))
    parts.append(_svg_line(x0 + cell, y0, x0 + cell, y_bottom, stroke="#808080", width=1.5))

    # Légende
    legend_y = y0 + (n + 1) * cell + 12
    if legend_y < height - 20:
        title_leg = "Légende des aspects" if language == "fr" else "Aspect legend"
        line1 = "☌ conjonction   ☍ opposition   □ carré   △ trigone   ✶ sextile" if language == "fr" else \
                "☌ conjunction   ☍ opposition   □ square   △ trine   ✶ sextile"
        line2 = "Aspects calculés en sphère locale (déclinaison réelle)" if language == "fr" else \
                "Aspects computed in local sphere (true declination)"

        parts.append(_svg_text(x0, legend_y, title_leg, size=11, weight="700", anchor="start", fill="#333333"))
        parts.append(_svg_text(x0, legend_y + 16, line1, size=10, anchor="start", fill="#444444"))
        parts.append(_svg_text(x0, legend_y + 32, line2, size=10, anchor="start", fill="#444444"))
        
    parts.append("</svg>")
    return "".join(parts)

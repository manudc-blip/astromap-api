from __future__ import annotations

import math
from html import escape
from typing import Any

from .ret_hp import compute_planet_hierarchy, compute_ret_box_colors
from .ret_families import compute_ret_ranking
from .signs_hierarchy import rank_signs


TITLE_COLOR = "#0b3d91"
TEXT_COLOR = "#111111"
GREY = "#444444"
LIGHT_GREY = "#bdbdbd"

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
}

SIGN_FILES = {
    "Bélier": "Bélier.svg",
    "Taureau": "Taureau.svg",
    "Gémeaux": "Gémeaux.svg",
    "Cancer": "Cancer.svg",
    "Lion": "Lion.svg",
    "Vierge": "Vierge.svg",
    "Balance": "Balance.svg",
    "Scorpion": "Scorpion.svg",
    "Sagittaire": "Sagittaire.svg",
    "Capricorne": "Capricorne.svg",
    "Verseau": "Verseau.svg",
    "Poissons": "Poissons.svg",
}

RET_STYLE = {
    "p": {"shape": "circle", "fill": "#FFFFFF", "stroke": "#000000", "label": "p", "legend": "pouvoir intensif"},
    "E": {"shape": "diamond", "fill": "#FF4A3A", "stroke": "#000000", "label": "E", "legend": "Existence extensive"},
    "t": {"shape": "circle", "fill": "#1E88E5", "stroke": "#000000", "label": "t", "legend": "transcendance intensive"},
    "e": {"shape": "circle", "fill": "#FF4336", "stroke": "#000000", "label": "e", "legend": "existence intensive"},
    "R": {"shape": "diamond", "fill": "#FFD200", "stroke": "#000000", "label": "R", "legend": "Représentation extensive"},
    "r": {"shape": "circle", "fill": "#FFD200", "stroke": "#000000", "label": "r", "legend": "représentation intensive"},
    "P": {"shape": "diamond", "fill": "#444444", "stroke": "#000000", "label": "P", "legend": "Pouvoir extensif"},
    "T": {"shape": "diamond", "fill": "#1E88E5", "stroke": "#000000", "label": "T", "legend": "Transcendance extensive"},
}


def _fmt(v: float) -> str:
    return f"{v:.2f}"


def _svg_text(
    x,
    y,
    text,
    *,
    size=12,
    fill=TEXT_COLOR,
    weight="normal",
    anchor="middle",
    baseline="middle",
    family="Segoe UI, Arial, sans-serif",
) -> str:
    return (
        f'<text x="{_fmt(x)}" y="{_fmt(y)}" '
        f'font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="{baseline}">'
        f'{escape(str(text))}</text>'
    )


def _svg_line(x1, y1, x2, y2, *, stroke="#000", width=1) -> str:
    return (
        f'<line x1="{_fmt(x1)}" y1="{_fmt(y1)}" x2="{_fmt(x2)}" y2="{_fmt(y2)}" '
        f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" />'
    )


def _svg_rect(x, y, w, h, *, fill="#fff", stroke="#000", width=1) -> str:
    return (
        f'<rect x="{_fmt(x)}" y="{_fmt(y)}" width="{_fmt(w)}" height="{_fmt(h)}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" />'
    )


def _svg_circle(cx, cy, r, *, fill="#fff", stroke="#000", width=1) -> str:
    return (
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" />'
    )


def _svg_diamond(cx, cy, size, *, fill="#fff", stroke="#000", width=1) -> str:
    pts = [
        (cx, cy - size),
        (cx + size, cy),
        (cx, cy + size),
        (cx - size, cy),
    ]
    pts_str = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)
    return f'<polygon points="{pts_str}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" />'


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


def _sign_href(asset_base_url: str, sign_name: str) -> str | None:
    fn = SIGN_FILES.get(sign_name)
    return f"{asset_base_url}/Signes/{fn}" if fn else None


def _extract_angular_set(theme_payload: dict[str, Any]) -> set[str]:
    out = set()
    for item in theme_payload.get("domitudes", []) or []:
        if item.get("est_angulaire"):
            name = item.get("planete")
            if name:
                out.add(name)
    return out


def _planet_sign_map(theme_payload: dict[str, Any]) -> dict[str, str]:
    out = {}
    for p in theme_payload.get("planets", []) or []:
        name = p.get("name")
        sign = p.get("sign")
        if name and sign:
            out[name] = sign
    return out


def _shape_for_ret_family(cx: float, cy: float, fam: str, size: float) -> str:
    style = RET_STYLE[fam]
    if style["shape"] == "circle":
        return _svg_circle(cx, cy, size * 0.58, fill=style["fill"], stroke=style["stroke"], width=1)
    return _svg_diamond(cx, cy, size, fill=style["fill"], stroke=style["stroke"], width=1)


def render_ret_svg(
    theme_payload: dict[str, Any],
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    ranks, ordered_planets, info = compute_planet_hierarchy(theme_payload, theme_payload)
    ret_order, ret_details = compute_ret_ranking(ranks)
    sign_ranked = rank_signs(theme_payload.get("planets", []), ranks)
    angular_set = _extract_angular_set(theme_payload)
    box_colors = compute_ret_box_colors(ordered_planets, angular_set, theme_payload.get("aspects", []) or [])
    sign_map = _planet_sign_map(theme_payload)

    title = "RET et Hiérarchie Planétaire" if language == "fr" else "RET and Planetary Hierarchy"

    w = width
    h = height
    cx = w * 0.50
    cy = h * 0.42

    left_x_rank = w * 0.10
    left_x_planet = w * 0.14
    left_x_shape = w * 0.19
    left_x_sign = w * 0.24
    left_y0 = h * 0.22
    left_dy = h * 0.062

    right_x_num = w * 0.74
    right_x_shape = w * 0.77
    right_x_label = w * 0.81
    right_y0 = h * 0.23
    right_dy = h * 0.060

    planet_px = 34
    sign_px = 20
    small_shape = 19

    tile = 46
    gap = tile * 0.98

    # placement losange central
    positions = {
        0: (cx, cy - 2 * gap),          # top
        1: (cx - gap, cy - gap),        # upper-left
        2: (cx, cy - gap),              # upper-mid
        3: (cx + gap, cy - gap),        # upper-right
        4: (cx - 1.5 * gap, cy),        # left-top
        5: (cx - 0.5 * gap, cy),        # left-mid
        6: (cx + 0.5 * gap, cy),        # right-mid
        7: (cx, cy + gap),              # bottom
    }

    family_to_planets = {
        "p": ["Lune"],
        "R": ["Soleil", "Vénus", "Mercure"],
        "E": ["Jupiter", "Mars", "Saturne"],
        "T": ["Uranus", "Neptune", "Pluton"],
        "r": ["Soleil", "Jupiter", "Uranus"],
        "e": ["Vénus", "Mars", "Neptune"],
        "t": ["Mercure", "Saturne", "Pluton"],
        "P": ["Soleil", "Mars", "Pluton"],
    }

    def top_planet_for_family(fam: str) -> str | None:
        candidates = family_to_planets.get(fam, [])
        ranked = [p for p in ordered_planets if p in candidates]
        return ranked[0] if ranked else (candidates[0] if candidates else None)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
        _svg_text(w / 2, 28, title, size=18, fill=TITLE_COLOR, weight="700", baseline="hanging"),
    ]

    # colonne gauche : classement planétaire
    for i, planet in enumerate(ordered_planets[:10], start=1):
        y = left_y0 + (i - 1) * left_dy

        parts.append(_svg_text(left_x_rank, y, f"{i}.", size=14, weight="700"))
        href_p = _planet_href(asset_base_url, planet)
        if href_p:
            parts.append(_svg_image(href_p, left_x_planet, y, planet_px))
        else:
            parts.append(_svg_text(left_x_planet, y, planet[:1], size=18, weight="700"))

        # case RET colorée
        fill = box_colors.get(planet, "white")
        fill_map = {"black": "#000000", "gray": "#9E9E9E", "white": "#FFFFFF"}
        stroke_map = {"black": "#000000", "gray": "#000000", "white": "#777777"}

        parts.append(_svg_diamond(left_x_shape, y, small_shape, fill=fill_map[fill], stroke=stroke_map[fill], width=1))

        # famille RET dominante de la planète (première famille qui la contient)
        fam_for_planet = None
        for fam in ret_order:
            if planet in family_to_planets.get(fam, []):
                fam_for_planet = fam
                break

        if fam_for_planet:
            style = RET_STYLE[fam_for_planet]
            if style["shape"] == "circle":
                parts.append(_svg_circle(left_x_shape, y, small_shape * 0.50, fill=style["fill"], stroke=style["stroke"], width=1))
            else:
                parts.append(_svg_diamond(left_x_shape, y, small_shape * 0.78, fill=style["fill"], stroke=style["stroke"], width=1))

        sign_name = sign_map.get(planet)
        href_s = _sign_href(asset_base_url, sign_name) if sign_name else None
        if href_s:
            parts.append(_svg_image(href_s, left_x_sign, y, sign_px))

    # losange central RET
    for idx, fam in enumerate(ret_order[:8]):
        x, y = positions[idx]
        parts.append(_shape_for_ret_family(x, y, fam, tile))

        # glyphe principal de la famille
        p = top_planet_for_family(fam)
        href = _planet_href(asset_base_url, p) if p else None

        # texte noir/blanc selon fond
        fill = RET_STYLE[fam]["fill"]
        dark_bg = fill in {"#000000", "#444444", "#1E88E5"}
        txt_color = "#FFFFFF" if dark_bg else "#000000"

        if href:
            parts.append(_svg_image(href, x, y, 40))
        else:
            parts.append(_svg_text(x, y, RET_STYLE[fam]["label"], size=22, weight="700", fill=txt_color))

    # petites lettres autour du losange
    parts.append(_svg_text(cx, cy - 2 * gap - 58, "p", size=14, weight="700"))
    parts.append(_svg_text(cx - 1.55 * gap, cy - 0.45 * gap, "T", size=14, weight="700", anchor="end"))
    parts.append(_svg_text(cx - 0.85 * gap, cy - 1.18 * gap, "E", size=14, weight="700", anchor="end"))
    parts.append(_svg_text(cx - 0.15 * gap, cy - 1.75 * gap, "R", size=14, weight="700", anchor="end"))
    parts.append(_svg_text(cx + 0.15 * gap, cy - 1.75 * gap, "r", size=14, weight="700", anchor="start"))
    parts.append(_svg_text(cx + 0.95 * gap, cy - 1.18 * gap, "e", size=14, weight="700", anchor="start"))
    parts.append(_svg_text(cx + 1.55 * gap, cy - 0.45 * gap, "t", size=14, weight="700", anchor="start"))
    parts.append(_svg_text(cx, cy + 1.78 * gap, "P", size=14, weight="700"))

    # colonne droite : légende RET
    for i, fam in enumerate(ret_order[:8], start=1):
        y = right_y0 + (i - 1) * right_dy
        style = RET_STYLE[fam]

        parts.append(_svg_text(right_x_num, y, f"{i}.", size=14, weight="700"))

        if style["shape"] == "circle":
            parts.append(_svg_circle(right_x_shape, y, 11, fill=style["fill"], stroke=style["stroke"], width=1))
        else:
            parts.append(_svg_diamond(right_x_shape, y, 19, fill=style["fill"], stroke=style["stroke"], width=1))

        label = style["label"]
        legend = style["legend"]
        parts.append(
            _svg_text(
                right_x_label,
                y,
                f"{label} ({legend})",
                size=12,
                weight="700",
                anchor="start",
            )
        )

    # bas gauche : dominantes
    dom_planets = ordered_planets[:4]
    dom_signs = [name for name, _score in sign_ranked[:3]]

    y_dom1 = h * 0.86
    y_dom2 = h * 0.91
    x_dom_label = w * 0.10
    x_dom_start = w * 0.23

    parts.append(_svg_text(x_dom_label, y_dom1, "Planètes dominantes :", size=13, weight="700", anchor="start"))
    for j, p in enumerate(dom_planets):
        href = _planet_href(asset_base_url, p)
        x = x_dom_start + j * 36
        if href:
            parts.append(_svg_image(href, x, y_dom1, 28))

    parts.append(_svg_text(x_dom_label, y_dom2, "Signes dominants :", size=13, weight="700", anchor="start"))
    for j, s in enumerate(dom_signs):
        href = _sign_href(asset_base_url, s)
        x = x_dom_start + j * 36
        if href:
            parts.append(_svg_image(href, x, y_dom2, 28))

    parts.append("</svg>")
    return "".join(parts)

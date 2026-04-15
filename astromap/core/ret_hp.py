from __future__ import annotations

from html import escape
from typing import Any

from .ret_families import compute_ret_ranking
from .signs_hierarchy import rank_signs


TITLE_COLOR = "#0b3d91"
TEXT_COLOR = "#111111"
BLACK = "#000000"
MID_GREY = "#BDBDBD"
DARK_GREY = "#444444"

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

# Style de légende RET, fidèle au Tkinter
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


def _draw_box_with_inner_symbol(cx: float, cy: float, box_size: float, box_fill: str, inner_family: str | None) -> str:
    parts: list[str] = []

    # fond de case "boîte"
    if box_fill == "black":
        parts.append(_svg_diamond(cx, cy, box_size, fill="#000000", stroke="#000000", width=1))
    elif box_fill == "gray":
        parts.append(_svg_diamond(cx, cy, box_size, fill=MID_GREY, stroke="#000000", width=1))
    else:
        parts.append(_svg_diamond(cx, cy, box_size, fill="#FFFFFF", stroke="#777777", width=1))

    # forme interne éventuelle
    if inner_family:
        style = RET_STYLE[inner_family]
        if style["shape"] == "circle":
            parts.append(_svg_circle(cx, cy, box_size * 0.52, fill=style["fill"], stroke=style["stroke"], width=1))
        else:
            parts.append(_svg_diamond(cx, cy, box_size * 0.78, fill=style["fill"], stroke=style["stroke"], width=1))

    return "".join(parts)


def _ret_family_for_planet(planet: str, ret_order: list[str], family_to_planets: dict[str, list[str]]) -> str | None:
    for fam in ret_order:
        if planet in family_to_planets.get(fam, []):
            return fam
    return None


def _top_planet_for_family(fam: str, ordered_planets: list[str], family_to_planets: dict[str, list[str]]) -> str | None:
    candidates = family_to_planets.get(fam, [])
    ranked = [p for p in ordered_planets if p in candidates]
    return ranked[0] if ranked else (candidates[0] if candidates else None)


def render_ret_svg(
    theme_payload: dict[str, Any],
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    ranks, ordered_planets, _info = compute_planet_hierarchy(theme_payload, theme_payload)
    ret_order, _ret_details = compute_ret_ranking(ranks)
    sign_ranked = rank_signs(theme_payload.get("planets", []), ranks)
    angular_set = _extract_angular_set(theme_payload)
    box_colors = compute_ret_box_colors(ordered_planets, angular_set, theme_payload.get("aspects", []) or [])
    sign_map = _planet_sign_map(theme_payload)

    title = "RET et Hiérarchie Planétaire" if language == "fr" else "RET and Planetary Hierarchy"

    w = width
    h = height

    # géométrie générale proche Tkinter
    left_x_rank = 110
    left_x_planet = 155
    left_x_shape = 225
    left_x_sign = 285
    left_y0 = 225
    left_dy = 56

    center_x = 610
    center_y = 390
    tile = 46
    gap = 45

    right_x_num = 890
    right_x_shape = 930
    right_x_text = 975
    right_y0 = 230
    right_dy = 48

    dom_label_x = 110
    dom_icons_x = 285
    dom_planets_y = 735
    dom_signs_y = 775

    planet_px_left = 36
    sign_px_left = 20
    planet_px_center = 48
    small_shape = 19
    dom_icon_px = 34

    # Familles RET vers planètes
    family_to_planets = {
        "p": ["Lune"],
        "E": ["Jupiter", "Mars", "Saturne"],
        "t": ["Mercure", "Saturne", "Pluton"],
        "e": ["Vénus", "Mars", "Neptune"],
        "R": ["Soleil", "Vénus", "Mercure"],
        "r": ["Soleil", "Jupiter", "Uranus"],
        "P": ["Soleil", "Mars", "Pluton"],
        "T": ["Uranus", "Neptune", "Pluton"],
    }

    # Cases fixes du losange central, comme le Tkinter
    pos = {
        0: (center_x, center_y - 3 * gap),   # sommet
        1: (center_x, center_y - 2 * gap),   # ligne 2 centre
        2: (center_x - gap, center_y - gap), # ligne 3 gauche
        3: (center_x + gap, center_y - gap), # ligne 3 droite
        4: (center_x - 2 * gap, center_y),   # ligne 4 gauche
        5: (center_x, center_y),             # ligne 4 centre
        6: (center_x + 2 * gap, center_y),   # ligne 4 droite
        7: (center_x - gap, center_y + gap), # ligne 5 gauche
        8: (center_x + gap, center_y + gap), # ligne 5 droite
        9: (center_x, center_y + 2 * gap),   # bas
    }

    # lettres autour du losange, positionnées comme le Tkinter
    edge_labels = [
        ("p", center_x, center_y - 3 * gap - 36),
        ("R", center_x - 32, center_y - 2 * gap - 12),
        ("r", center_x + 34, center_y - 2 * gap - 12),
        ("E", center_x - gap - 32, center_y - gap - 18),
        ("e", center_x + gap + 34, center_y - gap - 18),
        ("T", center_x - 2 * gap - 28, center_y + 3),
        ("t", center_x + 2 * gap + 28, center_y + 3),
        ("P", center_x, center_y + 2 * gap + 38),
    ]

    # Structure fidèle du losange Tkinter :
    # 0 sommet = famille 1 seule
    # 1 = planète 1 sur blanc
    # 2-3 = planètes 2-3
    # 4-5-6 = planètes 4-5-6
    # 7-8 = planètes 7-8
    # 9 = planète 9 sur blanc
    # la 10e planète reste dans la colonne gauche, pas dans le losange
    center_planets = ordered_planets[:9]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
        _svg_text(w / 2, 28, title, size=18, fill=TITLE_COLOR, weight="700", baseline="hanging"),
    ]

    # Colonne gauche
    for i, planet in enumerate(ordered_planets[:10], start=1):
        y = left_y0 + (i - 1) * left_dy
        parts.append(_svg_text(left_x_rank, y, f"{i}.", size=14, weight="700"))

        href_p = _planet_href(asset_base_url, planet)
        if href_p:
            parts.append(_svg_image(href_p, left_x_planet, y, planet_px_left))
        else:
            parts.append(_svg_text(left_x_planet, y, planet[:1], size=22, weight="700"))

        fam = _ret_family_for_planet(planet, ret_order, family_to_planets)
        box_fill = box_colors.get(planet, "white")
        parts.append(_draw_box_with_inner_symbol(left_x_shape, y, small_shape, box_fill, fam))

        sign_name = sign_map.get(planet)
        href_s = _sign_href(asset_base_url, sign_name) if sign_name else None
        if href_s:
            parts.append(_svg_image(href_s, left_x_sign, y, sign_px_left))

    # Losange RET central
    # Sommet : famille 1 seule
    if ret_order:
        fam0 = ret_order[0]
        x, y = pos[0]
        style = RET_STYLE[fam0]
        if style["shape"] == "circle":
            parts.append(_svg_circle(x, y, tile * 0.58, fill=style["fill"], stroke=style["stroke"], width=1))
        else:
            parts.append(_svg_diamond(x, y, tile, fill=style["fill"], stroke=style["stroke"], width=1))

        p = _top_planet_for_family(fam0, ordered_planets, family_to_planets)
        href = _planet_href(asset_base_url, p) if p else None
        if href:
            parts.append(_svg_image(href, x, y, planet_px_center))

    # Cases planétaires fixes 1..9
    center_slots = [
        (1, center_planets[0] if len(center_planets) > 0 else None),
        (2, center_planets[1] if len(center_planets) > 1 else None),
        (3, center_planets[2] if len(center_planets) > 2 else None),
        (4, center_planets[3] if len(center_planets) > 3 else None),
        (5, center_planets[4] if len(center_planets) > 4 else None),
        (6, center_planets[5] if len(center_planets) > 5 else None),
        (7, center_planets[6] if len(center_planets) > 6 else None),
        (8, center_planets[7] if len(center_planets) > 7 else None),
        (9, center_planets[8] if len(center_planets) > 8 else None),
    ]

    for slot_idx, planet in center_slots:
        if not planet:
            continue
        x, y = pos[slot_idx]
        fam = _ret_family_for_planet(planet, ret_order, family_to_planets)
        box_fill = box_colors.get(planet, "white")
        parts.append(_draw_box_with_inner_symbol(x, y, tile, box_fill, fam))

        href = _planet_href(asset_base_url, planet)
        if href:
            parts.append(_svg_image(href, x, y, planet_px_center))
        else:
            parts.append(_svg_text(x, y, planet[:1], size=24, weight="700"))

    # Lettres RET autour du losange
    for txt, x, y in edge_labels:
        parts.append(_svg_text(x, y, txt, size=14, weight="700"))

    # Légende droite
    for i, fam in enumerate(ret_order[:8], start=1):
        y = right_y0 + (i - 1) * right_dy
        style = RET_STYLE[fam]

        parts.append(_svg_text(right_x_num, y, f"{i}.", size=14, weight="700"))

        if style["shape"] == "circle":
            parts.append(_svg_circle(right_x_shape, y, 11, fill=style["fill"], stroke=style["stroke"], width=1))
        else:
            parts.append(_svg_diamond(right_x_shape, y, 19, fill=style["fill"], stroke=style["stroke"], width=1))

        parts.append(
            _svg_text(
                right_x_text,
                y,
                f'{style["label"]} ({style["legend"]})',
                size=12,
                weight="700",
                anchor="start",
            )
        )

    # Dominantes
    dom_planets = ordered_planets[:4]
    dom_signs = [name for name, _score in sign_ranked[:3]]

    parts.append(_svg_text(dom_label_x, dom_planets_y, "Planètes dominantes :", size=13, weight="700", anchor="start"))
    for j, p in enumerate(dom_planets):
        href = _planet_href(asset_base_url, p)
        x = dom_icons_x + j * 32
        if href:
            parts.append(_svg_image(href, x, dom_planets_y, dom_icon_px))

    parts.append(_svg_text(dom_label_x, dom_signs_y, "Signes dominants :", size=13, weight="700", anchor="start"))
    for j, s in enumerate(dom_signs):
        href = _sign_href(asset_base_url, s)
        x = dom_icons_x + j * 32
        if href:
            parts.append(_svg_image(href, x, dom_signs_y, dom_icon_px))

    parts.append("</svg>")
    return "".join(parts)

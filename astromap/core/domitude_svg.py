from __future__ import annotations

import math
from html import escape
from typing import Any


STRUCT_GREY = "#4A4A4A"
TITLE_COLOR = "#1f4fa3"
HOUSE_MARK_COLOR = "#0b3d91"

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

AXIS_FILES_FR = {
    "AS": "AS.svg",
    "DS": "DS.svg",
    "MC": "MC.svg",
    "FC": "FC.svg",
}

AXIS_FILES_EN = {
    "AS": "AS.svg",
    "DS": "DS.svg",
    "MC": "MC.svg",
    "FC": "IC.svg",
}

# petits glyphes de signes autour du cercle domitude
SIGN_DOMITUDE_FILES = {
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

ROMAN_HOUSES = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    11: "XI",
    12: "XII",
}


def _fmt(v: float) -> str:
    return f"{v:.2f}"


def _svg_line(x1, y1, x2, y2, stroke="#000", width=1, dash=None, linecap="round") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{_fmt(x1)}" y1="{_fmt(y1)}" '
        f'x2="{_fmt(x2)}" y2="{_fmt(y2)}" '
        f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="{linecap}"{dash_attr} />'
    )


def _svg_circle(cx, cy, r, stroke="#000", width=1, fill="none") -> str:
    return (
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" '
        f'stroke="{stroke}" stroke-width="{width}" fill="{fill}" />'
    )


def _svg_text(
    x,
    y,
    text,
    *,
    size=12,
    fill="#000",
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


def _svg_image(href: str, x_center: float, y_center: float, size_px: float) -> str:
    half = size_px / 2.0
    return (
        f'<image href="{escape(href)}" '
        f'x="{_fmt(x_center - half)}" y="{_fmt(y_center - half)}" '
        f'width="{_fmt(size_px)}" height="{_fmt(size_px)}" '
        f'preserveAspectRatio="xMidYMid meet" />'
    )


def _svg_polyline(points, stroke="#000", width=1, fill="none", dash=None, linecap="round", linejoin="round") -> str:
    pts = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-linecap="{linecap}" stroke-linejoin="{linejoin}"{dash_attr} />'
    )


def _arc_points(cx: float, cy: float, r: float, start_deg: float, extent_deg: float, steps: int = 48):
    pts = []
    steps = max(steps, 2)
    for i in range(steps + 1):
        t = i / steps
        a = start_deg + extent_deg * t
        th = math.radians(a)
        x = cx + r * math.cos(th)
        y = cy - r * math.sin(th)
        pts.append((x, y))
    return pts


def _polar_to_xy(cx: float, cy: float, angle_deg: float, radius: float) -> tuple[float, float]:
    th = math.radians(angle_deg)
    return cx + radius * math.cos(th), cy - radius * math.sin(th)


def _angle_from_domitude(dom_deg: float) -> float:
    """
    0° domitude = MC (vertical haut), sens horaire.
    Pour notre repère écran basé sur cos/sin :
    angle écran = 90 - domitude
    """
    return 90.0 - dom_deg


def _planet_href(asset_base_url: str, planet_name: str) -> str | None:
    filename = PLANET_FILES.get(planet_name)
    if not filename:
        return None
    return f"{asset_base_url}/Planetes/{filename}"


def _sign_domitude_href(asset_base_url: str, sign_name: str) -> str | None:
    filename = SIGN_DOMITUDE_FILES.get(sign_name)
    if not filename:
        return None
    return f"{asset_base_url}/Signes_domitude/{filename}"


def _axis_href(asset_base_url: str, axis_label: str, language: str) -> str | None:
    files = AXIS_FILES_EN if language == "en" else AXIS_FILES_FR
    filename = files.get(axis_label)
    if not filename:
        return None
    return f"{asset_base_url}/Axes/{filename}"


def _house_mid_domitude(house_num: int) -> float:
    """
    Convention de domitude :
    0 = cuspide X, 30 = XI, 60 = XII, 90 = I, ...
    Milieux des maisons :
      X=15, XI=45, XII=75, I=105, II=135, III=165,
      IV=195, V=225, VI=255, VII=285, VIII=315, IX=345
    """
    mapping = {
        10: 15.0,
        11: 45.0,
        12: 75.0,
        1: 105.0,
        2: 135.0,
        3: 165.0,
        4: 195.0,
        5: 225.0,
        6: 255.0,
        7: 285.0,
        8: 315.0,
        9: 345.0,
    }
    return mapping[house_num]


def _pack_close_angles(items: list[dict[str, Any]], threshold_deg: float = 8.0) -> list[list[dict[str, Any]]]:
    if not items:
        return []

    ordered = sorted(items, key=lambda x: x["domitude_deg"])
    groups: list[list[dict[str, Any]]] = [[ordered[0]]]

    for item in ordered[1:]:
        prev = groups[-1][-1]
        if abs(item["domitude_deg"] - prev["domitude_deg"]) <= threshold_deg:
            groups[-1].append(item)
        else:
            groups.append([item])

    return groups


def render_domitude_svg(
    payload: dict[str, Any],
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    title_suffix: str = "",
    show_title: bool = True,
    asset_base_url: str = "/glyphes",
) -> str:
    domitudes = payload.get("domitudes") or []
    sign_domitudes = payload.get("sign_domitudes") or []

    title_base = "Thème de domitude" if language != "en" else "Domitude chart"
    title = title_base + (title_suffix or "")

    cx = width * 0.56
    cy = height * 0.49

    r_outer = 225.0
    r_outer_tick_ring = 220.0
    r_house_outer = 214.0
    r_house_inner = 145.0
    r_inner_tick_ring = 151.0
    r_void = 143.0

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
    ]

    if show_title:
        parts.append(
            _svg_text(
                cx,
                28,
                title,
                size=28,
                fill=TITLE_COLOR,
                weight="700",
                baseline="hanging",
            )
        )

    # deux cercles de graduations + deux bords principaux
    parts.append(_svg_circle(cx, cy, r_outer_tick_ring, stroke="#CFCFCF", width=1.0))
    parts.append(_svg_circle(cx, cy, r_house_outer, stroke=STRUCT_GREY, width=2.8))
    parts.append(_svg_circle(cx, cy, r_inner_tick_ring, stroke="#CFCFCF", width=1.0))
    parts.append(_svg_circle(cx, cy, r_house_inner, stroke=STRUCT_GREY, width=2.8))
    parts.append(_svg_circle(cx, cy, r_void, stroke="#EFEFEF", width=1.0))

    # graduations double bande tous les 5°
    for deg in range(0, 360, 5):
        angle = _angle_from_domitude(float(deg))

        is_30 = (deg % 30 == 0)
        is_10 = (deg % 10 == 0)

        # bande extérieure
        outer_len = 10 if is_30 else 7 if is_10 else 4
        x1, y1 = _polar_to_xy(cx, cy, angle, r_outer_tick_ring)
        x2, y2 = _polar_to_xy(cx, cy, angle, r_outer_tick_ring - outer_len)
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#B8B8B8", width=1.0))

        # bande intérieure
        inner_len = 10 if is_30 else 7 if is_10 else 4
        x3, y3 = _polar_to_xy(cx, cy, angle, r_inner_tick_ring)
        x4, y4 = _polar_to_xy(cx, cy, angle, r_inner_tick_ring + inner_len)
        parts.append(_svg_line(x3, y3, x4, y4, stroke="#B8B8B8", width=1.0))

    # 12 secteurs de maison
    for dom_deg in range(0, 360, 30):
        angle = _angle_from_domitude(float(dom_deg))
        x1, y1 = _polar_to_xy(cx, cy, angle, r_house_inner)
        x2, y2 = _polar_to_xy(cx, cy, angle, r_house_outer)
        parts.append(_svg_line(x1, y1, x2, y2, stroke=STRUCT_GREY, width=2.8))

    # numéros de maisons
    house_order = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for house_num in house_order:
        dom_mid = _house_mid_domitude(house_num)
        angle = _angle_from_domitude(dom_mid)
        tx, ty = _polar_to_xy(cx, cy, angle, (r_house_inner + r_house_outer) / 2.0)
        parts.append(
            _svg_text(
                tx,
                ty,
                ROMAN_HOUSES[house_num],
                size=26,
                fill=STRUCT_GREY,
                weight="400",
            )
        )

    # petits signes de domitude autour du cercle
    for item in sign_domitudes:
        sign_name = item.get("signe")
        dom_deg = float(item.get("domitude_deg", 0.0))
        angle = _angle_from_domitude(dom_deg)
        sx, sy = _polar_to_xy(cx, cy, angle, r_outer_tick_ring + 9.0)

        href = _sign_domitude_href(asset_base_url, sign_name)
        if href:
            parts.append(_svg_image(href, sx, sy, 18))
        else:
            parts.append(_svg_text(sx, sy, sign_name, size=10, fill="#666666"))

    # axes
    axis_line_width = 4.0
    axis_glyph_px = 34.0

    axes = {
        "MC": {
            "line": ((cx, cy), (cx, cy - 330)),
            "glyph_center": (cx, cy - 352),
            "deco": ("circle", cx, cy - 352, 20),
        },
        "FC": {
            "line": ((cx, cy), (cx, cy + 330)),
            "glyph_center": (cx, cy + 352),
            "deco": ("half_circle", cx, cy + 352, 20, 180, 180),
        },
        "AS": {
            "line": ((cx, cy), (cx - 365, cy)),
            "glyph_center": (cx - 392, cy),
            "deco": ("arrow_left", cx - 390, cy),
        },
        "DS": {
            "line": ((cx, cy), (cx + 365, cy)),
            "glyph_center": (cx + 392, cy),
            "deco": ("crossbar", cx + 392, cy, 18),
        },
    }

    for label, cfg in axes.items():
        (x1, y1), (x2, y2) = cfg["line"]
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#222222", width=axis_line_width))

        deco = cfg["deco"]
        if deco[0] == "arrow_left":
            tipx, tipy = deco[1], deco[2]
            parts.append(_svg_line(tipx, tipy, tipx + 28, tipy - 14, stroke="#222222", width=axis_line_width))
            parts.append(_svg_line(tipx, tipy, tipx + 28, tipy + 14, stroke="#222222", width=axis_line_width))
        elif deco[0] == "crossbar":
            cx_bar, cy_bar, rr = deco[1], deco[2], deco[3]
            parts.append(_svg_line(cx_bar, cy_bar - rr, cx_bar, cy_bar + rr, stroke="#222222", width=axis_line_width))
        elif deco[0] == "circle":
            parts.append(_svg_circle(deco[1], deco[2], deco[3], stroke="#222222", width=axis_line_width))
        elif deco[0] == "half_circle":
            pts = _arc_points(deco[1], deco[2], deco[3], deco[4], deco[5], 24)
            parts.append(_svg_polyline(pts, stroke="#222222", width=axis_line_width, fill="none"))

        href = _axis_href(asset_base_url, label, language)
        gx, gy = cfg["glyph_center"]
        if href:
            parts.append(_svg_image(href, gx, gy, axis_glyph_px))
        else:
            txt = "IC" if (language == "en" and label == "FC") else label
            parts.append(_svg_text(gx, gy, txt, size=18, fill=TITLE_COLOR, weight="700"))

    # placement des planètes avec petits décalages pour amas
    groups = _pack_close_angles(domitudes, threshold_deg=8.0)

    placed: list[dict[str, Any]] = []
    for group in groups:
        n = len(group)
        for idx, item in enumerate(group):
            # décalage radial progressif pour éviter la superposition
            radial_offset = 0.0 + idx * 21.0
            angle_shift = 0.0
            if n >= 2:
                angle_shift = (idx - (n - 1) / 2.0) * 1.7

            dom_deg = float(item.get("domitude_deg", 0.0))
            angle = _angle_from_domitude(dom_deg + angle_shift)

            x0, y0 = _polar_to_xy(cx, cy, angle, r_house_outer)
            x1, y1 = _polar_to_xy(cx, cy, angle, r_house_outer + 18.0)
            x2, y2 = _polar_to_xy(cx, cy, angle, r_house_outer + 36.0 + radial_offset)

            placed.append(
                {
                    "item": item,
                    "angle": angle,
                    "anchor": (x0, y0),
                    "bend": (x1, y1),
                    "glyph": (x2, y2),
                    "glyph_px": 34.0,
                }
            )

    # dessiner planètes + connecteurs + degrés
    for p in placed:
        item = p["item"]
        planet_name = item.get("planete", "")
        deg_val = int(round(float(item.get("pos_maison_deg", 0.0))))
        x0, y0 = p["anchor"]
        x1, y1 = p["bend"]
        xg, yg = p["glyph"]

        parts.append(_svg_line(x0, y0, x1, y1, stroke=STRUCT_GREY, width=2.0))
        parts.append(_svg_line(x1, y1, xg, yg, stroke=STRUCT_GREY, width=2.0))

        href = _planet_href(asset_base_url, planet_name)
        if href:
            parts.append(_svg_image(href, xg, yg, p["glyph_px"]))
        else:
            parts.append(_svg_text(xg, yg, planet_name, size=12, fill="#000000"))

        # degré près du glyphe
        tx, ty = _polar_to_xy(cx, cy, p["angle"], r_house_outer + 58.0 + 8.0)
        parts.append(_svg_text(tx, ty, str(deg_val), size=14, fill="#000000"))

    parts.append("</svg>")
    return "".join(parts)

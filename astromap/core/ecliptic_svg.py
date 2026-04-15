from __future__ import annotations

import math
from html import escape
from typing import Any

from .ecliptic_layout import build_ecliptic_layout


STRUCT_GREY = "#4A4A4A"
TITLE_COLOR = "#1f4fa3"
HOUSE_MARK_COLOR = "#0b3d91"
ASPECT_BLUE = "#0077CC"
ASPECT_RED = "#D62828"
ASPECT_VIOLET = "#A855F7"

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
    "FC": "IC.svg",  # important : fond du ciel -> IC en anglais
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


def _svg_polyline(points, stroke="#000", width=1, fill="none", dash=None, linecap="round", linejoin="round") -> str:
    pts = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-linecap="{linecap}" stroke-linejoin="{linejoin}"{dash_attr} />'
    )


def _svg_image(href: str, x_center: float, y_center: float, size_px: float) -> str:
    half = size_px / 2.0
    return (
        f'<image href="{escape(href)}" '
        f'x="{_fmt(x_center - half)}" y="{_fmt(y_center - half)}" '
        f'width="{_fmt(size_px)}" height="{_fmt(size_px)}" '
        f'preserveAspectRatio="xMidYMid meet" />'
    )


def _arc_points(cx: float, cy: float, r: float, start_deg: float, extent_deg: float, steps: int = 24):
    pts = []
    if steps < 2:
        steps = 2
    for i in range(steps + 1):
        t = i / steps
        a = start_deg + extent_deg * t
        th = math.radians(a)
        x = cx + r * math.cos(th)
        y = cy - r * math.sin(th)
        pts.append((x, y))
    return pts


def _aspect_style(aspect_type: str) -> tuple[str, str | None, float]:
    a = (aspect_type or "").upper()

    if a in {"TRI", "TRINE", "SEX", "SEXTILE"}:
        return ASPECT_BLUE, None, 1.8

    if a in {"OPP", "OPPOSITION", "SQR", "SQUARE"}:
        return ASPECT_RED, "6 4", 1.8

    if a in {"QUINCUNX", "QNX", "INC", "INCONJ"}:
        return ASPECT_VIOLET, "4 4", 1.5

    if a == "CONJ":
        return ASPECT_BLUE, None, 2.0

    return "#888888", "3 4", 1.3


def _planet_href(asset_base_url: str, planet_name: str) -> str | None:
    filename = PLANET_FILES.get(planet_name)
    if not filename:
        return None
    return f"{asset_base_url}/Planetes/{filename}"


def _sign_href(asset_base_url: str, sign_name: str) -> str | None:
    filename = SIGN_FILES.get(sign_name)
    if not filename:
        return None
    return f"{asset_base_url}/Signes/{filename}"


def _axis_href(asset_base_url: str, axis_label: str, language: str) -> str | None:
    files = AXIS_FILES_EN if language == "en" else AXIS_FILES_FR
    filename = files.get(axis_label)
    if not filename:
        return None
    return f"{asset_base_url}/Axes/{filename}"


def _build_aspect_lines(payload: dict[str, Any], layout: dict[str, Any]) -> list[str]:
    if not layout.get("ok"):
        return []

    cx = layout["meta"]["center"]["x"]
    cy = layout["meta"]["center"]["y"]
    r_aspect = layout["radii"]["aspect"]

    planets = {p["name"]: p for p in layout["planets"]}
    items = []

    for aspect in payload.get("aspects", []) or []:
        a_type = (aspect.get("type") or "").upper()
        if a_type == "CONJ":
            continue

        p1 = planets.get(aspect.get("p1"))
        p2 = planets.get(aspect.get("p2"))
        if not p1 or not p2:
            continue

        a1 = p1["real_angle"]
        a2 = p2["real_angle"]

        th1 = math.radians(a1)
        th2 = math.radians(a2)

        x1 = cx + r_aspect * math.cos(th1)
        y1 = cy - r_aspect * math.sin(th1)
        x2 = cx + r_aspect * math.cos(th2)
        y2 = cy - r_aspect * math.sin(th2)

        color, dash, width = _aspect_style(a_type)
        items.append(_svg_line(x1, y1, x2, y2, stroke=color, width=width, dash=dash))

    return items


def render_ecliptic_svg(
    payload: dict[str, Any],
    width: int = 1200,
    height: int = 900,
    *,
    language: str = "fr",
    title_suffix: str = "",
    show_title: bool = True,
    show_houses: bool = True,
    show_aspects: bool = True,
    asset_base_url: str = "/glyphes",
) -> str:
    """
    asset_base_url doit pointer vers le dossier statique qui contient :
      /Planetes
      /Signes
      /Axes

    Exemple final probable :
      /glyphes/Glyphes_SVG
    ou
      /static/Glyphes_SVG
    selon ton site.
    """
    layout = build_ecliptic_layout(
        payload,
        width,
        height,
        language=language,
        title_suffix=title_suffix,
        show_title=show_title,
        show_houses=show_houses,
        show_aspects=show_aspects,
    )

    if not layout.get("ok"):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
            f'<rect width="100%" height="100%" fill="#FFFFFF" />'
            f'{_svg_text(width/2, height/2, "Layout indisponible", size=18, fill="#666")}'
            f'</svg>'
        )

    cx = layout["meta"]["center"]["x"]
    cy = layout["meta"]["center"]["y"]
    title = layout["meta"]["title"]

    r_outer = layout["radii"]["outer"]
    r_inner = layout["radii"]["inner"]

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
    ]

    if title:
        parts.append(
            _svg_text(
                width / 2,
                28,
                title,
                size=28,
                fill=TITLE_COLOR,
                weight="700",
                baseline="hanging",
            )
        )

    if show_aspects:
        parts.extend(_build_aspect_lines(payload, layout))

    parts.append(_svg_circle(cx, cy, r_outer, stroke=STRUCT_GREY, width=3))
    parts.append(_svg_circle(cx, cy, r_inner, stroke=STRUCT_GREY, width=3))

    # Graduations de 5° dans la bande zodiacale
    grid_band = r_outer - r_inner
    tick_inner_r = r_inner + grid_band * 0.08
    tick_outer_r = r_outer - grid_band * 0.08

    for d in range(0, 360, 5):
        ang = math.radians(d)

        inner_len = grid_band * (0.10 if d % 30 else 0.18)
        outer_len = grid_band * (0.10 if d % 30 else 0.18)

        x1 = cx + tick_inner_r * math.cos(ang)
        y1 = cy - tick_inner_r * math.sin(ang)
        x2 = cx + (tick_inner_r + inner_len) * math.cos(ang)
        y2 = cy - (tick_inner_r + inner_len) * math.sin(ang)
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#D7D7D7", width=1, linecap="butt"))

        x3 = cx + tick_outer_r * math.cos(ang)
        y3 = cy - tick_outer_r * math.sin(ang)
        x4 = cx + (tick_outer_r - outer_len) * math.cos(ang)
        y4 = cy - (tick_outer_r - outer_len) * math.sin(ang)
        parts.append(_svg_line(x3, y3, x4, y4, stroke="#D7D7D7", width=1, linecap="butt"))

    for z in layout["zodiac_boundaries"]:
        (x1, y1) = z["inner"]
        (x2, y2) = z["outer"]
        parts.append(_svg_line(x1, y1, x2, y2, stroke=STRUCT_GREY, width=3))

    for hm in layout["house_marks"]:
        mk = hm["mark"]
        parts.append(
            _svg_line(
                mk["x1"], mk["y1"], mk["x2"], mk["y2"],
                stroke=HOUSE_MARK_COLOR,
                width=mk["width"],
            )
        )
        lbl = hm["label"]
        parts.append(
            _svg_text(
                lbl["x"], lbl["y"], hm["roman"],
                size=16,
                fill=HOUSE_MARK_COLOR,
            )
        )

    for s in layout["signs"]:
        href = _sign_href(asset_base_url, s["name"])
        if href:
            parts.append(_svg_image(href, s["x"], s["y"], s["px"]))
        else:
            parts.append(_svg_text(s["x"], s["y"], s["name"], size=max(14, int(s["px"] * 0.55))))

    for conj in layout["conjunction_links"]:
        for r in conj["radii"]:
            pts = _arc_points(cx, cy, r, conj["start"], conj["extent"], steps=28)
            parts.append(
                _svg_polyline(
                    pts,
                    stroke=conj["color"],
                    width=conj["width"],
                    fill="none",
                )
            )

    for label in ("AS", "DS", "MC", "FC"):
        ax = layout["axes"].get(label)
        if not ax:
            continue

        for seg in ax["segments"]:
            parts.append(
                _svg_line(
                    seg["x1"], seg["y1"], seg["x2"], seg["y2"],
                    stroke="#222222",
                    width=ax["width"],
                )
            )

        deco = ax["decoration"]
        if deco["type"] == "arrow":
            tip = deco["tip"]
            left = deco["left"]
            right = deco["right"]
            parts.append(_svg_line(tip["x"], tip["y"], left["x"], left["y"], stroke="#222222", width=ax["width"]))
            parts.append(_svg_line(tip["x"], tip["y"], right["x"], right["y"], stroke="#222222", width=ax["width"]))

        elif deco["type"] == "crossbar":
            left = deco["left"]
            right = deco["right"]
            parts.append(_svg_line(left["x"], left["y"], right["x"], right["y"], stroke="#222222", width=ax["width"]))

        elif deco["type"] == "circle":
            parts.append(_svg_circle(deco["cx"], deco["cy"], deco["r"], stroke="#222222", width=ax["width"]))

        elif deco["type"] == "half_circle":
            pts = _arc_points(
                deco["cx"], deco["cy"], deco["r"],
                deco["start"], deco["extent"], steps=24
            )
            parts.append(_svg_polyline(pts, stroke="#222222", width=ax["width"], fill="none"))

        href = _axis_href(asset_base_url, label, language)
        g = ax["glyph"]
        if href:
            parts.append(_svg_image(href, g["x"], g["y"], g["px"]))
        else:
            parts.append(
                _svg_text(
                    g["x"], g["y"], g["language_label"],
                    size=max(16, int(g["px"] * 0.55)),
                    fill="#1f4fa3",
                    weight="700",
                )
            )

    for p in layout["planets"]:
        for conn in p["connectors"]:
            parts.append(
                _svg_line(
                    conn["x1"], conn["y1"], conn["x2"], conn["y2"],
                    stroke=conn["color"],
                    width=conn["width"],
                )
            )

        href = _planet_href(asset_base_url, p["name"])
        if href:
            parts.append(_svg_image(href, p["x"], p["y"], p["px"]))
        else:
            parts.append(
                _svg_text(
                    p["x"], p["y"], p["name"],
                    size=max(12, int(p["px"] * 0.45)),
                    fill="#000000",
                )
            )

        deg = p.get("degree_label")
        if deg:
            parts.append(
                _svg_text(
                    deg["x"], deg["y"], str(deg["value"]),
                    size=15,
                    fill="#000000",
                )
            )
            if deg["retro"]:
                parts.append(
                    _svg_text(
                        deg["retro_x"], deg["retro_y"], "R",
                        size=12,
                        fill="#000000",
                    )
                )

    parts.append("</svg>")
    return "".join(parts)

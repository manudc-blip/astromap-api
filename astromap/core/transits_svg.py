from __future__ import annotations

import math
from datetime import datetime
from html import escape
from typing import Any

from .aspects import detect_aspects, detect_aspects_between


STRUCT_GREY = "#4A4A4A"
TITLE_COLOR = "#1f4fa3"
HOUSE_MARK_COLOR = "#0b3d91"
ASPECT_BLUE = "#0077CC"
ASPECT_RED = "#D62828"

TRANSIT_ASPECT_COLOR = "#b567d6"
TRANSIT_ASPECT_WIDTH = 1.0
TRANSIT_PLANET_SCALE = 0.90
SHOW_ASPECT_CURSORS = True

PERCEPTION_COEFFS = {
    "Soleil": 1.30,
    "Lune": 1.25,
    "Mercure": 1.05,
    "Vénus": 1.08,
    "Mars": 1.10,
    "Jupiter": 1.22,
    "Saturne": 1.18,
    "Uranus": 1.08,
    "Neptune": 1.08,
    "Pluton": 1.08,
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
}

PLANET_TRANSIT_FILES = {
    "Soleil": "Soleil_transit.svg",
    "Lune": "Lune_transit.svg",
    "Mercure": "Mercure_transit.svg",
    "Vénus": "Venus_transit.svg",
    "Mars": "Mars_transit.svg",
    "Jupiter": "Jupiter_transit.svg",
    "Saturne": "Saturne_transit.svg",
    "Uranus": "Uranus_transit.svg",
    "Neptune": "Neptune_transit.svg",
    "Pluton": "Pluton_transit.svg",
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
    "FC": "IC.svg",
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


def _pol_to_xy(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    th = math.radians(deg)
    return (cx + r * math.cos(th), cy - r * math.sin(th))


def _planet_href(asset_base_url: str, planet_name: str) -> str | None:
    fn = PLANET_FILES.get(planet_name)
    return f"{asset_base_url}/Planetes/{fn}" if fn else None


def _planet_transit_href(asset_base_url: str, planet_name: str) -> str | None:
    fn = PLANET_TRANSIT_FILES.get(planet_name)
    return f"{asset_base_url}/Planetes/{fn}" if fn else None


def _sign_href(asset_base_url: str, sign_name: str) -> str | None:
    fn = SIGN_FILES.get(sign_name)
    return f"{asset_base_url}/Signes/{fn}" if fn else None


def _axis_href(asset_base_url: str, axis_label: str, language: str) -> str | None:
    files = AXIS_FILES_EN if language == "en" else AXIS_FILES_FR
    fn = files.get(axis_label)
    return f"{asset_base_url}/Axes/{fn}" if fn else None


def _axis_screen_angle(axes: dict[str, Any], label: str, to_screen) -> float | None:
    v = axes.get(label)
    if v is None:
        return None
    return to_screen(float(v))


def _deg_from_px(px: float, r: float) -> float:
    return (px / max(r, 1.0)) * (180.0 / math.pi)


def _transit_dash(kind: str):
    if kind in ("SQR", "OPP"):
        return "1 3"
    return None


def _aspect_style(aspect_type: str) -> tuple[str, str | None, float]:
    a = (aspect_type or "").upper()

    if a in {"TRI", "TRINE", "SEX", "SEXTILE"}:
        return ASPECT_BLUE, None, 1.8

    if a in {"OPP", "OPPOSITION", "SQR", "SQUARE"}:
        return ASPECT_RED, "6 4", 1.8

    if a == "CONJ":
        return ASPECT_BLUE, None, 2.0

    return "#888888", "3 4", 1.3


def _build_natal_aspect_lines(natal_payload: dict[str, Any], cx: float, cy: float, r_aspect: float, to_screen) -> list[str]:
    parts: list[str] = []
    planets = natal_payload.get("planets", []) or []

    pmap = {}
    for p in planets:
        name = p.get("name")
        lon = p.get("lon")
        if name and lon is not None:
            pmap[name] = to_screen(float(lon))

    for a in natal_payload.get("aspects", []) or []:
        if (a.get("type") or "").upper() == "CONJ":
            continue

        p1 = a.get("p1")
        p2 = a.get("p2")
        if p1 not in pmap or p2 not in pmap:
            continue

        x1, y1 = _pol_to_xy(cx, cy, r_aspect, pmap[p1])
        x2, y2 = _pol_to_xy(cx, cy, r_aspect, pmap[p2])

        color, dash, width = _aspect_style(a.get("type", ""))
        parts.append(_svg_line(x1, y1, x2, y2, stroke=color, width=width, dash=dash))

    return parts


def render_transits_svg(
    payload: dict[str, Any],
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    natal_payload = payload.get("natal") or {}
    transit_payload = (payload.get("transit") or {})
    transit_planets = transit_payload.get("planets") or []

    if not natal_payload.get("planets") or not transit_planets:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
            f'<rect width="100%" height="100%" fill="#FFFFFF" />'
            f'{_svg_text(width/2, height/2, "Payload transits indisponible", size=18, fill="#666")}'
            f'</svg>'
        )

    w = width
    h = height
    margin = 24

    size0 = min(w, h) - 2 * margin
    scale_theme = 0.80
    size = int(size0 * scale_theme)

    cx = w / 2
    cy = h / 2

    r_outer = size * 0.36
    r_inner = size * 0.23
    px_planet_base = int(size * 0.050)

    grid_band = size * 0.020
    circ_in_w = 2.0
    gap_in = circ_in_w / 2.0

    r2_grid_in = r_inner + gap_in
    r2_grid_out = r2_grid_in + grid_band
    r_link_inner = (r2_grid_in + r2_grid_out) * 0.5

    circ_out_w = 3.0
    gap_out = circ_out_w / 2.0

    r_grid_out = r_outer - gap_out
    r_grid_in = r_grid_out - grid_band
    r_link_outer = (r_grid_in + r_grid_out) * 0.5

    outer_gap_min = int(size * 0.030)
    outer_gap_factor = 1.30
    outer_gap = max(outer_gap_min, int(px_planet_base * outer_gap_factor))

    r_planet_natal = r_outer + outer_gap
    r_planet_transit = r_outer + outer_gap + int(size * 0.13)

    r_line_start = r_link_outer
    r_elbow = (r_line_start + r_planet_transit) / 2.0
    r_aspect = r_inner

    axes = natal_payload.get("axes", {})

    def to_screen(deg: float) -> float:
        asc = float(axes.get("AS", 0.0))
        return (float(deg) - asc + 180.0) % 360.0

    title = "Thème de transit"
    try:
        dt_natal = datetime.fromisoformat(natal_payload.get("meta", {}).get("datetime_utc"))
        dt_transit = datetime.fromisoformat(transit_payload.get("meta", {}).get("datetime_utc"))
        delta_days = (dt_transit - dt_natal).total_seconds() / 86400.0
        age_years = delta_days / 365.2425
        age_text = f"{age_years:.2f}".replace(".", ",") + " ans" if language == "fr" else f"{age_years:.2f} years"
        title = f"Thème de transit ({age_text})" if language == "fr" else f"Transit chart ({age_text})"
    except Exception:
        title = "Thème de transit" if language == "fr" else "Transit chart"

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
        _svg_text(w / 2, 28, title, size=18, fill=TITLE_COLOR, weight="700", baseline="hanging"),
    ]

    # Aspects natals
    parts.extend(_build_natal_aspect_lines(natal_payload, cx, cy, r_aspect, to_screen))

    # Cercle intérieur d'aspects
    parts.append(_svg_circle(cx, cy, r_inner, stroke=STRUCT_GREY, width=3))

    # Bande de graduations intérieure
    parts.append(_svg_circle(cx, cy, r2_grid_in, stroke="#DDDDDD", width=circ_in_w))
    parts.append(_svg_circle(cx, cy, r2_grid_out, stroke="#DDDDDD", width=1))

    for d in range(0, 360, 5):
        ang = to_screen(float(d))
        x1, y1 = _pol_to_xy(cx, cy, r2_grid_in, ang)
        tick_len = grid_band * (0.90 if d % 30 == 0 else (0.55 if d % 10 == 0 else 0.32))
        x2, y2 = _pol_to_xy(cx, cy, r2_grid_in + tick_len, ang)
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#D7D7D7", width=1, linecap="butt"))

    # Bande zodiacale
    parts.append(_svg_circle(cx, cy, r_grid_in, stroke="#DDDDDD", width=1))
    parts.append(_svg_circle(cx, cy, r_grid_out, stroke=STRUCT_GREY, width=circ_out_w))

    for d in range(0, 360, 5):
        ang = to_screen(float(d))
        x1, y1 = _pol_to_xy(cx, cy, r_grid_in, ang)
        tick_len = grid_band * (0.95 if d % 30 == 0 else (0.60 if d % 10 == 0 else 0.34))
        x2, y2 = _pol_to_xy(cx, cy, r_grid_in + tick_len, ang)
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#D7D7D7", width=1, linecap="butt"))

    # Frontières signes
    for i in range(12):
        deg = float(i * 30)
        ang = to_screen(deg)
        x1, y1 = _pol_to_xy(cx, cy, r_inner, ang)
        x2, y2 = _pol_to_xy(cx, cy, r_grid_out, ang)
        parts.append(_svg_line(x1, y1, x2, y2, stroke=STRUCT_GREY, width=3))

    # Signes natals dans la roue
    sign_radius = (r_grid_in + r_inner) * 0.5
    sign_px = max(24, int(size * 0.050))
    signs_fr = [
        "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
        "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"
    ]
    for i, sign_name in enumerate(signs_fr):
        ang = to_screen(i * 30 + 15)
        sx, sy = _pol_to_xy(cx, cy, sign_radius, ang)
        href = _sign_href(asset_base_url, sign_name)
        if href:
            parts.append(_svg_image(href, sx, sy, sign_px))
        else:
            parts.append(_svg_text(sx, sy, sign_name, size=12))

    # Marques de maisons et chiffres romains
    houses = natal_payload.get("houses", []) or []
    for idx, hitem in enumerate(houses):
        cusp = hitem.get("cusp")
        if cusp is None:
            continue
        ang = to_screen(float(cusp))
        x1, y1 = _pol_to_xy(cx, cy, r_grid_in, ang)
        x2, y2 = _pol_to_xy(cx, cy, r_grid_out, ang)
        parts.append(_svg_line(x1, y1, x2, y2, stroke=HOUSE_MARK_COLOR, width=2))

        next_cusp = houses[(idx + 1) % len(houses)].get("cusp", cusp + 30)
        start = float(cusp)
        end = float(next_cusp)
        span = (end - start) % 360.0
        mid = (start + span / 2.0) % 360.0
        mid_ang = to_screen(mid)
        tx, ty = _pol_to_xy(cx, cy, (r_inner + r_grid_in) * 0.5, mid_ang)
        roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"][idx]
        parts.append(_svg_text(tx, ty, roman, size=16, fill=HOUSE_MARK_COLOR))

    # Axes
    axis_width = max(3, int(size * 0.005))
    glyph_px = max(34, int(size * 0.060))
    axis_defs = {
        "AS": {"deco": "arrow", "glyph_r": r_outer + int(size * 0.12)},
        "DS": {"deco": "crossbar", "glyph_r": r_outer + int(size * 0.12)},
        "MC": {"deco": "circle", "glyph_r": r_outer + int(size * 0.12)},
        "FC": {"deco": "half_circle", "glyph_r": r_outer + int(size * 0.12)},
    }

    for label in ("AS", "DS", "MC", "FC"):
        av = axes.get(label)
        if av is None:
            continue

        ang = to_screen(float(av))
        x1, y1 = _pol_to_xy(cx, cy, 0, ang)
        x2, y2 = _pol_to_xy(cx, cy, r_outer + int(size * 0.12), ang)
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#222222", width=axis_width))

        endx, endy = x2, y2
        dx = math.cos(math.radians(ang))
        dy = -math.sin(math.radians(ang))

        deco = axis_defs[label]["deco"]
        if deco == "arrow":
            ah = int(size * 0.04)
            aw = int(size * 0.018)
            tip = (endx, endy)
            base = (endx - dx * ah, endy - dy * ah)
            px = -dy
            py = dx
            left = (base[0] + px * aw, base[1] + py * aw)
            right = (base[0] - px * aw, base[1] - py * aw)
            parts.append(_svg_line(tip[0], tip[1], left[0], left[1], stroke="#222222", width=axis_width))
            parts.append(_svg_line(tip[0], tip[1], right[0], right[1], stroke="#222222", width=axis_width))

        elif deco == "crossbar":
            bar_half = int(size * 0.015)
            px = -dy
            py = dx
            left = (endx + px * bar_half, endy + py * bar_half)
            right = (endx - px * bar_half, endy - py * bar_half)
            parts.append(_svg_line(left[0], left[1], right[0], right[1], stroke="#222222", width=axis_width))

        elif deco == "circle":
            parts.append(_svg_circle(endx, endy, int(size * 0.025), stroke="#222222", width=axis_width, fill="white"))

        elif deco == "half_circle":
            pts = _arc_points(endx, endy, int(size * 0.025), ang - 90, 180, steps=24)
            parts.append(_svg_polyline(pts, stroke="#222222", width=axis_width, fill="none"))

        gx, gy = _pol_to_xy(cx, cy, axis_defs[label]["glyph_r"], ang)
        href = _axis_href(asset_base_url, label, language)
        if href:
            parts.append(_svg_image(href, gx, gy, glyph_px))
        else:
            parts.append(_svg_text(gx, gy, label, size=18, fill=TITLE_COLOR, weight="700"))

    # Planètes natales
    natal_planets = natal_payload.get("planets", []) or []
    natal_items = []
    for p in natal_planets:
        name = p.get("name", "?")
        try:
            lon = float(p.get("lon", 0.0))
        except Exception:
            lon = 0.0

        ang_real = to_screen(lon)
        deg_in_sign = lon % 30.0
        px_target = int(px_planet_base * PERCEPTION_COEFFS.get(name, 1.0))

        is_retro = False
        for key in ("retro", "retrograde", "rflag"):
            if key in p:
                val = p.get(key)
                if isinstance(val, bool):
                    is_retro = val
                else:
                    try:
                        is_retro = bool(int(val))
                    except Exception:
                        if isinstance(val, str) and val.upper().startswith("R"):
                            is_retro = True
                break
        if not is_retro:
            dm = p.get("daily_motion")
            try:
                if dm is not None and float(dm) < 0:
                    is_retro = True
            except Exception:
                pass

        natal_items.append({
            "name": name,
            "real": ang_real,
            "adj": ang_real,
            "px": px_target,
            "deg_in_sign": deg_in_sign,
            "is_retro": is_retro,
        })

    # Packing natal
    if natal_items:
        def _circ_mean(degs):
            sx = sum(math.cos(math.radians(d)) for d in degs)
            sy = sum(math.sin(math.radians(d)) for d in degs)
            if sx == 0 and sy == 0:
                return (degs[0] + 360.0) % 360.0
            return (math.degrees(math.atan2(sy, sx)) + 360.0) % 360.0

        def _unwrap_around(ref, degs):
            out = []
            for d in degs:
                x = d
                while x - ref >= 180.0:
                    x -= 360.0
                while x - ref < -180.0:
                    x += 360.0
                out.append(x)
            return out

        angles_real = [d["real"] for d in natal_items]
        ref = _circ_mean(angles_real)
        lin = _unwrap_around(ref, angles_real)
        order = sorted(range(len(natal_items)), key=lambda idx: lin[idx])
        max_px = max(d["px"] for d in natal_items)
        min_gap = _deg_from_px(0.85 * (2 * max_px), r_planet_natal)

        adj_lin = lin[:]
        for _ in range(2):
            for k in range(1, len(order)):
                i_prev = order[k - 1]
                i_cur = order[k]
                gap = adj_lin[i_cur] - adj_lin[i_prev]
                if gap < min_gap:
                    shift = min_gap - gap
                    adj_lin[i_prev] -= 0.5 * shift
                    adj_lin[i_cur] += 0.5 * shift

            for k in range(len(order) - 2, -1, -1):
                i_cur = order[k]
                i_next = order[k + 1]
                gap = adj_lin[i_next] - adj_lin[i_cur]
                if gap < min_gap:
                    shift = min_gap - gap
                    adj_lin[i_cur] -= 0.5 * shift
                    adj_lin[i_next] += 0.5 * shift

        mean0 = sum(lin) / max(1, len(lin))
        mean1 = sum(adj_lin) / max(1, len(adj_lin))
        drift = mean1 - mean0
        for i in range(len(adj_lin)):
            adj_lin[i] -= drift

        for i, d in enumerate(natal_items):
            d["adj"] = (adj_lin[i] + 360.0) % 360.0

    # Aspects transits
    natal_xy = {}
    transit_xy = {}
    angles_natal = {}
    angles_transit = {}

    for p in natal_items:
        angles_natal[p["name"]] = p["real"]
        natal_xy[p["name"]] = _pol_to_xy(cx, cy, r_aspect, p["real"])

    for p in transit_planets:
        name = p.get("name")
        lon = p.get("lon")
        if name and lon is not None:
            ang = to_screen(float(lon))
            angles_transit[name] = ang
            transit_xy[name] = _pol_to_xy(cx, cy, r_aspect, ang)

    aspect_mode = ((payload.get("meta") or {}).get("aspect_mode") or "TN").upper()
    if aspect_mode == "TT":
        aspects_list = detect_aspects(transit_planets, exclude_sextiles_from_saturn=False)

        for a in aspects_list:
            if a.get("type") == "CONJ":
                continue
            p1 = a.get("p1")
            p2 = a.get("p2")
            if p1 in transit_xy and p2 in transit_xy:
                dash = _transit_dash(a.get("type", ""))
                parts.append(_svg_line(*transit_xy[p1], *transit_xy[p2], stroke=TRANSIT_ASPECT_COLOR, width=TRANSIT_ASPECT_WIDTH, dash=dash, linecap="butt"))

        if SHOW_ASPECT_CURSORS:
            for a in aspects_list:
                if a.get("type") == "CONJ":
                    continue
                for name in (a.get("p1"), a.get("p2")):
                    ang = angles_transit.get(name)
                    if ang is None:
                        continue
                    x1, y1 = _pol_to_xy(cx, cy, r2_grid_in, ang)
                    x2, y2 = _pol_to_xy(cx, cy, r_link_inner, ang)
                    parts.append(_svg_line(x1, y1, x2, y2, stroke=TRANSIT_ASPECT_COLOR, width=1, linecap="butt"))
    else:
        aspects_tn = detect_aspects_between(
            transit_planets,
            natal_payload.get("planets", []),
            side_a="T",
            side_b="N",
            exclude_sextiles_from_saturn=False,
        )

        for a in aspects_tn:
            if a.get("type") == "CONJ":
                continue
            p_t = a.get("p1")
            p_n = a.get("p2")
            if p_t in transit_xy and p_n in natal_xy:
                dash = _transit_dash(a.get("type", ""))
                parts.append(_svg_line(*transit_xy[p_t], *natal_xy[p_n], stroke=TRANSIT_ASPECT_COLOR, width=TRANSIT_ASPECT_WIDTH, dash=dash, linecap="butt"))

        if SHOW_ASPECT_CURSORS:
            for a in aspects_tn:
                if a.get("type") == "CONJ":
                    continue
                for name, ang_map in ((a.get("p1"), angles_transit), (a.get("p2"), angles_natal)):
                    ang = ang_map.get(name)
                    if ang is None:
                        continue
                    x1, y1 = _pol_to_xy(cx, cy, r2_grid_in, ang)
                    x2, y2 = _pol_to_xy(cx, cy, r_link_inner, ang)
                    parts.append(_svg_line(x1, y1, x2, y2, stroke=TRANSIT_ASPECT_COLOR, width=1, linecap="butt"))

    # Planètes natales, avec halo sur axes
    margin_oblique = 1.0
    deg_out_natal = int(size * 0.035)
    for d in natal_items:
        name = d["name"]
        ang_band = d["real"]
        ang_glyph = d["adj"]
        gx, gy = _pol_to_xy(cx, cy, r_planet_natal, ang_glyph)

        xb0, yb0 = _pol_to_xy(cx, cy, r_line_start, ang_band)
        xb1, yb1 = _pol_to_xy(cx, cy, (r_line_start + r_planet_natal) / 2.0, ang_band)
        parts.append(_svg_line(xb0, yb0, xb1, yb1, stroke="#555555", width=1))

        half_px = 0.5 * d["px"]
        dx, dy = (gx - xb1), (gy - yb1)
        dist = math.hypot(dx, dy)
        stop_from_elbow = max(dist - (half_px + margin_oblique), 0.0)
        if dist > 0 and stop_from_elbow > 0:
            t = stop_from_elbow / dist
            xo, yo = (xb1 + dx * t, yb1 + dy * t)
            parts.append(_svg_line(xb1, yb1, xo, yo, stroke="#555555", width=1))

        for label in ("AS", "DS", "MC", "FC"):
            aA = _axis_screen_angle(axes, label, to_screen)
            if aA is None:
                continue
            dist_ax = abs((ang_glyph - aA + 180.0) % 360.0 - 180.0)
            w_deg = ((half_px + 2) / max(1.0, r_planet_natal)) * (180.0 / math.pi)
            if dist_ax < w_deg:
                halo_r = half_px - 1
                parts.append(_svg_circle(gx, gy, halo_r, fill="#FFFFFF", stroke="#FFFFFF", width=0))
                break

        href = _planet_href(asset_base_url, name)
        if href:
            parts.append(_svg_image(href, gx, gy, d["px"]))

        n = int(round(float(d["deg_in_sign"]))) % 30
        tx, ty = _pol_to_xy(cx, cy, r_planet_natal + deg_out_natal, ang_glyph)
        parts.append(_svg_text(tx, ty, str(n), size=max(10, int(size * 0.012)), fill="#222222"))
        if d.get("is_retro"):
            parts.append(_svg_text(tx + int(d["px"] * 0.35), ty, "R", size=max(9, int(size * 0.010)), fill="#222222"))

    # Planètes de transit
    trans_items = []
    for p in transit_planets:
        name = p.get("name", "?")
        try:
            lon = float(p.get("lon", 0.0))
        except Exception:
            lon = 0.0

        ang_real = to_screen(lon)
        deg_in_sign = lon % 30.0

        is_retro = False
        for key in ("retro", "retrograde", "rflag"):
            if key in p:
                val = p.get(key)
                if isinstance(val, bool):
                    is_retro = val
                else:
                    try:
                        is_retro = bool(int(val))
                    except Exception:
                        if isinstance(val, str) and val.upper().startswith("R"):
                            is_retro = True
                break
        if not is_retro:
            dm = p.get("daily_motion")
            try:
                if dm is not None and float(dm) < 0:
                    is_retro = True
            except Exception:
                pass

        px_target = int(px_planet_base * PERCEPTION_COEFFS.get(name, 1.0) * TRANSIT_PLANET_SCALE)
        trans_items.append({
            "name": name,
            "lon": lon,
            "real": ang_real,
            "adj": ang_real,
            "px": px_target,
            "deg_in_sign": deg_in_sign,
            "is_retro": is_retro,
        })

    if trans_items:
        def _circ_mean(degs):
            sx = sum(math.cos(math.radians(d)) for d in degs)
            sy = sum(math.sin(math.radians(d)) for d in degs)
            if sx == 0 and sy == 0:
                return (degs[0] + 360.0) % 360.0
            return (math.degrees(math.atan2(sy, sx)) + 360.0) % 360.0

        def _unwrap_around(ref, degs):
            out = []
            for d in degs:
                x = d
                while x - ref >= 180.0:
                    x -= 360.0
                while x - ref < -180.0:
                    x += 360.0
                out.append(x)
            return out

        angles_real = [d["real"] for d in trans_items]
        ref = _circ_mean(angles_real)
        lin = _unwrap_around(ref, angles_real)
        order = sorted(range(len(trans_items)), key=lambda idx: lin[idx])

        max_px = max(d["px"] for d in trans_items)
        min_gap = _deg_from_px(0.85 * (2 * max_px), r_planet_transit)

        adj_lin = lin[:]
        for _ in range(2):
            for k in range(1, len(order)):
                i_prev = order[k - 1]
                i_cur = order[k]
                gap = adj_lin[i_cur] - adj_lin[i_prev]
                if gap < min_gap:
                    shift = min_gap - gap
                    adj_lin[i_prev] -= 0.5 * shift
                    adj_lin[i_cur] += 0.5 * shift

            for k in range(len(order) - 2, -1, -1):
                i_cur = order[k]
                i_next = order[k + 1]
                gap = adj_lin[i_next] - adj_lin[i_cur]
                if gap < min_gap:
                    shift = min_gap - gap
                    adj_lin[i_cur] -= 0.5 * shift
                    adj_lin[i_next] += 0.5 * shift

        mean0 = sum(lin) / max(1, len(lin))
        mean1 = sum(adj_lin) / max(1, len(adj_lin))
        drift = mean1 - mean0
        for i in range(len(adj_lin)):
            adj_lin[i] -= drift

        for i, d in enumerate(trans_items):
            d["adj"] = (adj_lin[i] + 360.0) % 360.0

    deg_out = int(size * 0.040)
    for d in trans_items:
        name = d["name"]
        ang_band = d["real"]
        ang_glyph = d["adj"]

        gx, gy = _pol_to_xy(cx, cy, r_planet_transit, ang_glyph)

        xb0, yb0 = _pol_to_xy(cx, cy, r_line_start, ang_band)
        xb1, yb1 = _pol_to_xy(cx, cy, r_elbow, ang_band)
        parts.append(_svg_line(xb0, yb0, xb1, yb1, stroke="#b567d6", width=1))

        half_px = 0.5 * d["px"]
        dx, dy = (gx - xb1), (gy - yb1)
        dist = math.hypot(dx, dy)
        stop_from_elbow = max(dist - (half_px + margin_oblique), 0.0)
        if dist > 0 and stop_from_elbow > 0:
            t = stop_from_elbow / dist
            xo, yo = (xb1 + dx * t, yb1 + dy * t)
            parts.append(_svg_line(xb1, yb1, xo, yo, stroke="#b567d6", width=1))

        for label in ("AS", "DS", "MC", "FC"):
            aA = _axis_screen_angle(axes, label, to_screen)
            if aA is None:
                continue
            dist_ax = abs((ang_glyph - aA + 180.0) % 360.0 - 180.0)
            w_deg = ((half_px + 2) / max(1.0, r_planet_transit)) * (180.0 / math.pi)
            if dist_ax < w_deg:
                halo_r = half_px - 1
                parts.append(_svg_circle(gx, gy, halo_r, fill="#FFFFFF", stroke="#FFFFFF", width=0))
                break

        href = _planet_transit_href(asset_base_url, name) or _planet_href(asset_base_url, name)
        if href:
            parts.append(_svg_image(href, gx, gy, d["px"]))

        n = int(round(float(d["deg_in_sign"]))) % 30
        tx, ty = _pol_to_xy(cx, cy, r_planet_transit + deg_out, ang_glyph)
        parts.append(_svg_text(tx, ty, str(n), size=max(10, int(size * 0.012)), fill="#b567d6"))
        if d.get("is_retro"):
            parts.append(_svg_text(tx + int(d["px"] * 0.35), ty, "R", size=max(9, int(size * 0.010)), fill="#b567d6"))

    parts.append("</svg>")
    return "".join(parts)

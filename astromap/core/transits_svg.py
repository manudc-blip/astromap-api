from __future__ import annotations

import math
from datetime import datetime
from html import escape
from typing import Any

from .aspects import detect_aspects, detect_aspects_between
from .ecliptic_svg import render_ecliptic_svg


STRUCT_GREY = "#4A4A4A"
SHOW_ASPECT_CURSORS = True

PERCEPTION_COEFFS = {
    "Soleil": 1.00,
    "Lune": 1.00,
    "Mercure": 1.20,
    "Vénus": 1.10,
    "Mars": 1.05,
    "Jupiter": 1.05,
    "Saturne": 1.15,
    "Uranus": 1.15,
    "Neptune": 1.05,
    "Pluton": 1.10,
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
    name: filename.replace(".svg", "_transit.svg")
    for name, filename in PLANET_FILES.items()
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


def _svg_image(
    href: str,
    x_center: float,
    y_center: float,
    size_px: float,
    *,
    elem_id: str | None = None,
    class_name: str | None = None,
    data_planet: str | None = None,
    title: str | None = None,
) -> str:
    half = size_px / 2.0

    attrs = []
    if elem_id:
        attrs.append(f'id="{escape(elem_id)}"')
    if class_name:
        attrs.append(f'class="{escape(class_name)}"')
    if data_planet:
        attrs.append(f'data-planet="{escape(data_planet)}"')

    attrs_str = (" " + " ".join(attrs)) if attrs else ""
    title_part = f"<title>{escape(title)}</title>" if title else ""

    return (
        f"<g{attrs_str}>"
        f"{title_part}"
        f'<image href="{escape(href)}" '
        f'x="{_fmt(x_center - half)}" y="{_fmt(y_center - half)}" '
        f'width="{_fmt(size_px)}" height="{_fmt(size_px)}" '
        f'preserveAspectRatio="xMidYMid meet" />'
        f"</g>"
    )

def _pol_to_xy(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    th = math.radians(deg)
    return (cx + r * math.cos(th), cy - r * math.sin(th))


def _planet_href(asset_base_url: str, planet_name: str) -> str | None:
    fn = PLANET_FILES.get(planet_name)
    return f"{asset_base_url}/Planetes/{fn}" if fn else None


def _planet_transit_href(asset_base_url: str, planet_name: str) -> str | None:
    fn = PLANET_TRANSIT_FILES.get(planet_name)
    return f"{asset_base_url}/Planetes/{fn}" if fn else None


def _deg_from_px(px: float, r: float) -> float:
    return (px / max(r, 1.0)) * (180.0 / math.pi)


def _transit_dash(kind: str):
    if kind in ("SQR", "OPP"):
        return "1 3"
    return None


def _extract_svg_inner(svg: str) -> str:
    start = svg.find(">")
    end = svg.rfind("</svg>")
    if start == -1 or end == -1 or end <= start:
        return svg
    return svg[start + 1:end]


def render_transits_svg(
    natal_payload: dict[str, Any],
    transit_payload: dict[str, Any],
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    aspect_mode: str = "TN",
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    if not natal_payload or not natal_payload.get("planets"):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
            f'<rect width="100%" height="100%" fill="#FFFFFF" />'
            f'{_svg_text(width/2, height/2, "Payload natal indisponible", size=18, fill="#666")}'
            f'</svg>'
        )

    if not transit_payload or not transit_payload.get("planets"):
        return render_ecliptic_svg(
            natal_payload,
            width=width,
            height=height,
            language=language,
            show_title=True,
            show_houses=True,
            show_aspects=True,
            asset_base_url=asset_base_url,
        )

    w = width
    h = height
    margin = 24

    size0 = min(w, h) - 2 * margin
    scale_theme = 0.80
    size = int(size0 * scale_theme)
    theme_dx = 100.0
    theme_dy = 12.0

    cx, cy = w / 2 + theme_dx, h / 2 + theme_dy

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

    r_planet_transit = r_outer + outer_gap + int(size * 0.13)
    r_line_start = r_link_outer
    r_elbow = (r_line_start + r_planet_transit) / 2.0
    r_aspect = r_inner

    axes = natal_payload.get("axes", {})

    def to_screen(deg: float) -> float:
        asc = float(axes.get("AS", 0.0))
        return (float(deg) - asc + 180.0) % 360.0

    def _axis_screen_angle(label: str):
        v = axes.get(label, None)
        return to_screen(float(v)) if v is not None else None

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
    ]

    # 1) Fond natal complet, identique à l’écliptique, sans titre
    natal_svg = render_ecliptic_svg(
        natal_payload,
        width=width,
        height=height,
        language=language,
        show_title=False,
        show_houses=True,
        show_aspects=True,
        asset_base_url=asset_base_url,
        center_dx=theme_dx,
        center_dy=theme_dy,
    )
    parts.append('<g>')

    # 2) Aspects transit
    transit_aspect_color = "#b567d6"
    transit_aspect_width = 1.0

    natal_xy = {}
    transit_xy = {}
    angles_natal = {}
    angles_transit = {}

    for p in natal_payload.get("planets", []):
        name = p.get("name")
        lon = p.get("lon")
        if name and lon is not None:
            ang = to_screen(float(lon))
            angles_natal[name] = ang
            natal_xy[name] = _pol_to_xy(cx, cy, r_aspect, ang)

    for p in transit_payload.get("planets", []):
        name = p.get("name")
        lon = p.get("lon")
        if name and lon is not None:
            ang = to_screen(float(lon))
            angles_transit[name] = ang
            transit_xy[name] = _pol_to_xy(cx, cy, r_aspect, ang)

    if (aspect_mode or "TN").upper() == "TT":
        aspects_list = detect_aspects(transit_payload.get("planets", []))

        for a in aspects_list:
            if a.get("type") == "CONJ":
                continue

            p1 = a.get("p1")
            p2 = a.get("p2")

            if p1 in transit_xy and p2 in transit_xy:
                parts.append(
                    _svg_line(
                        *transit_xy[p1],
                        *transit_xy[p2],
                        stroke=transit_aspect_color,
                        width=transit_aspect_width,
                        dash=_transit_dash(a.get("type")),
                        linecap="butt",
                    )
                )

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
                    parts.append(
                        _svg_line(
                            x1, y1, x2, y2,
                            stroke=transit_aspect_color,
                            width=1,
                            linecap="butt",
                        )
                    )
    else:
        aspects_tn = detect_aspects_between(
            transit_payload.get("planets", []),
            natal_payload.get("planets", []),
            side_a="T",
            side_b="N",
        )

        for a in aspects_tn:
            if a.get("type") == "CONJ":
                continue

            p_t = a.get("p1")
            p_n = a.get("p2")

            if p_t in transit_xy and p_n in natal_xy:
                parts.append(
                    _svg_line(
                        *transit_xy[p_t],
                        *natal_xy[p_n],
                        stroke=transit_aspect_color,
                        width=transit_aspect_width,
                        dash=_transit_dash(a.get("type")),
                        linecap="butt",
                    )
                )

        if SHOW_ASPECT_CURSORS:
            for a in aspects_tn:
                if a.get("type") == "CONJ":
                    continue

                for name, angle_map in ((a.get("p1"), angles_transit), (a.get("p2"), angles_natal)):
                    ang = angle_map.get(name)
                    if ang is None:
                        continue

                    x1, y1 = _pol_to_xy(cx, cy, r2_grid_in, ang)
                    x2, y2 = _pol_to_xy(cx, cy, r_link_inner, ang)
                    parts.append(
                        _svg_line(
                            x1, y1, x2, y2,
                            stroke=transit_aspect_color,
                            width=1,
                            linecap="butt",
                        )
                    )

    # 3) Planètes de transit
    transit_planet_scale = 0.90
    trans_planets = []

    for p in transit_payload.get("planets", []):
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

        px_target = int(px_planet_base * PERCEPTION_COEFFS.get(name, 1.0) * transit_planet_scale)

        trans_planets.append(
            {
                "name": name,
                "lon": lon,
                "real": ang_real,
                "adj": ang_real,
                "px": px_target,
                "deg_in_sign": deg_in_sign,
                "is_retro": is_retro,
            }
        )

    if trans_planets:
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

        angles_real = [d["real"] for d in trans_planets]
        ref = _circ_mean(angles_real)
        lin = _unwrap_around(ref, angles_real)
        order = sorted(range(len(trans_planets)), key=lambda idx: lin[idx])

        max_px = max(d["px"] for d in trans_planets)
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
        if abs(drift) > 1e-9:
            for i in range(len(adj_lin)):
                adj_lin[i] -= drift

        for i, d in enumerate(trans_planets):
            d["adj"] = (adj_lin[i] + 360.0) % 360.0

    margin_oblique = 1.0
    deg_out = int(size * 0.040)
    font_deg = max(10, int(size * 0.012))

    for d in trans_planets:
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

        # halo blanc si passe sur un axe
        for label in ("AS", "DS", "MC", "FC"):
            a_a = _axis_screen_angle(label)
            if a_a is None:
                continue
            dist_ax = abs((ang_glyph - a_a + 180.0) % 360.0 - 180.0)
            w_deg = ((half_px + 2) / max(1.0, r_planet_transit)) * (180.0 / math.pi)
            if dist_ax < w_deg:
                halo_r = half_px - 1
                parts.append(_svg_circle(gx, gy, halo_r, fill="#FFFFFF", stroke="#FFFFFF", width=0))
                break

        href = _planet_transit_href(asset_base_url, name)
        if not href:
            href = _planet_href(asset_base_url, name)
        if href:
            parts.append(
                _svg_image(
                    href,
                    gx,
                    gy,
                    d["px"],
                    elem_id=f"transit_planet_{name}",
                    class_name="transit_planet transit",
                    data_planet=name,
                    title=name,
                )
            )

        try:
            n = int(round(float(d["deg_in_sign"]))) % 30
            tx, ty = _pol_to_xy(cx, cy, r_planet_transit + deg_out, ang_glyph)
            parts.append(_svg_text(tx, ty, str(n), size=font_deg, fill="#b567d6"))
            if d.get("is_retro"):
                parts.append(
                    _svg_text(
                        tx + int(d["px"] * 0.35),
                        ty,
                        "R",
                        size=max(9, int(size * 0.010)),
                        fill="#b567d6",
                    )
                )
        except Exception:
            pass

    # 4) Titre transit
    age_text = None
    try:
        meta_natal = natal_payload.get("meta", {})
        meta_transit = transit_payload.get("meta", {})
        dt_natal = datetime.fromisoformat(meta_natal.get("datetime_utc"))
        dt_transit = datetime.fromisoformat(meta_transit.get("datetime_utc"))
        delta_days = (dt_transit - dt_natal).total_seconds() / 86400.0
        age_years = delta_days / 365.2425
        if language == "fr":
            age_text = f"{age_years:.2f}".replace(".", ",") + " ans"
        else:
            age_text = f"{age_years:.2f} years"
    except Exception:
        age_text = None

    if language == "fr":
        title_text = f"Thème de transit ({age_text})" if age_text else "Thème de transit"
    else:
        title_text = f"Transit chart ({age_text})" if age_text else "Transit chart"

    parts.append(
        _svg_text(
            w / 2,
            22,
            title_text,
            size=22,
            fill="#1f4fa3",
            weight="700",
            baseline="hanging",
            family="Segoe UI, Arial, sans-serif",
        )
    )

    parts.append("</svg>")
    return "".join(parts)

from __future__ import annotations

import math
from html import escape
from typing import Any


ROMANS = ["I", "II", "III", "IV", "V", "VI",
          "VII", "VIII", "IX", "X", "XI", "XII"]

SIGN_NAMES = [
    "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
    "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons",
]

STRUCT_GREY = "#4A4A4A"
TITLE_COLOR = "#0b3d91"
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

HOUSE_FILES = {str(i): f"Maison {i}.svg" for i in range(1, 13)}
SIGN_FILES_DOM = {name: f"{name}.svg" for name in SIGN_NAMES}

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

K_PROX = 0.75
ORB_CONJ_G1G1 = 18.0
ORB_CONJ_G1G2 = 16.0
ORB_CONJ_G2G2 = 14.0

K_PUSH = 0.90
DELTA_CAP_RATIO = 1.60
SPAN_MARGIN_RATIO = 0.15

G1_RAPIDES = {"Soleil", "Lune", "Mercure", "Vénus", "Mars"}
G2_LENTES = {"Jupiter", "Saturne", "Uranus", "Neptune", "Pluton"}


def _fmt(v: float) -> str:
    return f"{v:.2f}"


def _norm_deg(d: float) -> float:
    return d % 360.0


def _pol_to_xy(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    th = math.radians(deg)
    return (cx + r * math.cos(th), cy - r * math.sin(th))


def _deg_from_px(px_len: float, radius: float) -> float:
    if radius <= 0:
        return 0.0
    return (px_len / (2 * math.pi * radius)) * 360.0


def _svg_line(x1, y1, x2, y2, stroke="#000", width=1, dash=None, linecap="round") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{_fmt(x1)}" y1="{_fmt(y1)}" '
        f'x2="{_fmt(x2)}" y2="{_fmt(y2)}" '
        f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="{linecap}"{dash_attr} />'
    )


def _svg_circle(cx, cy, r, stroke="#000", width=1, fill="none", opacity: float | None = None) -> str:
    opacity_attr = f' opacity="{opacity:.2f}"' if opacity is not None else ""
    return (
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" '
        f'stroke="{stroke}" stroke-width="{width}" fill="{fill}"{opacity_attr} />'
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


def _svg_image_with_white_outline(href: str, x_center: float, y_center: float, size_px: float) -> str:
    half = size_px / 2.0
    return (
        f'<image href="{escape(href)}" '
        f'x="{_fmt(x_center - half)}" y="{_fmt(y_center - half)}" '
        f'width="{_fmt(size_px)}" height="{_fmt(size_px)}" '
        f'preserveAspectRatio="xMidYMid meet" '
        f'filter="url(#glyphWhiteOutline)" />'
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


def _svg_polyline(points, stroke="#000", width=1, fill="none", dash=None, linecap="round", linejoin="round") -> str:
    pts = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-linecap="{linecap}" stroke-linejoin="{linejoin}"{dash_attr} />'
    )


def _extract_domitudes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []

    data = None
    for key in ("domitudes", "domitude", "dom", "doms"):
        val = payload.get(key)
        if isinstance(val, list):
            data = val
            break

    if data is None:
        val = payload.get("planets")
        if isinstance(val, list):
            data = val

    if data is None:
        return []

    out = []
    for item in data:
        if not isinstance(item, dict):
            continue
        name = item.get("planete") or item.get("planet") or item.get("name")
        if not name:
            continue
        val = (
            item.get("domitude_deg")
            or item.get("dom")
            or item.get("dm")
            or item.get("lon")
        )
        try:
            dom_deg = float(val)
        except Exception:
            continue

        pos_house = item.get("pos_maison_deg")
        try:
            pos_house_val = float(pos_house) if pos_house is not None else None
        except Exception:
            pos_house_val = None

        out.append({
            "name": name,
            "dom": _norm_deg(dom_deg),
            "raw": item,
            "pos_house": pos_house_val,
        })

    out.sort(key=lambda d: d["dom"])
    return out


def _extract_sign_domitudes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []

    data = (
        payload.get("sign_domitudes")
        or payload.get("dom_signs")
        or payload.get("signs_domitude")
    )
    if not data:
        return []

    out = []
    for item in data:
        if not isinstance(item, dict):
            continue

        name = item.get("signe") or item.get("sign") or item.get("name")
        if not name:
            continue

        val = (
            item.get("domitude_deg")
            or item.get("dom")
            or item.get("dm")
            or item.get("lon")
        )
        try:
            dom_deg = float(val)
        except Exception:
            continue

        out.append({
            "name": name,
            "dom": _norm_deg(dom_deg),
            "raw": item,
        })

    out.sort(key=lambda d: d["dom"])
    return out


def _planet_href(asset_base_url: str, planet_name: str) -> str | None:
    filename = PLANET_FILES.get(planet_name)
    if not filename:
        return None
    return f"{asset_base_url}/Planetes/{filename}"


def _axis_href(asset_base_url: str, axis_label: str, language: str) -> str | None:
    files = AXIS_FILES_EN if language == "en" else AXIS_FILES_FR
    filename = files.get(axis_label)
    if not filename:
        return None
    return f"{asset_base_url}/Axes/{filename}"


def _house_href(asset_base_url: str, house_num: int) -> str | None:
    filename = HOUSE_FILES.get(str(house_num))
    if not filename:
        return None
    return f"{asset_base_url}/Maisons/{filename}"


def _sign_domitude_href(asset_base_url: str, sign_name: str) -> str | None:
    filename = SIGN_FILES_DOM.get(sign_name)
    if not filename:
        return None
    return f"{asset_base_url}/Signes_domitude/{filename}"


def render_domitude_svg(
    payload: dict[str, Any],
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    show_title: bool = True,
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    title = "Thème de domitude" if language != "en" else "Domitude chart"

    w = width
    h = height
    margin = 20

    cx = w / 2
    cy = h / 2

    size0 = min(w, h) - 2 * margin
    SCALE_THEME = 0.80
    size = int(size0 * SCALE_THEME)

    r_outer = size * 0.36
    r_inner = size * 0.23
    r_outer_houses = size * 0.33

    PX_PLANET = int(size * 0.050)
    PX_AXIS = int(size * 0.050)
    PX_HOUSE = int(size * 0.090)

    outer_gap_min = int(size * 0.030)
    outer_gap_factor = 1.55
    outer_gap = max(outer_gap_min, int(PX_PLANET * outer_gap_factor))
    r_planet_base = r_outer + outer_gap

    GRID_STEP = 5
    GRID_BAND = size * 0.020
    CIRC_OUT_W = 3
    CIRC_IN_W = 3

    GAP_OUT = CIRC_OUT_W / 2.0
    GAP_IN = CIRC_IN_W / 2.0

    r_grid_out = r_outer - GAP_OUT
    r_grid_in = r_grid_out - GRID_BAND
    r_link_outer = (r_grid_in + r_grid_out) * 0.5

    r2_grid_in = r_inner + GAP_IN
    r2_grid_out = r2_grid_in + GRID_BAND
    r_link_inner = (r2_grid_in + r2_grid_out) * 0.5

    rot_deg = 0.0

    def to_screen(dom_deg: float) -> float:
        return _norm_deg(dom_deg + 90.0 + rot_deg)

    AXES_SCREEN = {
        "MC": to_screen(0.0),
        "AS": to_screen(90.0),
        "FC": to_screen(180.0),
        "DS": to_screen(270.0),
    }

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',
        '''
    <defs>
      <filter id="glyphWhiteOutline" x="-30%" y="-30%" width="160%" height="160%">
        <feMorphology in="SourceAlpha" operator="dilate" radius="1.8" result="dilated"/>
        <feFlood flood-color="#FFFFFF" result="white"/>
        <feComposite in="white" in2="dilated" operator="in" result="outline"/>
        <feMerge>
          <feMergeNode in="outline"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    ''',
    ]

    if show_title:
        parts.append(
            _svg_text(
                w / 2,
                22,
                title,
                size=24,
                fill=TITLE_COLOR,
                weight="700",
                baseline="hanging",
                family="Segoe UI, Arial, sans-serif",
            )
        )
    parts.append('<g transform="translate(0, 18)">')

    # Bandes/graduations externes
    for deg in range(0, 360, GRID_STEP):
        if deg % 30 == 0:
            continue
        a = to_screen(deg)
        x1, y1 = _pol_to_xy(cx, cy, r_grid_out, a)
        x2, y2 = _pol_to_xy(cx, cy, r_link_outer, a)
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#d0d0d0", width=1))

    # Bandes/graduations internes
    for deg in range(0, 360, GRID_STEP):
        if deg % 30 == 0:
            continue
        a = to_screen(deg)
        x1, y1 = _pol_to_xy(cx, cy, r2_grid_in, a)
        x2, y2 = _pol_to_xy(cx, cy, r_link_inner, a)
        parts.append(_svg_line(x1, y1, x2, y2, stroke="#d0d0d0", width=1))

    def _arc_5deg(R, a1, a2):
        start = a1
        end = a2
        if end < start:
            end += 360.0
        extent = end - start
        pts = _arc_points(cx, cy, R, start, extent, steps=8)
        return _svg_polyline(pts, stroke="#cfcfcf", width=1, fill="none")

    for house in range(12):
        base = house * 30
        for k in range(6):
            a1 = to_screen(base + k * 5)
            a2 = to_screen(base + (k + 1) * 5)
            parts.append(_arc_5deg(r_link_outer, a1, a2))
            parts.append(_arc_5deg(r_link_inner, a1, a2))

    # Limites des maisons
    for i in range(12):
        a = to_screen(i * 30.0)
        x1, y1 = _pol_to_xy(cx, cy, r_inner, a)
        x2, y2 = _pol_to_xy(cx, cy, r_outer, a)
        parts.append(_svg_line(x1, y1, x2, y2, stroke=STRUCT_GREY, width=3))

    parts.append(_svg_circle(cx, cy, r_outer, stroke=STRUCT_GREY, width=3))
    parts.append(_svg_circle(cx, cy, r_inner, stroke=STRUCT_GREY, width=3))

    # Petits signes de domitude autour de la couronne
    sign_dom_list = _extract_sign_domitudes(payload)
    if sign_dom_list:
        MARK_W_SIGN = max(2, int(size * 0.0035))
        LABEL_OFFSET_SIGN = int(size * 0.018)
        PX_SIGN = int(size * 0.018)

        for item in sign_dom_list:
            dom_deg = item["dom"]
            name = item["name"]
            a = to_screen(dom_deg)

            x1, y1 = _pol_to_xy(cx, cy, r_grid_out, a)
            x2, y2 = _pol_to_xy(cx, cy, r_link_outer, a)
            parts.append(
                _svg_line(
                    x1, y1, x2, y2,
                    stroke=HOUSE_MARK_COLOR,
                    width=MARK_W_SIGN,
                )
            )

            tx, ty = _pol_to_xy(cx, cy, r_outer + LABEL_OFFSET_SIGN, a)
            href = _sign_domitude_href(asset_base_url, name)
            if href:
                parts.append(_svg_image(href, tx, ty, PX_SIGN))

    # Glyphes des maisons
    for idx, house_num in enumerate([10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
        cusp_dom = idx * 30.0
        mid_dom = cusp_dom + 15.0
        a_mid = to_screen(mid_dom)
        band_mid = 0.5 * (r_inner + r_outer_houses)
        house_radius = band_mid + size * 0.010
        tx, ty = _pol_to_xy(cx, cy, house_radius, a_mid)

        href = _house_href(asset_base_url, house_num)
        if href:
            parts.append(_svg_image(href, tx, ty, PX_HOUSE))
        else:
            roman = ROMANS[(house_num - 1) % 12]
            parts.append(
                _svg_text(
                    tx, ty, roman,
                    size=int(size * 0.040),
                    fill=STRUCT_GREY,
                    weight="400",
                )
            )

    # Axes
    def draw_axis(label: str, dom_deg: float):
        AXIS_LEN_AS_DS = 0.22
        AXIS_LEN_MC_FC = 0.20
        axis_gap = int(size * (AXIS_LEN_AS_DS if label in ("AS", "DS") else AXIS_LEN_MC_FC))
        r_axes = r_outer + axis_gap
        BASE_AXIS_WIDTH = 3
        AXIS_WIDTH = BASE_AXIS_WIDTH + 1
        TICK_SIZE = int(size * 0.026)
        CAP_MC = int(size * 0.032)
        CAP_FC = int(size * 0.036)

        a = to_screen(dom_deg)
        r_axis_end = r_axes
        if label == "MC":
            r_axis_end = r_axes - CAP_MC - AXIS_WIDTH / 2
        elif label in ("FC", "IC"):
            r_axis_end = r_axes - CAP_FC - AXIS_WIDTH / 2

        x0, y0 = _pol_to_xy(cx, cy, r_outer, a)
        x1, y1 = _pol_to_xy(cx, cy, r_axis_end, a)

        parts.append(_svg_line(x0, y0, x1, y1, stroke="#222222", width=AXIS_WIDTH))

        if label == "AS":
            arrow_len = int(size * 0.060)
            arrow_open = 26
            a_rev = a + 180.0
            tip_x, tip_y = _pol_to_xy(cx, cy, r_axis_end, a)

            def pt_from(cx0, cy0, L, ang_deg):
                th = math.radians(ang_deg)
                return cx0 + L * math.cos(th), cy0 - L * math.sin(th)

            xL, yL = pt_from(tip_x, tip_y, arrow_len, a_rev + arrow_open)
            xR, yR = pt_from(tip_x, tip_y, arrow_len, a_rev - arrow_open)
            parts.append(_svg_line(tip_x, tip_y, xL, yL, stroke="#222222", width=AXIS_WIDTH))
            parts.append(_svg_line(tip_x, tip_y, xR, yR, stroke="#222222", width=AXIS_WIDTH))

        elif label == "DS":
            tip_x, tip_y = _pol_to_xy(cx, cy, r_axis_end, a)
            ux = math.cos(math.radians(a + 90))
            uy = math.sin(math.radians(a + 90))
            xL = tip_x - TICK_SIZE * ux
            yL = tip_y + TICK_SIZE * uy
            xR = tip_x + TICK_SIZE * ux
            yR = tip_y - TICK_SIZE * uy
            parts.append(_svg_line(xL, yL, xR, yR, stroke="#222222", width=AXIS_WIDTH))

        elif label == "MC":
            xc, yc = _pol_to_xy(cx, cy, r_axes, a)
            parts.append(_svg_circle(xc, yc, CAP_MC, stroke="#222222", width=AXIS_WIDTH))

        elif label in ("FC", "IC"):
            xc, yc = _pol_to_xy(cx, cy, r_axes, a)
            pts = _arc_points(xc, yc, CAP_FC, a + 90, 180, steps=24)
            parts.append(_svg_polyline(pts, stroke="#222222", width=AXIS_WIDTH, fill="none"))

        if label in ("MC", "FC", "IC"):
            gx, gy = _pol_to_xy(cx, cy, r_axes, a)
        else:
            half_glyph = int(PX_AXIS * 0.5)
            margin2 = int(size * 0.008)
            offset = half_glyph + margin2
            gx, gy = _pol_to_xy(cx, cy, r_axis_end + offset, a)

        href = _axis_href(asset_base_url, label, language)
        if href:
            parts.append(_svg_image(href, gx, gy, PX_AXIS))

    axis_MC = "MC"
    axis_AS = "AS"
    axis_DS = "DS"
    axis_FC = "IC" if language == "en" else "FC"

    # Planètes
    dom_list = _extract_domitudes(payload)
    if not dom_list:
        parts.append("</svg>")
        return "".join(parts)

    PX_PLANET = int(size * 0.050)
    r_planet = r_planet_base
    LINE_W = 2
    ELBOW_OUT = int(size * 0.022)
    MARGIN_OBLIQUE = 4.0

    planets_info = []
    for item in dom_list:
        name = item["name"]
        ang_real = to_screen(item["dom"])
        px_target = int(PX_PLANET * PERCEPTION_COEFFS.get(name, 1.0))
        planets_info.append({
            "name": name,
            "real": ang_real,
            "adj": ang_real,
            "px": px_target,
            "crowded": False,
            "pos_house": item.get("pos_house"),
        })


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


    def _ang_short(a, b):
        return abs((b - a + 180.0) % 360.0 - 180.0)


    def _pair_orb_conj_deg(n1, n2):
        g1_n1 = n1 in G1_RAPIDES
        g1_n2 = n2 in G1_RAPIDES
        if g1_n1 and g1_n2:
            return ORB_CONJ_G1G1
        if (g1_n1 and (not g1_n2)) or ((not g1_n1) and g1_n2):
            return ORB_CONJ_G1G2
        return ORB_CONJ_G2G2


    def _pair_visual_min_deg(wi_px, wj_px):
        return _deg_from_px(1.00 * (wi_px + wj_px), r_planet)


    def _pair_dynamic_threshold(pL, pR):
        orb_deg = _pair_orb_conj_deg(pL["name"], pR["name"])
        vis_min = _pair_visual_min_deg(pL["px"], pR["px"])
        return max(vis_min, K_PROX * orb_deg)

    planets_info.sort(key=lambda d: d["real"])
    groups = []
    cur = [planets_info[0]]
    for k in range(1, len(planets_info)):
        L = planets_info[k - 1]
        R = planets_info[k]
        thr = _pair_dynamic_threshold(L, R)
        if _ang_short(L["real"], R["real"]) < thr:
            cur.append(R)
        else:
            groups.append(cur)
            cur = [R]
    groups.append(cur)

    if len(groups) > 1:
        L_last = groups[-1][-1]
        R_first = groups[0][0]
        thr_lr = _pair_dynamic_threshold(L_last, R_first)
        if _ang_short(L_last["real"], R_first["real"]) < thr_lr:
            groups[0] = groups[-1] + groups[0]
            groups.pop()


    def _min_current_gap_deg(grp):
        if len(grp) < 2:
            return 360.0
        grp_sorted = sorted(grp, key=lambda d: d["adj"])
        gaps = []
        for i in range(len(grp_sorted) - 1):
            a = grp_sorted[i]["adj"]
            b = grp_sorted[i + 1]["adj"]
            gaps.append(_ang_short(a, b))
        a_last = grp_sorted[-1]["adj"]
        a_first = grp_sorted[0]["adj"]
        gaps.append(_ang_short(a_last, a_first))
        return min(gaps) if gaps else 360.0


    def _max_needed_gap_deg(grp):
        need = 0.0
        for i in range(len(grp) - 1):
            wi = grp[i]["px"]
            wj = grp[i + 1]["px"]
            need = max(need, _deg_from_px(0.85 * (wi + wj), r_planet))
        return need


    for grp in groups:
        if len(grp) == 1:
            grp[0]["crowded"] = False
            grp[0]["adj"] = grp[0]["real"]
            continue

        min_current = _min_current_gap_deg(grp)
        max_needed = _max_needed_gap_deg(grp)

        if min_current >= max_needed:
            for d in grp:
                d["crowded"] = False
            continue

        angles_adj = [d["adj"] for d in grp]
        mid = _circ_mean(angles_adj)

        if len(grp) > 1:
            spacing = max_needed / (len(grp) - 1)
        else:
            spacing = 0.0

        start = (mid - spacing * (len(grp) - 1) / 2.0)
        for j, d in enumerate(grp):
            d["adj"] = (start + j * spacing) % 360.0
            d["crowded"] = True


    for grp in groups:
        if len(grp) <= 1:
            if len(grp) == 1:
                grp[0]["crowded"] = False
            continue

        real_list = [d["real"] for d in grp]
        px_list = [d["px"] for d in grp]
        gaps_min = [_deg_from_px(0.85 * (px_list[i] + px_list[i + 1]), r_planet) for i in range(len(grp) - 1)]
        span_min = sum(gaps_min)

        grp_sorted = sorted(grp, key=lambda d: d["adj"])
        span_cur = (grp_sorted[-1]["adj"] - grp_sorted[0]["adj"]) % 360.0
        if span_cur > 180.0:
            span_cur = 360.0 - span_cur

        mid = _circ_mean(real_list)

        if len(grp) > 1:
            spacing = span_min / (len(grp) - 1)
        else:
            spacing = 0.0

        start = mid - spacing * (len(grp) - 1) / 2.0
        targets = [(start + j * spacing) % 360.0 for j in range(len(grp))]

        span_target = spacing * (len(grp) - 1)
        span_cap = max(span_min, span_cur * (1.0 + SPAN_MARGIN_RATIO))
        if span_target > span_cap and len(grp) > 1:
            spacing *= (span_cap / span_target)
            start = mid - spacing * (len(grp) - 1) / 2.0
            targets = [(start + j * spacing) % 360.0 for j in range(len(grp))]

        for j, d in enumerate(grp):
            real = d["real"]
            target = targets[j]
            delta = ((target - real + 180.0) % 360.0) - 180.0
            max_delta = DELTA_CAP_RATIO * _deg_from_px(d["px"], r_planet)
            if delta > max_delta:
                delta = max_delta
            if delta < -max_delta:
                delta = -max_delta

            if len(grp) > 1:
                t_pos = j / (len(grp) - 1)
                edge_factor = 0.35 + 0.65 * math.sin(math.pi * t_pos)
            else:
                edge_factor = 1.0

            d["adj"] = (real + edge_factor * K_PUSH * delta + 360.0) % 360.0
            d["crowded"] = True

    for grp in groups:
        if len(grp) <= 1:
            continue

        real_list = [d["real"] for d in grp]
        adj_list = [d["adj"] for d in grp]
        mid = _circ_mean(real_list)
        real_un = _unwrap_around(mid, real_list)
        adj_un = _unwrap_around(mid, adj_list)

        idx_sorted_real = sorted(range(len(grp)), key=lambda i: real_un[i])
        adj_sorted_vals = sorted(adj_un)

        for rank, idx in enumerate(idx_sorted_real):
            new_ang = adj_sorted_vals[rank]
            grp[idx]["adj"] = (new_ang + 360.0) % 360.0
            grp[idx]["crowded"] = True

    if len(planets_info) >= 2:
        angles_adj = [d["adj"] for d in planets_info]
        mid = _circ_mean(angles_adj)
        lin = _unwrap_around(mid, angles_adj)
        order = sorted(range(len(planets_info)), key=lambda idx: lin[idx])
        lin_all = lin[:]
        for _iter in range(2):
            for k in range(1, len(order)):
                i_prev = order[k - 1]
                i_cur = order[k]
                a_prev = lin_all[i_prev]
                a_cur = lin_all[i_cur]
                min_gap = _deg_from_px(
                    0.60 * (planets_info[i_prev]["px"] + planets_info[i_cur]["px"]),
                    r_planet,
                )
                gap = a_cur - a_prev
                if gap < min_gap:
                    shift = (min_gap - gap)
                    lin_all[i_prev] -= 0.5 * shift
                    lin_all[i_cur] += 0.5 * shift

        for i, d in enumerate(planets_info):
            d["adj"] = (lin_all[i] + 360.0) % 360.0


    # Dessiner les axes avant les glyphes planétaires, style AstroAriana
    draw_axis(axis_MC, 0.0)
    draw_axis(axis_AS, 90.0)
    draw_axis(axis_FC, 180.0)
    draw_axis(axis_DS, 270.0)

    planets_info_sorted = sorted(planets_info, key=lambda d: d["real"])

    for d in planets_info_sorted:
        name = d["name"]
        ang_band = d["real"]
        ang_glyph = d["adj"]

        pxg, pyg = _pol_to_xy(cx, cy, r_planet, ang_glyph)
        half_px = 0.5 * d["px"]

        pos_house = d.get("pos_house")
        if pos_house is not None:
            try:
                n = int(round(float(pos_house))) % 30
                r_text = r_planet + int(size * 0.046)
                tx, ty = _pol_to_xy(cx, cy, r_text, ang_glyph)
                parts.append(
                    _svg_text(
                        tx, ty, str(n),
                        size=max(11, int(size * 0.017)),
                        fill=STRUCT_GREY,
                    )
                )
            except Exception:
                pass

        if d["crowded"]:
            elbow_r = r_outer + ELBOW_OUT
            for start_r in (r_grid_out, r_link_outer):
                xb0, yb0 = _pol_to_xy(cx, cy, start_r, ang_band)
                xb1, yb1 = _pol_to_xy(cx, cy, elbow_r, ang_band)
                parts.append(_svg_line(xb0, yb0, xb1, yb1, stroke=STRUCT_GREY, width=LINE_W))

            xb1, yb1 = _pol_to_xy(cx, cy, elbow_r, ang_band)
            dx, dy = pxg - xb1, pyg - yb1
            dist = math.hypot(dx, dy)
            stop_from_elbow = max(dist - (half_px + MARGIN_OBLIQUE), 0.0)
            if dist > 0 and stop_from_elbow > 0:
                t = stop_from_elbow / dist
                xo, yo = xb1 + dx * t, yb1 + dy * t
                parts.append(_svg_line(xb1, yb1, xo, yo, stroke=STRUCT_GREY, width=LINE_W))
        else:
            xb0, yb0 = _pol_to_xy(cx, cy, r_link_outer, ang_band)
            xb1, yb1 = _pol_to_xy(cx, cy, r_outer + ELBOW_OUT, ang_band)
            parts.append(_svg_line(xb0, yb0, xb1, yb1, stroke=STRUCT_GREY, width=LINE_W))

            dx, dy = pxg - xb1, pyg - yb1
            dist = math.hypot(dx, dy)
            stop_from_elbow = max(dist - (half_px + MARGIN_OBLIQUE), 0.0)
            if dist > 0 and stop_from_elbow > 0:
                t = stop_from_elbow / dist
                xo, yo = xb1 + dx * t, yb1 + dy * t
                parts.append(_svg_line(xb1, yb1, xo, yo, stroke=STRUCT_GREY, width=LINE_W))


        href = _planet_href(asset_base_url, name)
        if href:
            parts.append(_svg_image_with_white_outline(href, pxg, pyg, d["px"]))
        else:
            parts.append(
                _svg_text(
                    pxg, pyg, name[:1],
                    size=10,
                    fill="#000000",
                    weight="700",
                )
            )

    parts.append("</g>")
    parts.append("</svg>")
    return "".join(parts)

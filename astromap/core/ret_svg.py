from __future__ import annotations

from html import escape
from typing import Any

from .ret_hp import compute_planet_hierarchy, compute_ret_box_colors
from .signs_hierarchy import rank_signs
from .ret_families import compute_ret_ranking

TITLE_COLOR = "#1f4fa3"
TEXT_COLOR = "#111111"
BLACK = "#000000"
MID_GREY = "#A0A0A0"

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

RET_PLANET_CODE_COLORS = {
    "Lune":    ("#ffffff", None),
    "Soleil":  ("#ffd000", "#ffd000"),
    "Mercure": ("#ffd000", "#0090ff"),
    "Vénus":   ("#ffd000", "#ff3c2f"),
    "Mars":    ("#ff3c2f", "#ff3c2f"),
    "Jupiter": ("#ff3c2f", "#ffd000"),
    "Saturne": ("#ff3c2f", "#0090ff"),
    "Uranus":  ("#0090ff", "#ffd000"),
    "Neptune": ("#0090ff", "#ff3c2f"),
    "Pluton":  ("#0090ff", "#0090ff"),
}

RET_FAMILY_CODE_FROM_STR = {
    "R": "R",
    "Représentation extensive (R)": "R",
    "Extensive representation (R)": "R",
    "r": "r",
    "représentation intensive (r)": "r",
    "Intensive representation (r)": "r",
    "E": "E",
    "Existence extensive (E)": "E",
    "Extensive existence (E)": "E",
    "e": "e",
    "existence intensive (e)": "e",
    "Intensive existence (e)": "e",
    "T": "T",
    "Transcendance extensive (T)": "T",
    "Extensive transcendence (T)": "T",
    "t": "t",
    "transcendance intensive (t)": "t",
    "Intensive transcendence (t)": "t",
    "P": "P",
    "Pouvoir extensif (P)": "P",
    "Extensive power (P)": "P",
    "p": "p",
    "pouvoir intensif (p)": "p",
    "Intensive power (p)": "p",
}

RET_FAMILY_MARKERS = {
    "r": ("circle",  "#ffd000"),
    "R": ("diamond", "#ffd000"),
    "e": ("circle",  "#ff3c2f"),
    "E": ("diamond", "#ff3c2f"),
    "t": ("circle",  "#0090ff"),
    "T": ("diamond", "#0090ff"),
    "p": ("circle",  "#ffffff"),
    "P": ("diamond", "#404040"),
}

PLANET_LABELS = {
    "FR": {
        "Soleil": "Soleil",
        "Lune": "Lune",
        "Mercure": "Mercure",
        "Vénus": "Vénus",
        "Mars": "Mars",
        "Jupiter": "Jupiter",
        "Saturne": "Saturne",
        "Uranus": "Uranus",
        "Neptune": "Neptune",
        "Pluton": "Pluton",
    },
    "EN": {
        "Soleil": "Sun",
        "Lune": "Moon",
        "Mercure": "Mercury",
        "Vénus": "Venus",
        "Mars": "Mars",
        "Jupiter": "Jupiter",
        "Saturne": "Saturn",
        "Uranus": "Uranus",
        "Neptune": "Neptune",
        "Pluton": "Pluto",
    },
}

GLYPH_SCALE_RET = {
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

LEFT_PLANET_SCALE = {
    "Soleil": 0.95,
    "Lune": 1.00,
    "Mercure": 1.05,
    "Vénus": 1.00,
    "Mars": 0.95,
    "Jupiter": 1.00,
    "Saturne": 1.00,
    "Uranus": 1.00,
    "Neptune": 1.00,
    "Pluton": 1.00,
}

PERCEPTION_COEFFS_SIGNS = {
    "Bélier": 1.00,
    "Taureau": 1.02,
    "Gémeaux": 0.95,
    "Cancer": 1.00,
    "Lion": 1.08,
    "Vierge": 1.05,
    "Balance": 1.00,
    "Scorpion": 1.08,
    "Sagittaire": 0.92,
    "Capricorne": 1.00,
    "Verseau": 1.00,
    "Poissons": 1.00,
}

LEFT_RANK_SIZE = 16
RIGHT_RANK_SIZE = 16
RIGHT_CODE_SIZE = 19
RIGHT_LABEL_SIZE = 14
BOTTOM_LABEL_SIZE = 15

def _fmt(v: float) -> str:
    return f"{v:.2f}"

def _svg_text(
    x: float,
    y: float,
    text: str,
    *,
    size: int = 12,
    fill: str = TEXT_COLOR,
    weight: str = "normal",
    anchor: str = "middle",
    baseline: str = "middle",
    family: str = "Segoe UI, Arial, sans-serif",
    rotate: float | None = None,
) -> str:
    transform = ""
    if rotate is not None:
        transform = f' transform="rotate({rotate} {_fmt(x)} {_fmt(y)})"'

    return (
        f'<text x="{_fmt(x)}" y="{_fmt(y)}"{transform} '
        f'font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="{baseline}">'
        f"{escape(str(text))}</text>"
    )

def _svg_circle(cx: float, cy: float, r: float, *, fill="#fff", stroke="#000", width=1) -> str:
    return (
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}" />'
    )


def _svg_diamond(cx: float, cy: float, size: float, *, fill="#fff", stroke="#000", width=1) -> str:
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

def _planet_href_for_box(asset_base_url: str, planet_name: str, box_code: str) -> str | None:
    fn = PLANET_FILES.get(planet_name)
    if not fn:
        return None

    if box_code == "black":
        chosen = fn.replace(".svg", "_blanc.svg")
    else:
        chosen = fn.replace(".svg", "_noir.svg")

    return f"{asset_base_url}/Planetes/{chosen}"
    
def _sign_href(asset_base_url: str, sign_name: str) -> str | None:
    fn = SIGN_FILES.get(sign_name)
    return f"{asset_base_url}/Signes/{fn}" if fn else None


def _planet_label(name: str, language: str) -> str:
    lang = "EN" if language.lower().startswith("en") else "FR"
    return PLANET_LABELS[lang].get(name, name)


def _extract_angular_set(dom_payload: dict[str, Any] | None) -> set[str]:
    angular = set()
    if not dom_payload:
        return angular
    for d in dom_payload.get("domitudes", []) or []:
        if d.get("est_angulaire"):
            p = d.get("planete")
            if p:
                angular.add(p)
    return angular


def _planet_signs(theme_payload: dict[str, Any], dom_payload: dict[str, Any] | None) -> dict[str, str]:
    out: dict[str, str] = {}
    planets = theme_payload.get("planets", []) or []
    domitudes = (dom_payload or {}).get("domitudes", []) or []

    dom_by_name = {
        d.get("planete") or d.get("planet") or d.get("name"): d
        for d in domitudes
    }

    signs = [
        "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
        "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"
    ]

    for p in planets:
        name = (
            p.get("name")
            or p.get("planet")
            or p.get("planete")
            or p.get("nom")
            or p.get("label")
        )
        if not name:
            continue

        sign_name = None
        dom = dom_by_name.get(name)
        if dom:
            sign_name = (
                dom.get("sign_local")
                or dom.get("signe_local")
                or dom.get("sign")
                or dom.get("signe")
            )

        if sign_name is None:
            lon = p.get("lon") or p.get("longitude") or p.get("ecliptic_lon")
            try:
                lon_deg = float(lon)
                sign_name = signs[int((lon_deg % 360.0) // 30)]
            except Exception:
                sign_name = None

        if sign_name:
            out[name] = sign_name

    fr_to_en = PLANET_LABELS["EN"]
    en_to_fr = {v: k for k, v in fr_to_en.items()}

    aliases: dict[str, str] = {}
    for pname, sname in out.items():
        aliases[pname] = sname
        if pname in fr_to_en:
            aliases[fr_to_en[pname]] = sname
        if pname in en_to_fr:
            aliases[en_to_fr[pname]] = sname

    return aliases


def _draw_left_planet_code(planet_name: str, cx: float, cy: float, size: float = 24.0) -> str:
    colors = RET_PLANET_CODE_COLORS.get(planet_name)
    if not colors:
        return ""
    diamond_color, circle_color = colors
    parts = [_svg_diamond(cx, cy, size, fill=diamond_color, stroke="#000000", width=1)]
    if circle_color is not None:
        r = size * 0.52
        parts.append(_svg_circle(cx, cy, r, fill=circle_color, stroke="#000000", width=1))
    return "".join(parts)


def _draw_center_cell(planet_name: str, box_code: str, cx: float, cy: float, cell_size: float, asset_base_url: str) -> str:
    if box_code == "black":
        fill = "#000000"
    elif box_code in ("gray", "grey"):
        fill = MID_GREY
    else:
        fill = "#FFFFFF"

    parts = [
        _svg_diamond(cx, cy, cell_size / 2.0, fill=fill, stroke="#000000", width=2)
    ]

    href = _planet_href_for_box(asset_base_url, planet_name, box_code)
    scale = GLYPH_SCALE_RET.get(planet_name, 1.0)
    glyph_px = 36.0 * scale

    if href:
        parts.append(_svg_image(href, cx, cy, glyph_px))
    else:
        parts.append(
            _svg_text(
                cx, cy, planet_name[:2],
                size=24,
                fill="#FFFFFF" if fill == "#000000" else "#000000",
                weight="700",
            )
        )
    return "".join(parts)


def render_ret_svg(
    theme_payload: dict[str, Any],
    dom_payload: dict[str, Any] | None = None,
    width: int = 1400,
    height: int = 900,
    *,
    language: str = "fr",
    asset_base_url: str = "https://astromap-api-production.up.railway.app/glyphes",
) -> str:
    ranks, ordered_planets, _info = compute_planet_hierarchy(theme_payload, dom_payload)
    angular_set = _extract_angular_set(dom_payload)
    aspects = theme_payload.get("aspects", []) or []
    box_colors = compute_ret_box_colors(ordered_planets, angular_set, aspects)
    sign_rank = rank_signs(theme_payload.get("planets", []) or [], ranks)
    ret_order, _ret_details = compute_ret_ranking(ranks)
    planet_signs = _planet_signs(theme_payload, dom_payload)

    title = "RET et Hiérarchie Planétaire" if language.lower().startswith("fr") else "RET and Planetary Hierarchy"

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FFFFFF" />',

        _svg_text(
            width / 2.0,
            22,
            title,
            size=22,
            fill=TITLE_COLOR,
            weight="700",
            baseline="hanging",
            family="Segoe UI, Arial, sans-serif",
        ),
    ]

    left_margin = 110
    top = 120
    line_h = 48
    max_num_width = 30
    padding_num_glyph = 24

    col_planets_x = left_margin
    col_ret_x = col_planets_x + 420
    col_signs_x = col_ret_x + 360

    planet_glyph_x = col_planets_x + max_num_width + padding_num_glyph
    diamond_center_x = planet_glyph_x + 58
    sign_x = diamond_center_x + 34

    small_planet_px = 34
    small_sign_px = 15

    for rank, pname in enumerate(ordered_planets[:10], start=1):
        line_center_y = top + (rank - 1) * line_h + line_h / 2.0

        parts.append(
            _svg_text(
                col_planets_x,
                line_center_y,
                f"{rank}.",
                size=LEFT_RANK_SIZE,
                fill="#000000",
                weight="700",
                anchor="start",
            )
        )

        href_p = _planet_href_for_box(asset_base_url, pname, "white")
        if href_p:
            scale = LEFT_PLANET_SCALE.get(pname, 1.0)
            parts.append(_svg_image(href_p, planet_glyph_x, line_center_y, small_planet_px * scale))
        else:
            parts.append(
                _svg_text(
                    planet_glyph_x,
                    line_center_y,
                    _planet_label(pname, language),
                    size=LEFT_RANK_SIZE,
                    weight="700",
                )
            )

        parts.append(_draw_left_planet_code(pname, diamond_center_x, line_center_y, 22.0))

        sign_name = planet_signs.get(pname)
        href_s = _sign_href(asset_base_url, sign_name) if sign_name else None
        if href_s:
            coeff = PERCEPTION_COEFFS_SIGNS.get(sign_name, 1.0)
            parts.append(_svg_image(href_s, sign_x, line_center_y, small_sign_px * coeff))

    diamond_cx = col_ret_x + 20
    diamond_cy = top + 290
    cell_size = 105.0
    step = cell_size * 0.50

    positions = {
        "Lune":    (0, -4),
        "Soleil":  (0, -2),
        "Jupiter": (-1, -1),
        "Vénus":   (1, -1),
        "Uranus":  (-2,  0),
        "Mars":    (0,   0),
        "Mercure": (2,   0),
        "Neptune": (-1,  1),
        "Saturne": (1,   1),
        "Pluton":  (0,   2),
    }

    for planet_name, (dx, dy) in positions.items():
        box_code = box_colors.get(planet_name)
        if box_code is None:
            continue
        cx = diamond_cx + dx * step
        cy = diamond_cy + dy * step
        parts.append(_draw_center_cell(planet_name, box_code, cx, cy, cell_size, asset_base_url))

    letters = {
        "R": (-0.75, -2.75, -45),
        "E": (-1.75, -1.75, -45),
        "T": (-2.75, -0.75, -45),

        "r": (0.75, -2.75, 45),
        "e": (1.75, -1.75, 45),
        "t": (2.75, -0.75, 45),

        "p": (0.0, -5.55, 0),
        "P": (0.0, 3.35, 0),
    }

    for txt, (dx, dy, angle) in letters.items():
        parts.append(
            _svg_text(
                diamond_cx + dx * step,
                diamond_cy + dy * step,
                txt,
                size=19 if txt in {"T", "E", "R", "r", "e", "t"} else 18,
                fill="#000000",
                weight="700",
                rotate=angle,
            )
        )

    right_y0 = top + 10
    right_dy = 50
    marker_size = 21

    family_labels_fr = {
        "E": "Existence extensive",
        "p": "pouvoir intensif",
        "e": "existence intensive",
        "R": "Représentation extensive",
        "r": "représentation intensive",
        "t": "transcendance intensive",
        "P": "Pouvoir extensif",
        "T": "Transcendance extensive",
    }

    family_labels_en = {
        "E": "Extensive existence",
        "p": "Intensive power",
        "e": "Intensive existence",
        "R": "Extensive representation",
        "r": "Intensive representation",
        "t": "Intensive transcendence",
        "P": "Extensive power",
        "T": "Extensive transcendence",
    }

    fam_labels = family_labels_en if language.lower().startswith("en") else family_labels_fr

    for i, fam in enumerate(ret_order[:8], start=1):
        y = right_y0 + i * right_dy
        code = RET_FAMILY_CODE_FROM_STR.get(fam, fam)
        shape, color = RET_FAMILY_MARKERS[code]

        parts.append(
            _svg_text(
                col_signs_x,
                y,
                f"{i}.",
                size=RIGHT_RANK_SIZE,
                weight="700",
                anchor="start",
            )
        )

        marker_x = col_signs_x + 38
        if shape == "circle":
            parts.append(_svg_circle(marker_x, y, 12, fill=color, stroke="#000000", width=1))
        else:
            parts.append(_svg_diamond(marker_x, y, marker_size, fill=color, stroke="#000000", width=1))

        parts.append(
            _svg_text(
                col_signs_x + 68,
                y,
                code,
                size=RIGHT_CODE_SIZE,
                weight="700",
                anchor="start",
            )
        )

        parts.append(
            _svg_text(
                col_signs_x + 92,
                y,
                f"({fam_labels.get(code, code)})",
                size=RIGHT_LABEL_SIZE,
                weight="700",
                anchor="start",
            )
        )
 
    base_y = top + 10 * line_h + 80

    dominant_planets = [p for p in ordered_planets if box_colors.get(p) == "black"]
    parts.append(
        _svg_text(
            left_margin,
            base_y,
            "Planètes dominantes :",
            size=BOTTOM_LABEL_SIZE,
            weight="700",
            anchor="start",
        )
    )

    x_cursor = left_margin + 210
    for p in dominant_planets:
        href = _planet_href_for_box(asset_base_url, p, "white")
        if href:
            parts.append(_svg_image(href, x_cursor, base_y, 34))
            x_cursor += 34

    parts.append(
        _svg_text(
            left_margin,
            base_y + 40,
            "Signes dominants :",
            size=BOTTOM_LABEL_SIZE,
            weight="700",
            anchor="start",
        )
    )

    x_cursor = left_margin + 190
    for sign_name, score in sign_rank:
        if score > 15:
            href = _sign_href(asset_base_url, sign_name)
            if href:
                coeff = PERCEPTION_COEFFS_SIGNS.get(sign_name, 1.0)
                parts.append(_svg_image(href, x_cursor, base_y + 40, 28 * coeff))
                x_cursor += 36

    parts.append("</svg>")
    return "".join(parts)

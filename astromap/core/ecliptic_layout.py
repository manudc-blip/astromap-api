from __future__ import annotations

import math
from typing import Any


SIGN_NAMES = [
    "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
    "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons",
]

ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

SHOW_ASPECT_CURSORS = True
STRUCT_GREY = "#4A4A4A"

# === Grouping (amas) : paramètres RÉGLABLES ===
K_PROX = 0.75
ORB_CONJ_G1G1 = 18.0
ORB_CONJ_G1G2 = 16.0
ORB_CONJ_G2G2 = 14.0

# === Soft packing ===
K_PUSH = 0.90
DELTA_CAP_RATIO = 1.60
SPAN_MARGIN_RATIO = 0.15

G1_RAPIDES = {"Soleil", "Lune", "Mercure", "Vénus", "Mars"}
G2_LENTES = {"Jupiter", "Saturne", "Uranus", "Neptune", "Pluton"}

SHOW_HOUSE_SPOKES = False
HOUSES_SKIP_FOR_AXES = {1, 4, 7, 10}
HOUSE_MARK_LEN = 12
HOUSE_MARK_COLOR = "#0b3d91"
HOUSE_MARK_WIDTH = 2

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

PERCEPTION_COEFFS_SIGNS = {
    "Bélier": 1.00,
    "Taureau": 1.02,
    "Gémeaux": 0.92,
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


def _pol_to_xy(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    th = math.radians(deg)
    return (cx + r * math.cos(th), cy - r * math.sin(th))


def _norm_deg(d: float) -> float:
    return d % 360.0


def _circ_mean(degs: list[float]) -> float:
    sx = sum(math.cos(math.radians(d)) for d in degs)
    sy = sum(math.sin(math.radians(d)) for d in degs)
    if sx == 0 and sy == 0:
        return (degs[0] + 360.0) % 360.0
    return (math.degrees(math.atan2(sy, sx)) + 360.0) % 360.0


def _unwrap_around(ref: float, degs: list[float]) -> list[float]:
    out: list[float] = []
    for d in degs:
        x = d
        while x - ref >= 180.0:
            x -= 360.0
        while x - ref < -180.0:
            x += 360.0
        out.append(x)
    return out


def _ang_short(a: float, b: float) -> float:
    return abs((b - a + 180.0) % 360.0 - 180.0)


def _deg_from_px(px_len: float, radius: float) -> float:
    return (px_len / (2 * math.pi * radius)) * 360.0


def _pair_orb_conj_deg(n1: str, n2: str) -> float:
    if (n1 in G1_RAPIDES) and (n2 in G1_RAPIDES):
        return ORB_CONJ_G1G1
    if (n1 in G2_LENTES) and (n2 in G2_LENTES):
        return ORB_CONJ_G2G2
    return ORB_CONJ_G1G2


def _pair_visual_min_deg(wi_px: float, wj_px: float, r_planet: float) -> float:
    return _deg_from_px(1.00 * (wi_px + wj_px), r_planet)


def _pair_dynamic_threshold(p_left: dict[str, Any], p_right: dict[str, Any], r_planet: float) -> float:
    orb_deg = _pair_orb_conj_deg(p_left["name"], p_right["name"])
    vis_min = _pair_visual_min_deg(p_left["px"], p_right["px"], r_planet)
    return max(vis_min, K_PROX * orb_deg)


def _extract_axis(axes: dict[str, Any], *names: str) -> float | None:
    for key in names:
        if key in axes:
            try:
                return float(axes[key])
            except Exception:
                pass
    return None


def _planet_is_retrograde(planet_payload: dict[str, Any]) -> bool:
    for key in ("retro", "retrograde", "rflag"):
        if key in planet_payload:
            val = planet_payload.get(key)
            if isinstance(val, bool):
                return val
            try:
                return bool(int(val))
            except Exception:
                if isinstance(val, str) and val.upper().startswith("R"):
                    return True

    dm = planet_payload.get("daily_motion")
    try:
        return dm is not None and float(dm) < 0
    except Exception:
        return False


def _build_title(language: str, title_suffix: str = "", show_title: bool = True) -> str | None:
    if not show_title:
        return None
    title = "Thème écliptique" if language == "fr" else "Ecliptic chart"
    return title + (title_suffix or "")


def build_ecliptic_layout(
    payload: dict[str, Any],
    width: int,
    height: int,
    *,
    language: str = "fr",
    margin: int = 30,
    show_title: bool = True,
    title_suffix: str = "",
    show_houses: bool = True,
    show_aspects: bool = True,
) -> dict[str, Any]:
    """
    Renvoie une structure de layout purement géométrique, sans Tkinter.
    Le frontend web ou un générateur SVG pourra s'en servir tel quel.
    """
    if not payload or not payload.get("planets"):
        return {
            "ok": False,
            "reason": "missing_planets",
        }

    if width < 200 or height < 200:
        return {
            "ok": False,
            "reason": "canvas_too_small",
        }

    axes = dict(payload.get("axes", {}) or {})

    as_a = _extract_axis(axes, "AS", "Asc", "Ascendant")
    ds_a = _extract_axis(axes, "DS", "Desc", "Descendant")
    mc_a = _extract_axis(axes, "MC", "Midheaven", "Medium Coeli")
    fc_a = _extract_axis(axes, "FC", "IC", "Imum Coeli", "Nadir")

    if ds_a is None and as_a is not None:
        ds_a = (as_a + 180.0) % 360.0
    if fc_a is None and mc_a is not None:
        fc_a = (mc_a + 180.0) % 360.0

    if as_a is not None:
        axes["AS"] = as_a
    if ds_a is not None:
        axes["DS"] = ds_a
    if mc_a is not None:
        axes["MC"] = mc_a
    if fc_a is not None:
        axes["FC"] = fc_a

    def to_screen(deg: float) -> float:
        asc = float(axes.get("AS", 0.0))
        return (float(deg) - asc + 180.0) % 360.0

    size0 = min(width, height) - 2 * margin
    scale_theme = 0.80
    size = int(size0 * scale_theme)
    cx, cy = width // 2, height // 2

    r_outer = size * 0.36
    r_inner = size * 0.23
    aspect_gap = 0.0
    r_aspect = r_inner - aspect_gap

    px_sign = int(size * 0.048)
    px_planet_base = int(size * 0.055)
    px_axis = int(size * 0.050)

    outer_gap_min = int(size * 0.030)
    outer_gap_factor = 1.55
    outer_gap = max(outer_gap_min, int(px_planet_base * outer_gap_factor))
    r_planet = r_outer + outer_gap
    r_signs = 0.5 * (r_inner + r_outer)

    grid_step = 5
    grid_band = size * 0.020
    circ_out_w = 3
    circ_in_w = 2
    gap_out = circ_out_w / 2.0
    gap_in = circ_in_w / 2.0

    r_grid_out = r_outer - gap_out
    r_grid_in = r_grid_out - grid_band
    r_link_outer = (r_grid_in + r_grid_out) * 0.5

    r2_grid_in = r_inner + gap_in
    r2_grid_out = r2_grid_in + grid_band
    r_link_inner = (r2_grid_in + r2_grid_out) * 0.5

    # ------------------------------------------------------------------
    # Signes
    # ------------------------------------------------------------------
    signs = []
    for i, name in enumerate(SIGN_NAMES):
        ang = to_screen(i * 30 + 15)
        sx, sy = _pol_to_xy(cx, cy, r_signs, ang)
        coeff = PERCEPTION_COEFFS_SIGNS.get(name, 1.0)
        target_px = int(px_sign * coeff)
        signs.append({
            "index": i,
            "name": name,
            "angle": ang,
            "x": sx,
            "y": sy,
            "px": target_px,
        })

    # ------------------------------------------------------------------
    # Maisons
    # ------------------------------------------------------------------
    house_lines = []
    house_marks = []
    houses_payload = payload.get("houses", []) or []

    if show_houses and houses_payload:
        cusps: list[float] = []
        for hinfo in houses_payload:
            try:
                cusps.append(float(hinfo.get("lon_start")))
            except Exception:
                cusps.append(0.0)

        if len(cusps) == 12:
            if SHOW_HOUSE_SPOKES:
                for deg_cusp in cusps:
                    a = to_screen(deg_cusp)
                    x1, y1 = _pol_to_xy(cx, cy, r_inner, a)
                    x2, y2 = _pol_to_xy(cx, cy, r_outer, a)
                    house_lines.append({
                        "angle": a,
                        "x1": x1, "y1": y1,
                        "x2": x2, "y2": y2,
                    })

            for idx, deg_cusp in enumerate(cusps, start=1):
                if idx in HOUSES_SKIP_FOR_AXES:
                    continue
                a = to_screen(deg_cusp)
                xr1, yr1 = _pol_to_xy(cx, cy, r_grid_out, a)
                xr2, yr2 = _pol_to_xy(cx, cy, r_link_outer, a)
                label_offset = int(size * 0.018)
                tx, ty = _pol_to_xy(cx, cy, r_outer + label_offset, a)

                house_marks.append({
                    "house": idx,
                    "roman": ROMANS[idx - 1],
                    "angle": a,
                    "mark": {
                        "x1": xr1, "y1": yr1,
                        "x2": xr2, "y2": yr2,
                        "width": max(2, int(size * 0.0035)),
                    },
                    "label": {
                        "x": tx, "y": ty,
                    },
                })

    # ------------------------------------------------------------------
    # Planètes : préparation
    # ------------------------------------------------------------------
    planets_info: list[dict[str, Any]] = []
    for p in payload.get("planets", []):
        name = p.get("name", "?")
        lon = float(p.get("lon", 0.0))
        ang_real = to_screen(lon)
        deg_in_sign = lon % 30.0
        px_target = int(px_planet_base * PERCEPTION_COEFFS.get(name, 1.0))

        planets_info.append({
            "name": name,
            "lon": lon,
            "real": ang_real,
            "adj": ang_real,
            "px": px_target,
            "deg_in_sign": deg_in_sign,
            "is_retro": _planet_is_retrograde(p),
            "payload": p,
            "crowded": False,
        })

    planets_info.sort(key=lambda d: d["real"])

    # ------------------------------------------------------------------
    # Anti-chevauchement minimal
    # ------------------------------------------------------------------
    tol_factor = 2.0

    for i in range(1, len(planets_info)):
        left = planets_info[i - 1]
        right = planets_info[i]

        min_gap = _deg_from_px(0.85 * (left["px"] + right["px"]), r_planet)
        real_gap = _ang_short(left["real"], right["real"])

        if real_gap > tol_factor * min_gap:
            continue

        if (right["adj"] - left["adj"]) < min_gap:
            mid = 0.5 * (left["adj"] + right["adj"])
            left_new = mid - 0.5 * min_gap
            right_new = mid + 0.5 * min_gap

            max_shift = _deg_from_px(0.60 * max(left["px"], right["px"]), r_planet)
            left["adj"] = max(left["real"] - max_shift, min(left["real"] + max_shift, left_new))
            right["adj"] = max(right["real"] - max_shift, min(right["real"] + max_shift, right_new))

            j = i - 1
            while j > 0:
                lft = planets_info[j - 1]
                rgt = planets_info[j]
                gap_needed = _deg_from_px(0.85 * (lft["px"] + rgt["px"]), r_planet)

                if _ang_short(lft["real"], rgt["real"]) > tol_factor * gap_needed:
                    break

                gap = rgt["adj"] - lft["adj"]
                if gap >= gap_needed:
                    break

                mid2 = 0.5 * (lft["adj"] + rgt["adj"])
                l_new = mid2 - 0.5 * gap_needed
                r_new = mid2 + 0.5 * gap_needed

                max_l = _deg_from_px(0.60 * lft["px"], r_planet)
                max_r = _deg_from_px(0.60 * rgt["px"], r_planet)
                lft["adj"] = max(lft["real"] - max_l, min(lft["real"] + max_l, l_new))
                rgt["adj"] = max(rgt["real"] - max_r, min(rgt["real"] + max_r, r_new))
                j -= 1

    # ------------------------------------------------------------------
    # Groupes de planètes proches
    # ------------------------------------------------------------------
    groups: list[list[dict[str, Any]]] = []
    if planets_info:
        cur = [planets_info[0]]
        for k in range(1, len(planets_info)):
            left = planets_info[k - 1]
            right = planets_info[k]
            thr = _pair_dynamic_threshold(left, right, r_planet)
            if _ang_short(left["real"], right["real"]) < thr:
                cur.append(right)
            else:
                groups.append(cur)
                cur = [right]
        groups.append(cur)

        if len(groups) > 1:
            left_last = groups[-1][-1]
            right_first = groups[0][0]
            thr_lr = _pair_dynamic_threshold(left_last, right_first, r_planet)
            if _ang_short(left_last["real"], right_first["real"]) < thr_lr:
                groups[0] = groups[-1] + groups[0]
                groups.pop()

    def _min_current_gap_deg(grp: list[dict[str, Any]]) -> float:
        gmin = 1e9
        for i in range(len(grp) - 1):
            gmin = min(gmin, grp[i + 1]["adj"] - grp[i]["adj"])
        return gmin

    def _max_needed_gap_deg(grp: list[dict[str, Any]]) -> float:
        need = 0.0
        for i in range(len(grp) - 1):
            wi = grp[i]["px"]
            wj = grp[i + 1]["px"]
            need = max(need, _deg_from_px(0.85 * (wi + wj), r_planet))
        return need

    for grp in groups:
        if len(grp) == 1:
            continue

        min_current = _min_current_gap_deg(grp)
        max_needed = _max_needed_gap_deg(grp)

        if min_current >= max_needed:
            continue

        mid = _circ_mean([d["adj"] for d in grp])
        spacing = max_needed
        start = mid - spacing * (len(grp) - 1) / 2.0

        for j, d in enumerate(grp):
            d["adj"] = (start + j * spacing) % 360.0
            d["crowded"] = True

    # ------------------------------------------------------------------
    # Packing rangé exact
    # ------------------------------------------------------------------
    def _glyph_width_deg(px: float) -> float:
        return _deg_from_px(px, r_planet)

    for grp in groups:
        if len(grp) == 1:
            grp[0]["crowded"] = False
            continue

        real_list = [d["real"] for d in grp]
        px_list = [d["px"] for d in grp]

        gaps_min = [
            _deg_from_px(0.85 * (px_list[i] + px_list[i + 1]), r_planet)
            for i in range(len(grp) - 1)
        ]
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
            t = targets[j]
            real = d["real"]

            delta = ((t - real + 180.0) % 360.0) - 180.0

            cap_deg = DELTA_CAP_RATIO * _glyph_width_deg(d["px"])
            if delta > cap_deg:
                delta = cap_deg
            if delta < -cap_deg:
                delta = -cap_deg

            if len(grp) > 1:
                t_pos = j / (len(grp) - 1)
                edge_factor = 0.35 + 0.65 * math.sin(math.pi * t_pos)
            else:
                edge_factor = 1.0

            d["adj"] = (real + edge_factor * K_PUSH * delta + 360.0) % 360.0
            d["crowded"] = True

    # ------------------------------------------------------------------
    # Correction monotone intra-amas
    # ------------------------------------------------------------------
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
            grp[idx]["adj"] = (adj_sorted_vals[rank] + 360.0) % 360.0
            grp[idx]["crowded"] = True

    # ------------------------------------------------------------------
    # Garantie d'écart minimal intra-amas
    # ------------------------------------------------------------------
    for grp in groups:
        if len(grp) < 2:
            continue

        angles_adj = [d["adj"] for d in grp]
        mid = _circ_mean(angles_adj)
        lin = _unwrap_around(mid, angles_adj)
        order = sorted(range(len(grp)), key=lambda idx: lin[idx])

        lin_all = lin[:]
        for _ in range(2):
            for k in range(1, len(order)):
                i_prev = order[k - 1]
                i_cur = order[k]

                a_prev = lin_all[i_prev]
                a_cur = lin_all[i_cur]

                min_gap = _deg_from_px(0.65 * (grp[i_prev]["px"] + grp[i_cur]["px"]), r_planet)
                gap = a_cur - a_prev
                if gap < min_gap:
                    shift = (min_gap - gap)
                    lin_all[i_prev] -= 0.5 * shift
                    lin_all[i_cur] += 0.5 * shift

            for k in range(len(order) - 2, -1, -1):
                i_cur = order[k]
                i_next = order[k + 1]

                a_cur = lin_all[i_cur]
                a_next = lin_all[i_next]

                min_gap = _deg_from_px(0.65 * (grp[i_cur]["px"] + grp[i_next]["px"]), r_planet)
                gap = a_next - a_cur
                if gap < min_gap:
                    shift = (min_gap - gap)
                    lin_all[i_cur] -= 0.5 * shift
                    lin_all[i_next] += 0.5 * shift

        for i, d in enumerate(grp):
            d["adj"] = (lin_all[i] + 360.0) % 360.0

    # ------------------------------------------------------------------
    # Filet global
    # ------------------------------------------------------------------
    if len(planets_info) > 1:
        angles_all = [d["adj"] for d in planets_info]
        mid_all = _circ_mean(angles_all)
        lin_all = _unwrap_around(mid_all, angles_all)
        order_all = sorted(range(len(planets_info)), key=lambda idx: lin_all[idx])

        lin_all = lin_all[:]
        for _ in range(2):
            for k in range(1, len(order_all)):
                i_prev = order_all[k - 1]
                i_cur = order_all[k]

                a_prev = lin_all[i_prev]
                a_cur = lin_all[i_cur]

                min_gap = _deg_from_px(
                    0.60 * (planets_info[i_prev]["px"] + planets_info[i_cur]["px"]),
                    r_planet,
                )
                gap = a_cur - a_prev
                if gap < min_gap:
                    shift = min_gap - gap
                    lin_all[i_cur] += shift

        for i, d in enumerate(planets_info):
            d["adj"] = (lin_all[i] + 360.0) % 360.0

    # ------------------------------------------------------------------
    # Garantie monotone globale
    # ------------------------------------------------------------------
    if len(planets_info) >= 2:
        real_list = [d["real"] for d in planets_info]
        adj_list = [d["adj"] for d in planets_info]

        mid = _circ_mean(real_list)
        lin_real = _unwrap_around(mid, real_list)
        lin_adj = _unwrap_around(mid, adj_list)

        order_real = sorted(range(len(planets_info)), key=lambda i: lin_real[i])

        inversion = False
        for k in range(1, len(order_real)):
            i_prev = order_real[k - 1]
            i_cur = order_real[k]
            if lin_adj[i_cur] < lin_adj[i_prev]:
                inversion = True
                break

        if inversion:
            adj_sorted = sorted(lin_adj)
            for rank, idx in enumerate(order_real):
                planets_info[idx]["adj"] = (adj_sorted[rank] + 360.0) % 360.0

    # ------------------------------------------------------------------
    # Encoches des axes
    # ------------------------------------------------------------------
    def _axis_screen_angle(label: str) -> float | None:
        v = axes.get(label)
        return to_screen(float(v)) if v is not None else None

    def _encoches_par_axes(planets: list[dict[str, Any]]) -> dict[str, list[float]]:
        enc = {"AS": [], "DS": [], "MC": [], "FC": []}
        for d in planets:
            half_px = 0.5 * d["px"]
            a_planet = d["adj"]
            w_deg = ((half_px + 2) / max(1.0, r_planet)) * (180.0 / math.pi)

            for label in ("AS", "DS", "MC", "FC"):
                a_axis = _axis_screen_angle(label)
                if a_axis is None:
                    continue
                dist = abs((a_planet - a_axis + 180.0) % 360.0 - 180.0)
                if dist < w_deg:
                    r_gap = r_planet - (half_px - 1)
                    enc[label].append(r_gap)
        return enc

    enc_by_axis = _encoches_par_axes(planets_info)

    # ------------------------------------------------------------------
    # Axes : géométrie seulement
    # ------------------------------------------------------------------
    def build_axis(label: str, sky_deg: float | None, gaps_px: list[float] | None = None) -> dict[str, Any] | None:
        if sky_deg is None:
            return None

        a = to_screen(sky_deg)

        axis_gap = int(size * 0.09)
        r_axes = r_outer + axis_gap
        base_axis_width = max(3, int(size * 0.004))
        arm = int(size * 0.08)
        tick = int(size * 0.026)
        cap_mc = int(size * 0.032)
        cap_fc = int(size * 0.036)

        axis_len_as_ds = 0.22
        axis_len_mc_fc = 0.20
        axis_gap = int(size * (axis_len_as_ds if label in ("AS", "DS") else axis_len_mc_fc))
        r_axes = r_outer + axis_gap
        axis_width = base_axis_width + 1

        r_axis_end = r_axes
        if label == "MC":
            r_axis_end = r_axes - cap_mc - axis_width / 2
        elif label == "FC":
            r_axis_end = r_axes - cap_fc - axis_width / 2

        gap_len_px = 2
        half_len = gap_len_px * 0.5
        gaps = sorted(set(round(g, 2) for g in (gaps_px or [])))

        segments = []
        cursor_r0 = r_outer
        for r_gap in gaps:
            r1 = r_gap - half_len
            r2 = r_gap + half_len
            if r1 > cursor_r0:
                x0, y0 = _pol_to_xy(cx, cy, cursor_r0, a)
                x1, y1 = _pol_to_xy(cx, cy, min(r1, r_axis_end), a)
                segments.append({
                    "x1": x0, "y1": y0,
                    "x2": x1, "y2": y1,
                })
            cursor_r0 = max(cursor_r0, r2)

        if cursor_r0 < r_axis_end:
            x0, y0 = _pol_to_xy(cx, cy, cursor_r0, a)
            x1, y1 = _pol_to_xy(cx, cy, r_axis_end, a)
            segments.append({
                "x1": x0, "y1": y0,
                "x2": x1, "y2": y1,
            })

        axis_end_x, axis_end_y = _pol_to_xy(cx, cy, r_axis_end, a)

        decoration: dict[str, Any] = {"type": None}
        if label == "AS":
            arrow_len = int(size * 0.060)
            arrow_open = 26
            a_rev = a + 180
            xL, yL = _pol_to_xy(axis_end_x, axis_end_y, arrow_len, a_rev + arrow_open)
            xR, yR = _pol_to_xy(axis_end_x, axis_end_y, arrow_len, a_rev - arrow_open)
            decoration = {
                "type": "arrow",
                "tip": {"x": axis_end_x, "y": axis_end_y},
                "left": {"x": xL, "y": yL},
                "right": {"x": xR, "y": yR},
            }
        elif label == "DS":
            ux = math.cos(math.radians(a + 90))
            uy = math.sin(math.radians(a + 90))
            xL = axis_end_x - tick * ux
            yL = axis_end_y + tick * uy
            xR = axis_end_x + tick * ux
            yR = axis_end_y - tick * uy
            decoration = {
                "type": "crossbar",
                "left": {"x": xL, "y": yL},
                "right": {"x": xR, "y": yR},
            }
        elif label == "MC":
            xc, yc = _pol_to_xy(cx, cy, r_axes, a)
            decoration = {
                "type": "circle",
                "cx": xc,
                "cy": yc,
                "r": cap_mc,
            }
        elif label == "FC":
            xc, yc = _pol_to_xy(cx, cy, r_axes, a)
            decoration = {
                "type": "half_circle",
                "cx": xc,
                "cy": yc,
                "r": cap_fc,
                "start": float(a + 90),
                "extent": 180,
            }

        if label in ("MC", "FC"):
            gx, gy = _pol_to_xy(cx, cy, r_axes, a)
        elif label in ("AS", "DS"):
            half_glyph = int(px_axis * 0.5)
            mg = int(size * 0.008)
            offset = half_glyph + mg
            gx, gy = _pol_to_xy(cx, cy, r_axis_end + offset, a)
        else:
            gx, gy = _pol_to_xy(cx, cy, r_axes, a)

        return {
            "label": label,
            "sky_deg": sky_deg,
            "angle": a,
            "width": axis_width,
            "segments": segments,
            "decoration": decoration,
            "glyph": {
                "x": gx,
                "y": gy,
                "px": px_axis,
                "language_label": "IC" if (label == "FC" and language == "en") else label,
            },
        }

    axes_layout = {
        "AS": build_axis("AS", as_a, enc_by_axis.get("AS")),
        "DS": build_axis("DS", ds_a, enc_by_axis.get("DS")),
        "MC": build_axis("MC", mc_a, enc_by_axis.get("MC")),
        "FC": build_axis("FC", fc_a, enc_by_axis.get("FC")),
    }

    # ------------------------------------------------------------------
    # Conjonctions
    # ------------------------------------------------------------------
    conj_links = []
    if show_aspects:
        angles_for_markers = {d["name"]: d["real"] for d in planets_info}
        tick_out_len = (r_grid_out - r_link_outer)
        r_tip = r_outer + tick_out_len - 1
        sep = 3
        r1 = r_tip - sep
        r2 = r_tip
        eps = 0.15

        for aspect in payload.get("aspects", []) or []:
            if aspect.get("type") != "CONJ":
                continue
            ang1 = angles_for_markers.get(aspect.get("p1"))
            ang2 = angles_for_markers.get(aspect.get("p2"))
            if ang1 is None or ang2 is None:
                continue

            a, b = sorted([ang1, ang2])
            if b - a > 180:
                a, b = b, a + 360

            start = a - eps
            extent = (b - a) + 2 * eps

            conj_links.append({
                "p1": aspect.get("p1"),
                "p2": aspect.get("p2"),
                "start": start,
                "extent": extent,
                "radii": [r1, r2],
                "color": "#0077CC",
                "width": 2,
            })

    # ------------------------------------------------------------------
    # Planètes : géométrie finale
    # ------------------------------------------------------------------
    line_w = 2
    link_col = "#4A4A4A"
    elbow_out = int(size * 0.022)

    planets_info_sorted = sorted(planets_info, key=lambda d: d["real"])
    planets_layout = []

    for d in planets_info_sorted:
        name = d["name"]
        ang_band = d["real"]
        ang_glyph = d["adj"]

        pxg, pyg = _pol_to_xy(cx, cy, r_planet, ang_glyph)
        half_px = 0.5 * d["px"]
        margin_oblique = 1.0

        degree_label = None
        pos_sign = d.get("deg_in_sign")
        if pos_sign is not None:
            try:
                n = int(round(float(pos_sign))) % 30
                r_text = r_planet + int(size * 0.040)
                tx, ty = _pol_to_xy(cx, cy, r_text, ang_glyph)
                degree_label = {
                    "value": n,
                    "x": tx,
                    "y": ty,
                    "retro": bool(d.get("is_retro")),
                    "retro_x": tx + int(size * 0.018),
                    "retro_y": ty,
                }
            except Exception:
                degree_label = None

        connectors = []
        if d["crowded"]:
            elbow_r = r_outer + elbow_out
            for start_r in (r_grid_out, r_link_outer):
                xb0, yb0 = _pol_to_xy(cx, cy, start_r, ang_band)
                xb1, yb1 = _pol_to_xy(cx, cy, elbow_r, ang_band)
                connectors.append({
                    "type": "radial",
                    "x1": xb0, "y1": yb0,
                    "x2": xb1, "y2": yb1,
                    "width": line_w,
                    "color": link_col,
                })

            xb1, yb1 = _pol_to_xy(cx, cy, elbow_r, ang_band)
            dx, dy = (pxg - xb1), (pyg - yb1)
            dist = math.hypot(dx, dy)
            stop_from_elbow = max(dist - (half_px + margin_oblique), 0.0)
            if dist > 0 and stop_from_elbow > 0:
                t = stop_from_elbow / dist
                xo, yo = (xb1 + dx * t, yb1 + dy * t)
                connectors.append({
                    "type": "oblique",
                    "x1": xb1, "y1": yb1,
                    "x2": xo, "y2": yo,
                    "width": line_w,
                    "color": link_col,
                })
        else:
            xb0, yb0 = _pol_to_xy(cx, cy, r_link_outer, ang_band)
            xb1, yb1 = _pol_to_xy(cx, cy, r_outer + elbow_out, ang_band)
            connectors.append({
                "type": "radial",
                "x1": xb0, "y1": yb0,
                "x2": xb1, "y2": yb1,
                "width": line_w,
                "color": link_col,
            })

            dx, dy = (pxg - xb1), (pyg - yb1)
            dist = math.hypot(dx, dy)
            stop_from_elbow = max(dist - (half_px + margin_oblique), 0.0)
            if dist > 0 and stop_from_elbow > 0:
                t = stop_from_elbow / dist
                xo, yo = (xb1 + dx * t, yb1 + dy * t)
                connectors.append({
                    "type": "oblique",
                    "x1": xb1, "y1": yb1,
                    "x2": xo, "y2": yo,
                    "width": line_w,
                    "color": link_col,
                })

        planets_layout.append({
            "name": name,
            "lon": d["lon"],
            "real_angle": ang_band,
            "glyph_angle": ang_glyph,
            "x": pxg,
            "y": pyg,
            "px": d["px"],
            "crowded": bool(d["crowded"]),
            "is_retro": bool(d["is_retro"]),
            "deg_in_sign": d["deg_in_sign"],
            "degree_label": degree_label,
            "connectors": connectors,
        })

    # ------------------------------------------------------------------
    # Retour complet
    # ------------------------------------------------------------------
    return {
        "ok": True,
        "meta": {
            "language": language,
            "title": _build_title(language, title_suffix, show_title),
            "width": width,
            "height": height,
            "center": {"x": cx, "y": cy},
            "size": size,
        },
        "radii": {
            "outer": r_outer,
            "inner": r_inner,
            "aspect": r_aspect,
            "planet": r_planet,
            "signs": r_signs,
            "grid_out": r_grid_out,
            "grid_in": r_grid_in,
            "link_outer": r_link_outer,
            "grid2_in": r2_grid_in,
            "grid2_out": r2_grid_out,
            "link_inner": r_link_inner,
        },
        "zodiac_boundaries": [
            {
                "index": i,
                "angle": to_screen(i * 30.0),
                "inner": _pol_to_xy(cx, cy, r_inner, to_screen(i * 30.0)),
                "outer": _pol_to_xy(cx, cy, r_outer, to_screen(i * 30.0)),
            }
            for i in range(12)
        ],
        "signs": signs,
        "house_lines": house_lines,
        "house_marks": house_marks,
        "axes": axes_layout,
        "conjunction_links": conj_links,
        "planets": planets_layout,
        "raw_axes": {
            "AS": as_a,
            "DS": ds_a,
            "MC": mc_a,
            "FC": fc_a,
        },
    }

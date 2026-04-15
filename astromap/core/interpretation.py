from __future__ import annotations

import html
from typing import Any, Dict, List, Tuple

from .interpret_texts import INTRO_TEXTS, PLANET_TEXTS, RET_FAMILY_TEXTS, SIGN_TEXTS
from .ret_hp import compute_planet_hierarchy, compute_ret_box_colors
from .ret_families import compute_ret_ranking
from .signs_hierarchy import rank_signs


PLANET_TO_TEXT_KEY = {
    "Soleil": "rR",
    "Vénus": "eR",
    "Venus": "eR",
    "Mercure": "tR",
    "Mars": "eE",
    "Jupiter": "rE",
    "Saturne": "tE",
    "Uranus": "rT",
    "Neptune": "eT",
    "Pluton": "tT",
    "Lune": "p",
}

SIGN_FR_TO_KEY = {
    "Bélier": "Aries",
    "Belier": "Aries",
    "Taureau": "Taurus",
    "Gémeaux": "Gemini",
    "Gemeaux": "Gemini",
    "Cancer": "Cancer",
    "Lion": "Leo",
    "Vierge": "Virgo",
    "Balance": "Libra",
    "Scorpion": "Scorpio",
    "Sagittaire": "Sagittarius",
    "Capricorne": "Capricorn",
    "Verseau": "Aquarius",
    "Poissons": "Pisces",
}


def sign_name_from_longitude(lon: float) -> str:
    signs = [
        "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
        "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons",
    ]
    lon = float(lon) % 360.0
    return signs[int(lon // 30.0)]


def _lang(settings_language: str | None) -> str:
    return "EN" if str(settings_language or "").upper().startswith("EN") else "FR"


def _planet_sign_map(payload: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in payload.get("planets", []) or []:
        name = p.get("name")
        sign = p.get("sign")
        if not sign and isinstance(p.get("lon"), (int, float)):
            sign = sign_name_from_longitude(float(p["lon"]))
        if name and sign:
            out[str(name)] = str(sign)
    return out


def _asc_sign_from_payload(payload: dict[str, Any]) -> str:
    axes = payload.get("axes", {}) or {}
    asc = axes.get("AS")
    if isinstance(asc, (int, float)):
        return sign_name_from_longitude(float(asc))

    if isinstance(payload.get("houses"), list) and payload["houses"]:
        h1 = payload["houses"][0]
        if isinstance(h1, dict):
            sign = h1.get("sign")
            if sign:
                return str(sign)
            if isinstance(h1.get("lon"), (int, float)):
                return sign_name_from_longitude(float(h1["lon"]))

    return ""


def _compute_ret_state(payload: dict[str, Any]) -> dict[str, Any]:
    ranks, ordered_planets, _info = compute_planet_hierarchy(payload, payload)
    ret_order, _ret_details = compute_ret_ranking(ranks)
    sign_ranking = rank_signs(payload.get("planets", []) or [], ranks)
    angular_set = set()
    box_colors = compute_ret_box_colors(ordered_planets, angular_set, payload.get("aspects", []) or [])
    planet_signs = _planet_sign_map(payload)

    return {
        "ordered_planets": ordered_planets,
        "ret_colors": box_colors,
        "sign_ranking": sign_ranking,
        "planet_signs": planet_signs,
        "ret_families_order": ret_order,
    }


def _compute_interpretation_state(payload: dict[str, Any]) -> dict[str, Any]:
    st = _compute_ret_state(payload)

    ordered_planets: list[str] = st["ordered_planets"]
    ret_colors: dict[str, str] = st["ret_colors"]
    sign_ranking: list[tuple[str, float]] = st["sign_ranking"]
    planet_signs: dict[str, str] = st["planet_signs"]
    ret_order: list[str] = st["ret_families_order"]

    dominant_planets = [p for p in ordered_planets if (ret_colors.get(p) or "").lower() == "black"][:5]

    filtered = [(sign, score) for (sign, score) in sign_ranking if score > 15]
    dominant_signs: list[str] = []
    if filtered:
        dominant_planets_by_sign: Dict[str, List[str]] = {}
        speed_order = [
            "Lune", "Soleil", "Mercure", "Vénus", "Mars",
            "Jupiter", "Saturne", "Uranus", "Neptune", "Pluton",
        ]
        speed_index = {name: idx for idx, name in enumerate(speed_order)}

        for planet in ordered_planets:
            if (ret_colors.get(planet) or "").lower() == "black":
                sign_name = planet_signs.get(planet)
                if sign_name:
                    dominant_planets_by_sign.setdefault(sign_name, []).append(planet)

        original_index = {sign: idx for idx, (sign, _score) in enumerate(sign_ranking)}

        def sort_key(item: Tuple[str, float]) -> Tuple[float, int, int, int]:
            sign, score = item
            has_dom = bool(dominant_planets_by_sign.get(sign))
            if has_dom:
                fastest_planet = min(
                    dominant_planets_by_sign[sign],
                    key=lambda p: speed_index.get(p, 999),
                )
                fastest_idx = speed_index.get(fastest_planet, 999)
            else:
                fastest_idx = 999

            return (
                -score,
                -int(has_dom),
                fastest_idx,
                original_index.get(sign, 999),
            )

        filtered_sorted = sorted(filtered, key=sort_key)
        dominant_signs = [s for (s, _score) in filtered_sorted][:2]

    greys = {"grey", "gray", "lightgray", "lightgrey"}
    sub_dominant_planets = [p for p in ordered_planets if (ret_colors.get(p) or "").lower() in greys]
    non_dominant_planets = [p for p in ordered_planets if (ret_colors.get(p) or "").lower() == "white"]

    sun_sign = planet_signs.get("Soleil", "")
    asc_sign = _asc_sign_from_payload(payload)
    dominant_ret_families = ret_order[:4]

    return {
        "ordered_planets": ordered_planets,
        "ret_colors": ret_colors,
        "planet_signs": planet_signs,
        "sign_ranking": sign_ranking,
        "ret_families_order": ret_order,
        "dominant_planets": dominant_planets,
        "dominant_signs": dominant_signs,
        "dominant_ret_families": dominant_ret_families,
        "sun_sign": sun_sign,
        "asc_sign": asc_sign,
        "sub_dominant_planets": sub_dominant_planets,
        "non_dominant_planets": non_dominant_planets,
    }


def build_dynamic_intro(state: dict[str, Any], lang: str) -> str:
    sun = (state.get("sun_sign") or "").strip()
    asc = (state.get("asc_sign") or "").strip()

    dom = ", ".join(state.get("dominant_planets", []) or [])
    sub = ", ".join(state.get("sub_dominant_planets", []) or [])
    non = ", ".join(state.get("non_dominant_planets", []) or [])

    if lang == "EN":
        sun = SIGN_FR_TO_KEY.get(sun, sun)
        asc = SIGN_FR_TO_KEY.get(asc, asc)
        return (
            f"{sun} with {asc} rising, your dominant planets—those that most often "
            f"structure your functioning—are: {dom}. "
            f"The sub-dominant planets—activated in a more occasional manner—are: {sub}. "
            f"Finally, {non} occupy the lowest positions in the chart’s hierarchy and correspond to functions "
            f"that are weakly mobilised in everyday experience.\n\n"
            "The interpretations presented here describe psychological and behavioral "
            "tendencies derived from the natal chart. For a fully personalized reading, "
            "it would be necessary to take into account extra-astrological factors such as "
            "education, sociocultural environment, personal history, heredity, and so on."
        )

    return (
        f"{sun} ascendant {asc}, tes planètes dominantes — celles qui structurent "
        f"le plus souvent ton fonctionnement — sont : {dom}. "
        f"Les planètes sous-dominantes — mobilisées de manière plus ponctuelle — "
        f"sont : {sub}. "
        f"Enfin, {non} sont les planètes les plus faibles du thème et correspondent à des fonctions "
        f"peu ou pas mobilisées dans l’expérience habituelle.\n\n"
        "Les interprétations proposées ici décrivent des tendances psychologiques et "
        "comportementales issues du thème de naissance. Pour une lecture pleinement "
        "personnalisée, il serait nécessaire de prendre en compte l’ensemble des "
        "facteurs extra-astrologiques — éducation, environnement socioculturel, "
        "histoire personnelle, hérédité, etc."
    )


def _add_planet_block(runs: list[dict[str, str]], txt: str) -> None:
    if not txt:
        return
    lines = txt.strip("\n").splitlines()
    if not lines:
        return

    title = lines[0].strip()
    rest = lines[1:]

    if title:
        runs.append({"style": "bold", "text": title})

    paragraph_buffer: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            body = "\n".join(paragraph_buffer).strip()
            if body:
                runs.append({"style": "p", "text": body})
        paragraph_buffer = []

    for raw_line in rest:
        s = raw_line.rstrip()
        stripped = s.strip()

        if not stripped:
            flush_paragraph()
            continue

        if stripped.endswith(":"):
            flush_paragraph()
            runs.append({"style": "bold_soft", "text": stripped})
        else:
            paragraph_buffer.append(s)

    flush_paragraph()


def _add_ret_family_block(runs: list[dict[str, str]], txt: str) -> None:
    if not txt:
        return
    lines = txt.strip("\n").splitlines()
    if not lines:
        return

    title = lines[0].strip()
    subtitle = lines[1].strip() if len(lines) > 1 and lines[1].strip().startswith("(") else None
    body_lines = lines[2:] if subtitle else lines[1:]
    body = "\n".join(l.rstrip() for l in body_lines).strip()

    if title:
        runs.append({"style": "bold_nogap", "text": title})
    if subtitle:
        runs.append({"style": "bold_soft", "text": subtitle})
    if body:
        runs.append({"style": "p", "text": body})


def _add_sign_block(runs: list[dict[str, str]], txt: str) -> None:
    if not txt:
        return

    lines = txt.strip("\n").splitlines()
    if not lines:
        return

    paragraph_buffer: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            body = "\n".join(paragraph_buffer).strip()
            if body:
                runs.append({"style": "p", "text": body})
        paragraph_buffer = []

    for line in lines:
        s = line.rstrip()
        stripped = s.strip()

        if not stripped:
            flush_paragraph()
            continue

        low = stripped.lower()
        is_main_heading_fr = ("expression adaptée" in low) or ("expression inadaptée" in low)
        is_main_heading_en = ("adapted expression" in low) or ("maladapted expression" in low)

        is_internal_subtitle = (
            not is_main_heading_fr
            and not is_main_heading_en
            and not stripped.endswith(".")
            and not stripped.endswith("!")
            and not stripped.endswith("?")
            and len(stripped) <= 60
        )

        if is_main_heading_fr or is_main_heading_en:
            flush_paragraph()
            runs.append({"style": "bold", "text": stripped})
        elif is_internal_subtitle:
            flush_paragraph()
            subtitle = stripped if stripped.endswith(":") else stripped + " :"
            runs.append({"style": "bold_soft", "text": subtitle})
        else:
            paragraph_buffer.append(s)

    flush_paragraph()


def build_interpretation_payload(theme_payload: dict[str, Any], language: str = "fr") -> dict[str, Any]:
    lang = _lang(language)
    state = _compute_interpretation_state(theme_payload)

    runs: list[dict[str, str]] = []
    page_title = "Lecture du thème astrologique" if lang == "FR" else "Astrological Chart Reading"

    runs.append({"style": "page_title", "text": page_title})
    runs.append({"style": "p", "text": build_dynamic_intro(state, lang)})

    runs.append({"style": "section", "text": "Planètes dominantes" if lang == "FR" else "Dominant Planets"})
    runs.append({"style": "p", "text": INTRO_TEXTS.get(lang, {}).get("planets", "")})
    if state["dominant_planets"]:
        for planet in state["dominant_planets"]:
            key = PLANET_TO_TEXT_KEY.get(planet)
            txt = PLANET_TEXTS.get(lang, {}).get(key, "") if key else ""
            if txt:
                _add_planet_block(runs, txt)
    else:
        runs.append({"style": "p", "text": "Aucune planète dominante." if lang == "FR" else "No dominant planet."})

    runs.append({"style": "section", "text": "Familles RET dominantes" if lang == "FR" else "Dominant RET Families"})
    runs.append({"style": "p", "text": INTRO_TEXTS.get(lang, {}).get("ret", "")})
    if state["dominant_ret_families"]:
        for fam in state["dominant_ret_families"]:
            txt = RET_FAMILY_TEXTS.get(lang, {}).get(fam, "")
            if txt:
                _add_ret_family_block(runs, txt)
    else:
        runs.append({"style": "p", "text": "Aucune famille RET dominante." if lang == "FR" else "No dominant RET family."})

    runs.append({"style": "section", "text": "Signes dominants" if lang == "FR" else "Dominant Zodiac Signs"})
    runs.append({"style": "p", "text": INTRO_TEXTS.get(lang, {}).get("signs", "")})
    if state["dominant_signs"]:
        for sign in state["dominant_signs"]:
            key = SIGN_FR_TO_KEY.get(sign, sign)
            txt = SIGN_TEXTS.get(lang, {}).get(key, "")
            if txt:
                _add_sign_block(runs, txt)
    else:
        runs.append({"style": "p", "text": "Aucun signe dominant." if lang == "FR" else "No dominant sign."})

    return {
        "title": page_title,
        "language": lang.lower(),
        "intro": build_dynamic_intro(state, lang),
        "dominants": {
            "planets": state["dominant_planets"],
            "ret_families": state["dominant_ret_families"],
            "signs": state["dominant_signs"],
            "sub_dominant_planets": state["sub_dominant_planets"],
            "non_dominant_planets": state["non_dominant_planets"],
            "sun_sign": state["sun_sign"],
            "asc_sign": state["asc_sign"],
        },
        "runs": runs,
    }


def render_interpretation_html(data: dict[str, Any]) -> str:
    title = html.escape(str(data.get("title", "")))
    runs = data.get("runs", []) or []

    parts = [
        "<!doctype html>",
        '<html lang="fr"><head><meta charset="utf-8">',
        f"<title>{title}</title>",
        """<style>
        body{margin:0;background:#fff;font-family:"Segoe UI",Arial,sans-serif;color:#000;}
        .wrap{max-width:980px;margin:0 auto;padding:18px 140px 28px 140px;}
        .page-title{font-size:18px;font-weight:700;color:#1f4fa3;text-align:center;margin:0 0 18px 0;}
        .section{font-size:14px;font-weight:700;color:#1f3a5f;margin:18px 0 10px 0;}
        .bold{font-size:11px;font-weight:700;color:#2b4c7e;margin:0 0 10px 0;}
        .bold-soft{font-size:10px;font-weight:700;color:#333;margin:0 0 10px 0;}
        .bold-nogap{font-size:11px;font-weight:700;color:#2b4c7e;margin:0;}
        .p{font-size:10px;line-height:1.45;margin:0 0 16px 0;text-align:justify;white-space:pre-line;}
        </style></head><body><div class="wrap">"""
    ]

    for run in runs:
        style = run.get("style", "p")
        text = html.escape(str(run.get("text", "")))

        if style == "page_title":
            parts.append(f'<div class="page-title">{text}</div>')
        elif style == "section":
            parts.append(f'<div class="section">{text}</div>')
        elif style == "bold":
            parts.append(f'<div class="bold">{text}</div>')
        elif style == "bold_soft":
            parts.append(f'<div class="bold-soft">{text}</div>')
        elif style == "bold_nogap":
            parts.append(f'<div class="bold-nogap">{text}</div>')
        else:
            parts.append(f'<div class="p">{text}</div>')

    parts.append("</div></body></html>")
    return "".join(parts)

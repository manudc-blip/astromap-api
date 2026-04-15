from __future__ import annotations

from typing import Any

from .interpret_texts import INTRO_TEXTS, PLANET_TEXTS, RET_FAMILY_TEXTS, SIGN_TEXTS
from .ret_hp import compute_planet_hierarchy
from .ret_families import compute_ret_ranking
from .signs_hierarchy import rank_signs
from .houses import sign_name_from_longitude


PLANET_TO_TEXT_KEY = {
    "Soleil": "sun",
    "Lune": "moon",
    "Mercure": "mercury",
    "Vénus": "venus",
    "Venus": "venus",
    "Mars": "mars",
    "Jupiter": "jupiter",
    "Saturne": "saturn",
    "Uranus": "uranus",
    "Neptune": "neptune",
    "Pluton": "pluto",
}

SIGN_FR_TO_KEY = {
    "Bélier": "aries",
    "Belier": "aries",
    "Taureau": "taurus",
    "Gémeaux": "gemini",
    "Gemeaux": "gemini",
    "Cancer": "cancer",
    "Lion": "leo",
    "Vierge": "virgo",
    "Balance": "libra",
    "Scorpion": "scorpio",
    "Sagittaire": "sagittarius",
    "Capricorne": "capricorn",
    "Verseau": "aquarius",
    "Poissons": "pisces",
}

RET_LABELS = {
    "fr": {
        "p": "pouvoir intensif",
        "E": "Existence extensive",
        "t": "transcendance intensive",
        "e": "existence intensive",
        "R": "Représentation extensive",
        "r": "représentation intensive",
        "P": "Pouvoir extensif",
        "T": "Transcendance extensive",
    },
    "en": {
        "p": "intensive power",
        "E": "extensive existence",
        "t": "intensive transcendence",
        "e": "intensive existence",
        "R": "extensive representation",
        "r": "intensive representation",
        "P": "extensive power",
        "T": "extensive transcendence",
    },
}


def _lang(language: str | None) -> str:
    return "en" if str(language or "").lower().startswith("en") else "fr"


def _norm_planet(name: str | None) -> str:
    return (name or "").strip()


def _norm_sign(name: str | None) -> str:
    return (name or "").strip()


def _txt(src: Any, language: str, *keys: str, default: str = "") -> str:
    cur = src
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    if isinstance(cur, dict):
        return str(cur.get(language, default) or default)
    return str(cur or default)


def _planet_text(language: str, planet_name: str) -> dict[str, str]:
    key = PLANET_TO_TEXT_KEY.get(_norm_planet(planet_name))
    if not key:
        return {"title": planet_name, "body": ""}

    data = PLANET_TEXTS.get(key, {})
    title = _txt(data, language, "title", default=planet_name)
    body = _txt(data, language, "text", default="")
    if not body:
        body = _txt(data, language, "body", default="")
    return {"title": title, "body": body}


def _ret_text(language: str, family_code: str) -> dict[str, str]:
    data = RET_FAMILY_TEXTS.get(family_code, {})
    title = _txt(data, language, "title", default=family_code)
    body = _txt(data, language, "text", default="")
    if not body:
        body = _txt(data, language, "body", default="")
    return {"title": title, "body": body}


def _sign_text(language: str, sign_name: str) -> dict[str, str]:
    key = SIGN_FR_TO_KEY.get(_norm_sign(sign_name))
    if not key:
        return {"title": sign_name, "body": ""}

    data = SIGN_TEXTS.get(key, {})
    title = _txt(data, language, "title", default=sign_name)
    body = _txt(data, language, "text", default="")
    if not body:
        body = _txt(data, language, "body", default="")
    return {"title": title, "body": body}


def _get_sun_sign(payload: dict[str, Any]) -> str:
    for p in payload.get("planets", []) or []:
        if p.get("name") == "Soleil":
            return p.get("sign") or ""
    return ""


def _get_asc_sign(payload: dict[str, Any]) -> str:
    axes = payload.get("axes", {}) or {}

    asc = axes.get("AS")
    if isinstance(asc, dict):
        return asc.get("sign") or ""

    if isinstance(asc, (int, float)):
        return sign_name_from_longitude(float(asc))

    return ""


def _compute_dominants(payload: dict[str, Any]) -> tuple[list[str], list[str], list[tuple[str, float]], list[str]]:
    ranks, ordered_planets, _info = compute_planet_hierarchy(payload, payload)
    ret_order, _ret_details = compute_ret_ranking(ranks)
    sign_ranked = rank_signs(payload.get("planets", []) or [], ranks)

    dom_planets = ordered_planets[:4]
    sign_names = [name for name, _score in sign_ranked[:3]]
    return ordered_planets, dom_planets, sign_ranked, ret_order


def _build_dynamic_intro(payload: dict[str, Any], language: str, ordered_planets: list[str], dom_planets: list[str]) -> str:
    sun_sign = _get_sun_sign(payload) or ("Aries" if language == "en" else "Bélier")
    asc_sign = _get_asc_sign(payload) or ("Leo" if language == "en" else "Lion")

    subdom = ordered_planets[4:8]
    weak = ordered_planets[8:]

    def join_names(names: list[str]) -> str:
        return ", ".join(names)

    if language == "en":
        lead = (
            f"{sun_sign} with {asc_sign} rising, your dominant planets — those that most often structure "
            f"your way of functioning — are {join_names(dom_planets)}. "
        )
        if subdom:
            lead += (
                f"The sub-dominant planets — mobilized in a more punctual way — are {join_names(subdom)}. "
            )
        if weak:
            lead += (
                f"Finally, {join_names(weak)} are the least emphasized planets in the chart and correspond "
                f"to functions that are little used, or not always easy to mobilize in experience."
            )
        disclaimer = _txt(INTRO_TEXTS, language, "disclaimer", default="")
        return (lead + ("\n\n" + disclaimer if disclaimer else "")).strip()

    lead = (
        f"{sun_sign} ascendant {asc_sign}, tes planètes dominantes — celles qui structurent le plus souvent "
        f"ton fonctionnement — sont : {join_names(dom_planets)}. "
    )
    if subdom:
        lead += (
            f"Les planètes sous-dominantes — mobilisées de manière plus ponctuelle — sont : {join_names(subdom)}. "
        )
    if weak:
        lead += (
            f"Enfin, {join_names(weak)} sont les planètes les plus faibles du thème et correspondent à des "
            f"fonctions peu ou pas mobilisées dans l'expérience habituelle."
        )
    disclaimer = _txt(INTRO_TEXTS, language, "disclaimer", default="")
    return (lead + ("\n\n" + disclaimer if disclaimer else "")).strip()


def build_interpretation_payload(payload: dict[str, Any], language: str = "fr") -> dict[str, Any]:
    language = _lang(language)

    ordered_planets, dom_planets, sign_ranked, ret_order = _compute_dominants(payload)
    dom_signs = [name for name, _score in sign_ranked[:3]]
    dom_families = ret_order[:3]

    intro = _build_dynamic_intro(payload, language, ordered_planets, dom_planets)

    planet_blocks = []
    for planet in dom_planets:
        txt = _planet_text(language, planet)
        planet_blocks.append({
            "key": planet,
            "title": txt["title"],
            "body": txt["body"],
        })

    ret_blocks = []
    for fam in dom_families:
        txt = _ret_text(language, fam)
        fam_label = RET_LABELS[language].get(fam, fam)
        ret_blocks.append({
            "key": fam,
            "title": f"{fam} — {fam_label}",
            "body": txt["body"] or txt["title"],
        })

    sign_blocks = []
    for sign_name in dom_signs:
        txt = _sign_text(language, sign_name)
        sign_blocks.append({
            "key": sign_name,
            "title": txt["title"],
            "body": txt["body"],
        })

    if language == "en":
        title = "Reading of the astrological chart"
        planet_section_title = "Dominant planets"
        ret_section_title = "Dominant RET families"
        sign_section_title = "Dominant signs"
        planet_intro = _txt(INTRO_TEXTS, language, "planet_intro", default="")
        ret_intro = _txt(INTRO_TEXTS, language, "ret_intro", default="")
        sign_intro = _txt(INTRO_TEXTS, language, "sign_intro", default="")
    else:
        title = "Lecture du thème astrologique"
        planet_section_title = "Planètes dominantes"
        ret_section_title = "Familles RET dominantes"
        sign_section_title = "Signes dominants"
        planet_intro = _txt(INTRO_TEXTS, language, "planet_intro", default="")
        ret_intro = _txt(INTRO_TEXTS, language, "ret_intro", default="")
        sign_intro = _txt(INTRO_TEXTS, language, "sign_intro", default="")

    return {
        "title": title,
        "language": language,
        "intro": intro,
        "dominants": {
            "planets": dom_planets,
            "ret_families": dom_families,
            "signs": dom_signs,
        },
        "sections": [
            {
                "key": "planets",
                "title": planet_section_title,
                "intro": planet_intro,
                "blocks": planet_blocks,
            },
            {
                "key": "ret",
                "title": ret_section_title,
                "intro": ret_intro,
                "blocks": ret_blocks,
            },
            {
                "key": "signs",
                "title": sign_section_title,
                "intro": sign_intro,
                "blocks": sign_blocks,
            },
        ],
    }

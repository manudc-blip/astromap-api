from __future__ import annotations

from typing import Dict, List, Iterable, Set, Tuple, Any

from .hierarchisation_conditionaliste import (
    trouver_dominantes_angularite,
    trouver_sous_dominantes_aspects,
    hierarchiser_theme_sans_angulaires,
    PLANET_TIE_ORDER,
)

MAJOR_TYPES = {"CONJ", "OPP", "SQR", "TRI"}


def _build_planet_feats(theme_payload: Dict[str, Any],
                        dom_payload: Dict[str, Any] | None) -> List[Dict[str, Any]]:
    """
    Construit la liste de 'features' planétaires à partir des payloads AstroMap.

    Chaque élément renvoyé est un dict compatible avec hierarchisation_conditionaliste :
      {
        "planete": "Soleil",
        "nom": "Soleil",
        "domitude_deg": float | None,
        "maison": int,
        "pos_maison_deg": float,
        "zone_16": "Zone 1" | ... | None,
        "zone_angulaire": "Zone 1" | ... | None,
        "axe": "AS" | "MC" | "DS" | "FC" | None,
        "est_angulaire": bool,
      }
    """
    planets = theme_payload.get("planets", []) or []
    domitudes = (dom_payload or {}).get("domitudes", []) or []
    dom_by_name = {d.get("planete"): d for d in domitudes}

    feats: List[Dict[str, Any]] = []
    for p in planets:
        name = p.get("name")
        dom = dom_by_name.get(name, {}) if dom_by_name else {}
        zone_locale = dom.get("zone_locale")  # ex: "MC+", "AS+", ...
        axe = None
        if isinstance(zone_locale, str) and len(zone_locale) >= 2:
            prefix = zone_locale[:2]
            if prefix in {"AS", "MC", "DS", "FC"}:
                axe = prefix

        feats.append(
            {
                "planete": name,
                "nom": name,
                "domitude_deg": dom.get("domitude_deg"),
                "maison": dom.get("maison", p.get("house")),
                "pos_maison_deg": dom.get("pos_maison_deg", p.get("house_pos_deg")),
                "zone_16": dom.get("zone_16"),
                "zone_angulaire": dom.get("zone_angulaire"),
                "axe": axe,
                "est_angulaire": bool(dom.get("est_angulaire", False)),
            }
        )
    return feats


def _adapt_aspects(theme_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Adapte la liste d'aspects du payload AstroMap au format attendu par
    hierarchisation_conditionaliste (type 'SXT' au lieu de 'SEX', etc.).
    """
    out: List[Dict[str, Any]] = []
    for a in theme_payload.get("aspects", []) or []:
        atype = a.get("type")
        if atype == "SEX":
            atype = "SXT"
        out.append(
            {
                "p1": a.get("p1") or a.get("planet1") or a.get("A") or a.get("planet_a"),
                "p2": a.get("p2") or a.get("planet2") or a.get("B") or a.get("planet_b"),
                "type": atype,
                "orb": float(a.get("orb", 0.0)),
            }
        )
    return out


def compute_planet_hierarchy(theme_payload: Dict[str, Any],
                             dom_payload: Dict[str, Any] | None):
    """
    Calcule la hiérarchie planétaire conditionaliste à partir des payloads AstroMap.

    Returns
    -------
    ranks : Dict[str, int]
        Rang (1..10) de chaque planète.
    ordered : List[str]
        Liste des planètes dans l'ordre de hiérarchie.
    info : Dict[str, Any]
        Détail des dominantes / sous-dominantes / non-dominantes.
    """
    feats = _build_planet_feats(theme_payload, dom_payload)
    aspects = _adapt_aspects(theme_payload)

    # y a-t-il au moins une angulaire ?
    has_ang = any(bool(f.get("est_angulaire")) for f in feats)

    if has_ang:
        # Thème AVEC angularités
        doms = trouver_dominantes_angularite(feats)
        subs = trouver_sous_dominantes_aspects(feats, aspects)
        already: Set[str] = {d["planete"] for d in doms} | {s["planete"] for s in subs}
        nd = [f["planete"] for f in feats if f["planete"] not in already]
    else:
        # Thème SANS angularités
        doms, subs, nd, _amas = hierarchiser_theme_sans_angulaires(feats, aspects)

    # -------------------------
    # Aplatissement de la hiérarchie avec élimination des doublons
    # (priorité : dominantes > sous-dominantes > non-dominantes)
    # -------------------------
    seen: Set[str] = set()
    ordered: List[str] = []

    doms_unique = []
    for d in doms:
        name = d["planete"]
        if name in seen:
            continue
        doms_unique.append(d)
        seen.add(name)
        ordered.append(name)

    subs_unique = []
    for s in subs:
        name = s["planete"]
        if name in seen:
            continue
        subs_unique.append(s)
        seen.add(name)
        ordered.append(name)

    nd_unique: List[str] = []
    for name in nd:
        if name in seen:
            continue
        nd_unique.append(name)
        seen.add(name)
        ordered.append(name)

    ranks = {name: i + 1 for i, name in enumerate(ordered)}
    info = {"dominantes": doms_unique, "sous_dom": subs_unique, "nd": nd_unique}
    return ranks, ordered, info

def compute_ret_box_colors(
    ordered_planets: List[str],
    angular_set: Set[str],
    aspects: Iterable[Dict[str, Any]],
) -> Dict[str, str]:
    """
    Applique les règles de coloriage des cases RET (noir / gris / blanc).

    Returns
    -------
    colors : Dict[str, str]
        Mapping { "Soleil": "black" | "gray" | "white", ... }
    """
    colors: Dict[str, str] = {p: "white" for p in ordered_planets}
    n_ang = len(angular_set)

    def has_major_aspect_with_nonangular() -> bool:
        """Règle 5) : détecte une non-angulaire en aspect majeur avec une angulaire."""
        for a in aspects:
            atype = a.get("type")
            if atype == "SEX":
                atype = "SXT"
            if atype not in MAJOR_TYPES:
                continue
            p1 = a.get("p1")
            p2 = a.get("p2")
            if p1 in angular_set and p2 not in angular_set:
                return True
            if p2 in angular_set and p1 not in angular_set:
                return True
        return False

    if n_ang == 0:
        # Thèmes sans angularités :
        #  → 4 premières noires, 3 suivantes grises, le reste blanc.
        for p in ordered_planets[:4]:
            colors[p] = "black"
        for p in ordered_planets[4:7]:
            colors[p] = "gray"
        return colors

    if n_ang > 5:
        # > 5 angulaires : 5 premières angulaires noires, autres angulaires grises.
        ang_in_order = [p for p in ordered_planets if p in angular_set]
        for p in ang_in_order[:5]:
            colors[p] = "black"
        for p in ang_in_order[5:]:
            colors[p] = "gray"
        return colors

    if n_ang == 5:
        # 5 angulaires : 5 noires, 3 suivantes (non angulaires) en gris
        ang_in_order = [p for p in ordered_planets if p in angular_set]
        for p in ang_in_order:
            colors[p] = "black"
        # on prend les 3 planètes suivantes dans l'ordre général,
        # en excluant déjà les angulaires
        rest = [p for p in ordered_planets if p not in ang_in_order]
        for p in rest[:3]:
            colors[p] = "gray"
        return colors

    if n_ang == 4:
        # 4 angulaires : 4 noires, 3 grises
        ang_in_order = [p for p in ordered_planets if p in angular_set]
        for p in ang_in_order:
            colors[p] = "black"
        rest = [p for p in ordered_planets if p not in ang_in_order]
        for p in rest[:3]:
            colors[p] = "gray"
        return colors

    if n_ang == 3:
        # 3 angulaires : 3 noires, 4 grises
        ang_in_order = [p for p in ordered_planets if p in angular_set]
        for p in ang_in_order:
            colors[p] = "black"
        rest = [p for p in ordered_planets if p not in ang_in_order]
        for p in rest[:4]:
            colors[p] = "gray"
        return colors

    if n_ang == 2:
        # 2 angulaires + éventuellement une non-angulaire liée par aspect majeur
        ang_in_order = [p for p in ordered_planets if p in angular_set]
        for p in ang_in_order:
            colors[p] = "black"

        extra_black: List[str] = []
        if has_major_aspect_with_nonangular():
            for a in aspects:
                atype = a.get("type")
                if atype == "SEX":
                    atype = "SXT"
                if atype not in MAJOR_TYPES:
                    continue
                p1 = a.get("p1")
                p2 = a.get("p2")
                if p1 in angular_set and p2 not in angular_set:
                    extra_black.append(p2)
                elif p2 in angular_set and p1 not in angular_set:
                    extra_black.append(p1)
            extra_black = [p for p in ordered_planets
                           if p in extra_black and p not in ang_in_order][:1]
            for p in extra_black:
                colors[p] = "black"

        rest = [p for p in ordered_planets if colors[p] == "white"]
        for p in rest[:4]:
            colors[p] = "gray"
        return colors

    if n_ang == 1:
        # 1 seule angulaire : elle + les deux suivantes en noir, 4 suivantes en gris
        ang = next(iter(angular_set))
        if ang in ordered_planets:
            idx = ordered_planets.index(ang)
            for p in ordered_planets[idx:idx + 3]:
                colors[p] = "black"
        rest = [p for p in ordered_planets if colors[p] == "white"]
        for p in rest[:4]:
            colors[p] = "gray"
        return colors

    return colors

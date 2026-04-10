from __future__ import annotations

from typing import Dict, List, Tuple, Any, Set

# ------------------------------------------------------------
# Constantes
# ------------------------------------------------------------

SIGNS = [
    "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
    "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons",
]

# Pondérations de base par planète (VERSION GÉOASTRO, avec Pluton)
PLANET_SIGN_POINTS: Dict[str, int] = {
    "Lune": 10,
    "Soleil": 9,
    "Mercure": 8,
    "Vénus": 7,
    "Mars": 6,
    "Jupiter": 5,
    "Saturne": 4,
    "Uranus": 3,
    "Neptune": 2,
    "Pluton": 1,
}

# Ordre fixe pour les égalités de planètes (HP, etc.)
TIE_BREAK_ORDER = [
    "Lune", "Mercure", "Vénus", "Soleil",
    "Mars", "Jupiter", "Saturne", "Uranus", "Neptune", "Pluton",
]

RAPIDES: Set[str] = {"Lune", "Soleil", "Mercure", "Vénus"}

# ------------------------------------------------------------
# Option : signe à partir de la déclinaison (module GéoAstro)
# ------------------------------------------------------------

try:
    # À condition que positions_planetes.py soit copié dans astromap/core
    from .positions_planetes import sign_from_declination  # type: ignore
except Exception:  # pragma: no cover - fallback si module absent
    sign_from_declination = None  # type: ignore


def _sign_from_lon(lon: float) -> str:
    """Retourne le nom du signe (français) à partir de la longitude écliptique 0..360."""
    idx = int(lon // 30) % 12
    return SIGNS[idx]


def _planet_tie_index(name: str) -> int:
    """Indice pour départager les égalités (plus petit = plus prioritaire)."""
    try:
        return TIE_BREAK_ORDER.index(name)
    except ValueError:
        return len(TIE_BREAK_ORDER) + 1


# ------------------------------------------------------------
# Hiérarchie des signes
# ------------------------------------------------------------

def rank_signs(planets: List[Dict[str, Any]],
               planet_ranks: Dict[str, int] | None = None) -> List[Tuple[str, int]]:
    """
    Classe les signes selon la méthode utilisée dans GéoAstro,
    en partant directement du payload AstroMap (liste de dicts de planètes).

    Si possible, le signe de chaque planète est déterminé via la déclinaison
    (`sign_from_declination(decl, lon)`), sinon on retombe sur le signe
    écliptique simple (_sign_from_lon).

    Scoring pour chaque planète :
        score_planète = PLANET_SIGN_POINTS[name] + bonus_HP
    avec bonus_HP = (11 - rang_HP) si un rang 1..10 est fourni.
    """

    scores: Dict[str, int] = {s: 0 for s in SIGNS}

    for p in planets:
        name = p.get("name")
        if name not in PLANET_SIGN_POINTS:
            continue

        lon = float(p.get("lon", 0.0))
        decl = p.get("decl")
        if decl is None:
            decl = p.get("dec")

        # --- Signe utilisé : δ+λ si possible, sinon λ seul
        if sign_from_declination is not None and decl is not None:
            try:
                sign = sign_from_declination(float(decl), lon)  # type: ignore
            except Exception:
                sign = _sign_from_lon(lon)
        else:
            sign = _sign_from_lon(lon)

        base = PLANET_SIGN_POINTS[name]
        add_rank = 0
        if planet_ranks is not None:
            r = int(planet_ranks.get(name, 0))
            if 1 <= r <= 10:
                add_rank = 11 - r  # rang 1 → +10, rang 10 → +1

        scores[sign] += base + add_rank

    # Tri par score décroissant, puis par ordre zodiacal
    ranked_simple = sorted(
        scores.items(),
        key=lambda kv: (-kv[1], SIGNS.index(kv[0])),
    )
    return ranked_simple


# ------------------------------------------------------------
# Hiérarchie des familles zodiacales (F+/F-/V+/L+/V-/L-/SC/SD/SE)
# ------------------------------------------------------------

def compute_sign_and_family_ranks(
    planets: List[Dict[str, Any]],
    planet_ranks: Dict[str, int] | None = None,
    angular_planets: Set[str] | None = None,
) -> Tuple[Dict[str, int], Dict[str, Dict[str, int]]]:
    """
    Calcule :
      - un dict de points par signe (comme dans rank_signs)
      - les rangs des familles zodiacales :
          reactions:  "Force d'excitation", "Force d'inhibition"
          mobilities: "Vitesse d'excitation", "Lenteur d'excitation",
                      "Vitesse d'inhibition", "Lenteur d'inhibition"
          phases:     "Sens des Contraires", "Sens des Dosages",
                      "Sens des Ensembles"

    `angular_planets` est l'ensemble des noms de planètes angulaires
    (pour compter les angularités par famille, comme dans GéoAstro).
    """

    if angular_planets is None:
        angular_planets = set()

    # 1) Scores par signe + compte de planètes + compte d'angulaires
    sign_points: Dict[str, int] = {s: 0 for s in SIGNS}
    sign_nplan: Dict[str, int] = {s: 0 for s in SIGNS}
    sign_nang: Dict[str, int] = {s: 0 for s in SIGNS}

    for p in planets:
        name = p.get("name")
        if name not in PLANET_SIGN_POINTS:
            continue

        lon = float(p.get("lon", 0.0))
        decl = p.get("decl")
        if decl is None:
            decl = p.get("dec")

        if sign_from_declination is not None and decl is not None:
            try:
                sign = sign_from_declination(float(decl), lon)  # type: ignore
            except Exception:
                sign = _sign_from_lon(lon)
        else:
            sign = _sign_from_lon(lon)

        base = PLANET_SIGN_POINTS[name]
        add_rank = 0
        if planet_ranks is not None:
            r = int(planet_ranks.get(name, 0))
            if 1 <= r <= 10:
                add_rank = 11 - r

        val = base + add_rank
        sign_points[sign] += val
        sign_nplan[sign] += 1
        if name in angular_planets:
            sign_nang[sign] += 1

    # 2) Regroupement en familles
    reactions = {
        "Force d'excitation": ["Bélier", "Gémeaux", "Lion", "Balance", "Sagittaire", "Verseau"],
        "Force d'inhibition": ["Taureau", "Cancer", "Vierge", "Scorpion", "Capricorne", "Poissons"],
    }
    mobilities = {
        "Vitesse d'excitation": ["Bélier", "Taureau", "Gémeaux"],
        "Lenteur d'excitation": ["Cancer", "Lion", "Vierge"],
        "Vitesse d'inhibition": ["Balance", "Scorpion", "Sagittaire"],
        "Lenteur d'inhibition": ["Capricorne", "Verseau", "Poissons"],
    }
    phases = {
        "Sens des Contraires": ["Bélier", "Vierge", "Balance", "Poissons"],
        "Sens des Dosages":    ["Taureau", "Lion", "Scorpion", "Verseau"],
        "Sens des Ensembles":  ["Gémeaux", "Cancer", "Sagittaire", "Capricorne"],
    }

    def _aggregate(fam_map: Dict[str, List[str]]):
        scores, npl, nang = {}, {}, {}
        for fam, signs in fam_map.items():
            scores[fam] = sum(sign_points.get(s, 0) for s in signs)
            npl[fam]    = sum(sign_nplan.get(s, 0)  for s in signs)
            nang[fam]   = sum(sign_nang.get(s, 0)   for s in signs)
        return scores, npl, nang

    def _ranks(scores: Dict[str, int],
               npl: Dict[str, int],
               nang: Dict[str, int],
               order: List[str]) -> Dict[str, int]:
        """
        Classe les familles par score décroissant, puis nombre de planètes,
        puis nombre d'angulaires, puis ordre canonique fixe.
        """
        idx = {name: i for i, name in enumerate(order)}
        items = list(scores.items())
        items.sort(
            key=lambda kv: (
                -kv[1],                # score élevé d'abord
                -npl.get(kv[0], 0),    # plus de planètes
                -nang.get(kv[0], 0),   # plus d'angulaires
                idx.get(kv[0], 999),   # ordre canonique
            )
        )
        return {name: i + 1 for i, (name, _) in enumerate(items)}

    reac_scores, reac_npl, reac_nang = _aggregate(reactions)
    mob_scores, mob_npl, mob_nang   = _aggregate(mobilities)
    ph_scores,  ph_npl,  ph_nang    = _aggregate(phases)

    reactions_ranks = _ranks(
        reac_scores, reac_npl, reac_nang,
        ["Force d'excitation", "Force d'inhibition"],
    )
    mobilities_ranks = _ranks(
        mob_scores, mob_npl, mob_nang,
        [
            "Vitesse d'excitation", "Lenteur d'excitation",
            "Vitesse d'inhibition", "Lenteur d'inhibition",
        ],
    )
    phases_ranks = _ranks(
        ph_scores, ph_npl, ph_nang,
        ["Sens des Contraires", "Sens des Dosages", "Sens des Ensembles"],
    )

    families = {
        "reactions": reactions_ranks,
        "mobilities": mobilities_ranks,
        "phases": phases_ranks,
    }

    return sign_points, families

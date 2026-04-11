
import math

# --- Helpers sphériques pour les aspects en RA/δ (sphère locale) ---

def _deg(x: float) -> float:   # rad -> deg
    return x * 180.0 / math.pi

def _rad(x: float) -> float:   # deg -> rad
    return x * math.pi / 180.0

def _spherical_sep_deg(ra1_deg: float, dec1_deg: float,
                       ra2_deg: float, dec2_deg: float) -> float:
    """
    Angle sphérique grand cercle entre (α1, δ1) et (α2, δ2), en degrés.
    Utilisé pour les aspects en sphère locale (équatorial, RA/δ).
    """
    a1, d1 = _rad(ra1_deg), _rad(dec1_deg)
    a2, d2 = _rad(ra2_deg), _rad(dec2_deg)
    cosd = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(a1 - a2)
    cosd = max(-1.0, min(1.0, cosd))
    return _deg(math.acos(cosd))

# --- Règle conditionaliste : pas de sextiles à partir de Saturne ---

EXCLUDE_SEXTILES_FROM_SATURN_ON = True
TRANS_SATURN = {"Saturne", "Saturn", "Uranus", "Neptune", "Pluton", "Pluto"}

# =========================
# PATCH ORBES — AstroAriana
# =========================

# Mapping noms FR -> clés internes d'aspects
_ASP_KEY = {
    "Conjonction": "CONJ",
    "Opposition":  "OPP",
    "Carré":       "SQR",
    "Trigone":     "TRI",
    "Sextile":     "SEX",
    # on accepte déjà les clés internes si elles arrivent ainsi
    "CONJ": "CONJ", "OPP": "OPP", "SQR": "SQR", "TRI": "TRI", "SEX": "SEX",
}

def _pair_key_from_tuple(t):
    """(1,1)->g1_g1 ; (2,1)->g2_g1 ; accepte aussi 'g1_g1' inchangé."""
    if isinstance(t, str):
        # déjà normalisé (g1_g1 / g1_g2 / etc.)
        return t.lower()
    if not (isinstance(t, tuple) and len(t) == 2):
        raise ValueError(f"Clé de groupe invalide: {t!r}")
    a, b = t
    return f"g{int(a)}_g{int(b)}".lower()

def _normalize_orb_cfg(user_cfg):
    """
    Convertit une table d'orbes FR:
      { 'Trigone': {(1,1): 9, (2,2): 7, (1,2): 8, (2,1): 8}, ... }
    en format interne:
      { 'TRI': {'g1_g1': 9, 'g2_g2': 7, 'g1_g2': 8}, ... }
    Note: g1_g2 et g2_g1 sont fusionnés (même valeur).
    """
    norm = {}
    for asp_label, group_table in user_cfg.items():
        k = _ASP_KEY.get(asp_label)
        if not k:
            raise KeyError(f"Aspect inconnu: {asp_label!r}")
        dst = {}
        for pair, val in group_table.items():
            pkey = _pair_key_from_tuple(pair)
            if pkey in ("g1_g2", "g2_g1"):
                # on stocke une seule entrée pour les mixtes
                dst["g1_g2"] = float(val)
            else:
                dst[pkey] = float(val)
        norm[k] = dst
    return norm

# ---- Tes orbes (table FR) ----
_ORBES_FR_RAW = {
    "Conjonction": {(1, 1): 18, (2, 2): 14, (1, 2): 16, (2, 1): 16},
    "Opposition":  {(1, 1): 18, (2, 2): 14, (1, 2): 16, (2, 1): 16},
    "Carré":       {(1, 1): 9,  (2, 2): 7,  (1, 2): 8,  (2, 1): 8},
    "Trigone":     {(1, 1): 9,  (2, 2): 7,  (1, 2): 8,  (2, 1): 8},
    "Sextile":     {(1, 1): 5,  (2, 2): 3,  (1, 2): 4,  (2, 1): 4},
}

# ---- Config normalisée utilisable par le moteur ----
ORB_CFG_DEFAULT = _normalize_orb_cfg(_ORBES_FR_RAW)

ASPECTS = {"CONJ":0,"OPP":180,"TRI":120,"SQR":90,"SEX":60}

def angular_sep(a, b):
    d = abs((a-b+180) % 360 - 180)
    return d

# Groupes de planètes (rapides vs lentes)
GROUP1 = {"Soleil", "Sun", "Lune", "Moon", "Mercure", "Mercury", "Vénus", "Venus", "Mars"}
GROUP2 = {"Jupiter", "Saturne", "Saturn", "Uranus", "Neptune", "Pluton", "Pluto"}

def group_of(name: str) -> str:
    if name in GROUP1:
        return "g1"
    if name in GROUP2:
        return "g2"
    return "g1"  # défaut robuste

def orb_for(a_name, b_name, kind, orb_cfg):
    g1 = group_of(a_name); g2 = group_of(b_name)
    key = f"{g1}_{g2}" if g1<=g2 else f"{g2}_{g1}"
    return (orb_cfg.get(kind, {}) or {}).get(key, 6.0)

def detect_aspects(planets, orb_cfg=None, exclude_sextiles_from_saturn=None):
    """
    Détection des aspects planétaires avec orbes G1/G2,
    en utilisant la *sphère locale* (coordonnées équatoriales RA/δ) quand c'est possible.

    - On cherche un seul aspect par paire (priorité : CONJ > OPP > SQR > TRI > SEX).
    - Les orbes sont pris dans orb_cfg (par défaut ORB_CFG_DEFAULT).
    - Règle conditionaliste : pas de sextiles à partir de Saturne (incluse) si
      EXCLUDE_SEXTILES_FROM_SATURN_ON = True.
    """
    if orb_cfg is None:
        orb_cfg = ORB_CFG_DEFAULT
    if exclude_sextiles_from_saturn is None:
        exclude_sextiles_from_saturn = EXCLUDE_SEXTILES_FROM_SATURN_ON

    out = []

    n = len(planets)
    for i in range(n):
        for j in range(i + 1, n):
            p1 = planets[i]
            p2 = planets[j]

            name1 = p1.get("name")
            name2 = p2.get("name")

            # --- Séparation angulaire : priorité à RA/δ, fallback sur longitude écliptique ---

            ra1 = p1.get("ra")
            dec1 = p1.get("decl")
            ra2 = p2.get("ra")
            dec2 = p2.get("decl")

            if ra1 is not None and dec1 is not None and ra2 is not None and dec2 is not None:
                # Aspects en sphère locale (équatorial)
                sep = _spherical_sep_deg(float(ra1), float(dec1),
                                         float(ra2), float(dec2))  # 0..180
            else:
                # Fallback robuste : aspects en zodiaque écliptique classique
                sep = angular_sep(float(p1["lon"]), float(p2["lon"]))

            # --- Test contre les angles canoniques avec orbes G1/G2 ---

            # Priorité: CONJ > OPP > SQR > TRI > SEX
            for kind in ("CONJ", "OPP", "SQR", "TRI", "SEX"):
                exact = ASPECTS[kind]

                # règle: pas de sextiles à partir de Saturne (incluse)
                if (kind == "SEX"
                    and exclude_sextiles_from_saturn
                    and (name1 in TRANS_SATURN or name2 in TRANS_SATURN)):
                    continue

                orb = orb_for(name1, name2, kind, orb_cfg)
                delta = abs(sep - exact)

                if delta <= orb:
                    out.append({
                        "p1": name1,
                        "p2": name2,
                        "type": kind,            # "CONJ","OPP","SQR","TRI","SEX"
                        "orb": round(delta, 2),  # écart à l’aspect exact
                        "exact": round(sep, 3),  # distance angulaire réelle (optionnel)
                    })
                    # Un seul aspect par paire de planètes
                    break

    return out

def detect_aspects_between(planets_a, planets_b, orb_cfg=None,
                          side_a="A", side_b="B", exclude_sextiles_from_saturn=None):
    """
    Détecte les aspects *entre deux ensembles* de planètes (A ↔ B).

    Utile pour les transits : Transits → Natal (T ↔ N) sans ambiguïté,
    y compris quand la même planète existe des deux côtés (ex: Soleil natal + Soleil en transit).

    Retourne une liste de dicts au format proche de detect_aspects(), avec en plus :
      - side1 / side2 : side_a / side_b
      - base1 / base2 : noms planètes sans suffixe
    """
    if orb_cfg is None:
        orb_cfg = ORB_CFG_DEFAULT

    if exclude_sextiles_from_saturn is None:
        exclude_sextiles_from_saturn = EXCLUDE_SEXTILES_FROM_SATURN_ON

    out = []

    if not planets_a or not planets_b:
        return out

    # On cherche un seul aspect par paire (priorité : CONJ > OPP > SQR > TRI > SEX)
    for p1 in planets_a:
        name1 = p1.get("name")
        if not name1:
            continue
        for p2 in planets_b:
            name2 = p2.get("name")
            if not name2:
                continue

            # --- Séparation angulaire : priorité à RA/δ, fallback sur longitude écliptique ---
            ra1 = p1.get("ra")
            dec1 = p1.get("decl")
            ra2 = p2.get("ra")
            dec2 = p2.get("decl")

            if ra1 is not None and dec1 is not None and ra2 is not None and dec2 is not None:
                sep = _spherical_sep_deg(float(ra1), float(dec1),
                                         float(ra2), float(dec2))  # 0..180
            else:
                sep = angular_sep(float(p1["lon"]), float(p2["lon"]))

            for kind in ("CONJ", "OPP", "SQR", "TRI", "SEX"):
                exact = ASPECTS[kind]

                # règle: pas de sextiles à partir de Saturne (incluse)
                if (kind == "SEX"
                    and exclude_sextiles_from_saturn
                    and (name1 in TRANS_SATURN or name2 in TRANS_SATURN)):
                    continue

                orb = orb_for(name1, name2, kind, orb_cfg)
                delta = abs(sep - exact)

                if delta <= orb:
                    out.append({
                        "p1": name1,
                        "p2": name2,
                        "side1": side_a,
                        "side2": side_b,
                        "base1": name1,
                        "base2": name2,
                        "type": kind,
                        "orb": round(delta, 2),
                        "exact": round(sep, 3),
                    })
                    break

    return out

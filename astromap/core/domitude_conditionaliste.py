import math
import swisseph as swe
from datetime import datetime
import math
import swisseph as swe
from datetime import datetime
from .coords import ecliptic_to_equatorial   # ⇐ NOUVEL IMPORT
try:
    from .positions_planetes import sign_from_declination
except Exception:
    sign_from_declination = None

def normaliser_radian(r):
    return r % (2 * math.pi)

def normaliser_degre(d):
    return d % 360

# === Constantes planètes et noms ===
planetes = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
            swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]
noms_planetes = ["Soleil", "Lune", "Mercure", "Vénus", "Mars",
                 "Jupiter", "Saturne", "Uranus", "Neptune", "Pluton"]

# === Constantes signes (0° Bélier, 30° Taureau, etc.) ===================
SIGN_NAMES = [
    "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
    "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"
]

def normaliser_radian(r):
    return r % (2 * math.pi)

def normaliser_degre(d):
    return d % 360

# === Constantes planètes et noms ===
planetes = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
            swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO]
noms_planetes = ["Soleil", "Lune", "Mercure", "Vénus", "Mars",
                 "Jupiter", "Saturne", "Uranus", "Neptune", "Pluton"]

# === Zones de la sphère locale ===
zones_sphere_locale = {
    "MC+": (0, 18),
    "MC-": (-20, 0),
    "AS+": (90, 105),
    "AS-": (70, 90),
    "FC+": (180, 195),
    "FC-": (165, 180),
    "DS+": (270, 290),
    "DS-": (255, 270),
    # ... autres zones si besoin
}

# ------------------------------------------------------------------ 
# CALCUL DE LA DOMITUDE (algorithme Azimut35)
# ------------------------------------------------------------------

def calcul_domitude(ar_rad, decl_rad, tsn_rad, latitude_rad):
    # Sinus(DA) = Tan(lat) * Tan(déclinaison)
    sin_DA = math.tan(latitude_rad) * math.tan(decl_rad)
    # clamp pour éviter les erreurs numériques
    sin_DA = max(min(sin_DA, 1), -1)
    DA = math.asin(sin_DA)

    SAD = math.pi / 2 + DA    # semi-arc diurne
    SAN = math.pi - SAD       # semi-arc nocturne

    # dm = AR - TSN, normalisée sur 0..2π
    dm = ar_rad - tsn_rad
    if dm < 0:
        dm += 2 * math.pi

    # Transformation selon l’algorithme que tu as donné
    if dm <= SAD:
        dm = dm * (math.pi / 2) / SAD
    elif dm > SAD and (dm - math.pi) >= SAN:
        dm = (dm - 2 * math.pi) * (math.pi / 2) / SAD
    elif dm > SAD and (dm - math.pi) < SAN and dm <= math.pi:
        dm = (dm - math.pi) * (math.pi / 2) / SAN + math.pi
    else:
        dm = (dm - math.pi) * (math.pi / 2) / SAN + math.pi

    # retour en degrés 0..360
    return normaliser_degre(math.degrees(normaliser_radian(dm)))

def trouver_maison(dom_deg):
    """
    0° de domitude = cuspide X, 30° = XI, 60° = XII, 90° = I, etc.
    On retrouve l’indice de maison 1..12 et la position dans la maison (0..30°).
    """
    slot = int(dom_deg // 30)        # 0..11 (0 = secteur autour du MC)
    maison = ((slot + 9) % 12) + 1   # 0->10 (X), 1->11, 2->12, 3->1, ...
    pos = dom_deg % 30
    return maison, pos

# === Zones 1..16 (définition par maison + position 0..30°) ==============
# même logique que celle que nous avons utilisée dans Solarius

def attribuer_zone_16(maison: int, pos_maison_deg: float) -> str:
    m = maison
    p = float(pos_maison_deg)

    # 1) ZONES ANGULAIRES (priorité maximale)
    if (m == 12 and p >= 10) or (m == 1 and p <= 15):
        return "Zone 1"
    if (m == 10 and p <= 18) or (m == 9 and p >= 10):
        return "Zone 2"
    if (m == 7 and p <= 20) or (m == 6 and p >= 15):
        return "Zone 3"
    if (m == 3 and p >= 15) or (m == 4 and p <= 15):
        return "Zone 4"

    # 2) ZONES NON ANGULAIRES
    if m == 12 and p < 10:
        return "Zone 5"
    if m == 9 and p < 10:
        return "Zone 6"
    if m == 1 and p > 15:
        return "Zone 7"
    if m == 10 and p > 18:
        return "Zone 8"
    if m == 7 and p > 20:
        return "Zone 9"
    if m == 6 and p < 15:
        return "Zone 10"
    if m == 3 and p < 15:
        return "Zone 11"
    if m == 4 and p > 15:
        return "Zone 12"

    # 3) MAISONS ÉLOIGNÉES DES AXES
    if m == 11:
        return "Zone 13"
    if m == 8:
        return "Zone 14"
    if m == 2:
        return "Zone 15"
    if m == 5:
        return "Zone 16"

    return "Zone 16"

def is_angulaire(zone_16: str) -> bool:
    return zone_16 in {"Zone 1", "Zone 2", "Zone 3", "Zone 4"}

def identifier_zone(dom_deg):
    """
    Retourne la zone locale MC+/MC-/AS+/AS-/... en fonction de la domitude.
    """
    x = dom_deg % 360
    for nom_zone, (start, end) in zones_sphere_locale.items():
        s, e = start % 360, end % 360
        if s <= e:
            if s <= x < e:
                return nom_zone
        else:
            # intervalle qui traverse 360->0
            if x >= s or x < e:
                return nom_zone
    return None

# ------------------------------------------------------------------ 
# FONCTION UTILISÉE PAR AstroMap
# ------------------------------------------------------------------

def calc_domitude_features(date_naissance: datetime,
                           latitude_deg: float,
                           longitude_deg: float):
    """
    Calcule la domitude pour les 10 planètes principales.

    date_naissance : datetime en UTC (dt_utc fourni par main.py)
    latitude_deg   : latitude géographique
    longitude_deg  : longitude géographique
    """
    # JD UT (on prend directement l’heure UTC que tu fournis)
    jd_ut = swe.julday(
        date_naissance.year,
        date_naissance.month,
        date_naissance.day,
        date_naissance.hour + date_naissance.minute / 60.0
    )

    # Temps sidéral local (en radians) : TSN = sidtime * 15° + longitude
    lst_rad = math.radians(swe.sidtime(jd_ut) * 15 + longitude_deg)
    latitude_rad = math.radians(latitude_deg)

    out = []
    for i, p in enumerate(planetes):
        # Position équatoriale : AR (ascension droite), déclinaison
        pos_eq, _ = swe.calc_ut(jd_ut, p, flags=swe.FLG_EQUATORIAL)
        ar_deg = pos_eq[0]
        decl_deg = pos_eq[1]
        decl_rad = math.radians(decl_deg)
        ar_rad = math.radians(ar_deg)

        # Position écliptique pour connaître la longitude
        pos_ecl, _ = swe.calc_ut(jd_ut, p)  # par défaut : longitude/latitude écliptique
        lon_ecl_deg = pos_ecl[0]

        # Domitude en degrés 0..360
        dom_deg = calcul_domitude(ar_rad, decl_rad, lst_rad, latitude_rad)

        # Signe local (sphère locale) si la fonction est dispo
        sign_local = None
        if sign_from_declination is not None:
            try:
                # fonction GéoAstro : signe en sphère locale à partir de δ et λ
                sign_local = sign_from_declination(decl_deg, lon_ecl_deg)
            except Exception:
                sign_local = None

        # Maison et position dans la maison
        maison, pos = trouver_maison(dom_deg)

        # Zone locale (MC+, AS-, etc.)
        zone_locale = identifier_zone(dom_deg)

        # Zone 1..16 et caractère angulaire
        zone16 = attribuer_zone_16(maison, pos)
        ang = is_angulaire(zone16)

        out.append({
            "planete": noms_planetes[i],
            "domitude_deg": dom_deg,
            "maison": maison,
            "pos_maison_deg": pos,
            "zone_locale": zone_locale,
            "zone_16": zone16,
            "est_angulaire": ang,
            "zone_angulaire": zone16 if ang else None,
            "sign_local": sign_local,
        })

    return out

def calc_sign_domitudes(date_naissance: datetime,
                        latitude_deg: float,
                        longitude_deg: float):
    """
    Calcule la domitude des 12 débuts de signes : 0° Bélier, 0° Taureau, ..., 0° Poissons.

    Retourne une liste de 12 dicts :
    [
        {
            "signe": "Bélier",
            "index": 1,
            "lon_ecliptique_deg": 0.0,
            "domitude_deg": ...,
        },
        ...
    ]
    """
    # JD UT, comme dans calc_domitude_features
    jd_ut = swe.julday(
        date_naissance.year,
        date_naissance.month,
        date_naissance.day,
        date_naissance.hour + date_naissance.minute / 60.0
    )

    # Temps sidéral local (en radians)
    lst_rad = math.radians(swe.sidtime(jd_ut) * 15 + longitude_deg)
    latitude_rad = math.radians(latitude_deg)

    out = []
    for idx, name in enumerate(SIGN_NAMES):
        # 0°, 30°, 60° ... 330° écliptiques, latitude = 0
        lon_ecl = idx * 30.0
        ra_deg, dec_deg = ecliptic_to_equatorial(lon_ecl, 0.0, jd_ut)

        ar_rad = math.radians(ra_deg)
        decl_rad = math.radians(dec_deg)

        # Domitude en degrés 0..360 (même algorithme que pour les planètes)
        dom_deg = calcul_domitude(ar_rad, decl_rad, lst_rad, latitude_rad)

        out.append({
            "signe": name,
            "index": idx + 1,              # 1 = Bélier, 2 = Taureau, etc.
            "lon_ecliptique_deg": lon_ecl,
            "domitude_deg": dom_deg,
        })

    return out
def build_domitude_payload(date_naissance: datetime,
                           latitude_deg: float,
                           longitude_deg: float):
    """
    Construit un payload prêt à être consommé par DomitudeView :
    - 'domitudes'    : liste des planètes en domitude
    - 'sign_domitudes': liste des 12 débuts de signes en domitude
    """
    dom_planets = calc_domitude_features(date_naissance,
                                         latitude_deg,
                                         longitude_deg)
    dom_signs = calc_sign_domitudes(date_naissance,
                                    latitude_deg,
                                    longitude_deg)
    return {
        "domitudes": dom_planets,
        "sign_domitudes": dom_signs,
    }

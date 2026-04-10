from datetime import datetime
from math import fmod
import math
import importlib
import os

os.environ["SWEPH_EPHE_PATH"] = r"C:\chemin\vers\tes\ephemerides"

PLANETS = ["Soleil","Lune","Mercure","Vénus","Mars","Jupiter","Saturne","Uranus","Neptune","Pluton"]

def has_swe():
    return importlib.util.find_spec("swisseph") is not None

def _demo_positions():
    lons = [0, 12, 40, 88, 132, 210, 250, 300, 330, 15]
    return [{"name": PLANETS[i], "lon": float(lons[i] % 360), "lat": 0.0} for i in range(len(PLANETS))]

def _swe_calc_ut_safe(swe, jd, ipl):
    """Retourne (lon, lat, dist) robustement pour swisseph."""
    res = swe.calc_ut(jd, ipl)
    # Certains builds renvoient (values, retflag)
    if isinstance(res, (list, tuple)) and len(res) == 2 and isinstance(res[0], (list, tuple)):
        vals = res[0]
    else:
        vals = res
    lon = float(vals[0])
    lat = float(vals[1]) if len(vals) > 1 else 0.0
    dist = float(vals[2]) if len(vals) > 2 else 1.0
    return lon, lat, dist

def compute_positions(dt_utc: datetime, latitude: float, longitude: float, altitude: float = 0.0):
    """Retourne les positions planétaires avec infos étendues.

    Pour chaque planète :
      - lon            : longitude écliptique (0..360)
      - lat            : latitude écliptique
      - daily_motion   : pas journalier en longitude (°/jour)
      - ra             : ascension droite (°)
      - decl           : déclinaison (°)
      - height         : hauteur (altitude, °)
      - azimut         : azimut (°)
    """
    if not has_swe():
        # mode démo : on garde la forme mais sans les champs avancés
        demo = _demo_positions()
        for d in demo:
            d.update({
                "daily_motion": None,
                "ra": None,
                "decl": None,
                "height": None,
                "azimut": None,
            })
        return demo

    import swisseph as swe

    # Altitude facultative
    try:
        swe.set_topo(longitude, latitude, float(altitude or 0.0))
    except Exception:
        pass

    # julian day (UT)
    jd = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0,
    )

    results = []
    mapping = {
        "Soleil":  swe.SUN,
        "Lune":    swe.MOON,
        "Mercure": swe.MERCURY,
        "Vénus":   swe.VENUS,
        "Mars":    swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturne": swe.SATURN,
        "Uranus":  swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluton":  swe.PLUTO,
    }

    # temps sidéral local (deg)
    lst_hours = swe.sidtime(jd)
    lst_deg = (lst_hours * 15.0 + longitude) % 360.0

    for name, ipl in mapping.items():
        daily_motion = None
        try:
            vals, _ = swe.calc_ut(jd, ipl, swe.FLG_SWIEPH | swe.FLG_SPEED)
            lon = float(vals[0])
            lat = float(vals[1])
            daily_motion = float(vals[3])
        except Exception:
            lon, lat, _dist = _swe_calc_ut_safe(swe, jd, ipl)

        lon = float(fmod(lon, 360.0))
        lat = float(lat)

        try:
            vals_eq, _ = swe.calc_ut(jd, ipl, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
            ra = float(vals_eq[0]) % 360.0
            decl = float(vals_eq[1])
        except Exception:
            ra = None
            decl = None

        height = None
        azimut = None
        try:
            if ra is not None and decl is not None:
                phi = math.radians(latitude)
                ra_rad = math.radians(ra)
                dec_rad = math.radians(decl)

                H_deg = (lst_deg - ra) % 360.0
                H_rad = math.radians(H_deg)

                sin_alt = (
                    math.sin(phi) * math.sin(dec_rad)
                    + math.cos(phi) * math.cos(dec_rad) * math.cos(H_rad)
                )
                sin_alt = max(-1.0, min(1.0, sin_alt))
                alt_rad = math.asin(sin_alt)
                height = math.degrees(alt_rad)

                y = -math.sin(H_rad) * math.cos(dec_rad)
                x = (
                    math.sin(dec_rad) - math.sin(phi) * math.sin(alt_rad)
                ) / (math.cos(phi) * math.cos(alt_rad) + 1e-12)
                az_rad = math.atan2(y, x)
                azimut = (math.degrees(az_rad) + 360.0) % 360.0
        except Exception:
            pass

        results.append({
            "name":         name,
            "lon":          lon,
            "lat":          lat,
            "daily_motion": daily_motion,
            "ra":           ra,
            "decl":         decl,
            "height":       height,
            "azimut":       azimut,
        })

    return results

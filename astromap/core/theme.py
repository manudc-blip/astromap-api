from dataclasses import dataclass
from datetime import datetime
import pytz
from .eph import compute_positions
from .houses import compute_houses_ecliptic
from .aspects import detect_aspects
from .config import load_config

# --- NEW: utilitaire pour annoter les planètes avec leur maison ---
def _assign_planet_houses(planets, houses):
    """
    Ajoute à chaque planète:
      - planet["house"]        = n° de maison (1..12)
      - planet["house_pos_deg"] = position 0..30° dans la maison
    en se basant sur les cuspides écliptiques calculées par compute_houses_ecliptic.
    """

    def _in_interval(lon, start, end):
        """Vrai si lon appartient à l’intervalle start→end sur le cercle."""
        lon = lon % 360.0
        start = start % 360.0
        end = end % 360.0

        if start == end:
            # cas dégénéré : couvre tout le cercle
            return True

        if start < end:
            return start <= lon < end
        else:
            # intervalle qui traverse 360°→0°
            return lon >= start or lon < end

    if not planets or not houses:
        return

    for p in planets:
        try:
            lon = float(p.get("lon", 0.0)) % 360.0
        except Exception:
            lon = 0.0

        best_house = None
        best_start = None

        for h in houses:
            try:
                start = float(h.get("lon_start"))
            except Exception:
                continue
            try:
                end = float(h.get("lon_end"))
            except Exception:
                # fallback 30°
                end = (start + 30.0) % 360.0

            if _in_interval(lon, start, end):
                best_house = int(h.get("i", 0)) or None
                best_start = start
                break

        # fallback : la cuspide la plus proche si rien trouvé (robuste)
        if best_house is None and houses:
            h = min(
                houses,
                key=lambda hh: (lon - float(hh.get("lon_start", 0.0)) + 360.0) % 360.0
            )
            best_house = int(h.get("i", 0)) or None
            best_start = float(h.get("lon_start", 0.0))

        if best_house is not None:
            p["house"] = best_house
            if best_start is not None:
                # on ramène dans [0,30[
                p["house_pos_deg"] = (lon - best_start + 360.0) % 30.0

@dataclass
class ThemeResult:
    payload: dict
    def to_json(self): return self.payload

def _parse_tz(tz_str: str):
    # "Europe/Paris" ou "+01:00" / "-07:00"
    if "/" in tz_str:
        return pytz.timezone(tz_str)
    s = tz_str.strip()
    sign = 1 if s.startswith("+") else -1
    parts = s.replace("+","").replace("-","").split(":")
    hh = int(parts[0]) if parts and parts[0] else 0
    mm = int(parts[1]) if len(parts) > 1 else 0
    return pytz.FixedOffset(sign * (hh*60 + mm))

def _sign_from_lon_fr(lon: float) -> str:
    """Convertit une longitude écliptique (0..360) en nom de signe FR."""
    signs = [
        "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
        "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons",
    ]
    if lon is None:
        return ""
    lon = float(lon) % 360.0
    return signs[int(lon // 30) % 12]

class Theme:
    @staticmethod
    def compute(name, datetime_local: str, latitude: float, longitude: float, tz: str, settings: dict):
        cfg = load_config()
        tzinfo = _parse_tz(tz)
        dt_local = tzinfo.localize(datetime.strptime(datetime_local, "%Y-%m-%d %H:%M"))
        dt_utc = dt_local.astimezone(pytz.UTC)

        # Altitude par défaut = 0 (champ supprimé côté UI)
        planets = compute_positions(dt_utc, latitude, longitude, altitude=0.0)

        # --- Maisons & axes ---
        # Avec SwissEph : compute_houses_ecliptic -> (houses, axes)
        # Sans SwissEph : fallback maisons égales + orientation AstroAriana
        try:
            result = compute_houses_ecliptic({
                "dt_utc": dt_utc,
                "lat": latitude,
                "lon": longitude,
            })
            if isinstance(result, tuple):
                houses, axes = result
            else:
                houses = result
                axes = {"AS": 180.0, "DS": 0.0, "MC": 90.0, "IC": 270.0}
        except Exception:
            houses = compute_houses_ecliptic({"ascendant": 180.0})
            axes = {"AS": 180.0, "DS": 0.0, "MC": 90.0, "IC": 270.0}

        # Annoter les planètes avec leur maison/position dans la maison
        _assign_planet_houses(planets, houses)

        orbs = cfg.get("aspects", {}).get("orbs")
        aspects = detect_aspects(
            planets,
            orbs if orbs else None,
            exclude_sextiles_from_saturn=False
        )

        # --- Ascendant (signe) ---
        asc_lon = axes.get("AS", None)
        asc_sign = _sign_from_lon_fr(asc_lon)

        return ThemeResult({
            "meta": {"name": name, "datetime_utc": dt_utc.isoformat(), "tz": tz},
            "settings": {"house_system": settings.get("house_system","Placidus"), "domitude": {"enabled": False}},
            "axes": axes,
            "asc_sign": asc_sign,
            "ascendant": {"lon": asc_lon, "sign": asc_sign},
            "houses": houses,
            "planets": planets,
            "aspects": aspects,
        })

import math
import swisseph as swe

def ecliptic_to_equatorial(lon_deg: float,
                           lat_deg: float,
                           jd_ut: float) -> tuple[float, float]:
    """
    Convertit des coordonnées écliptiques (longitude, latitude, en degrés)
    en coordonnées équatoriales (ascension droite, déclinaison, en degrés),
    en utilisant l'obliquité de l'écliptique pour la date (Swiss Ephemeris).
    """
    # Obliquité de l'écliptique pour la date (en degrés)
    # Swiss Ephemeris renvoie un tuple complexe : (obliquité, nutation)
    obl = swe.calc_ut(jd_ut, swe.ECL_NUT)[0]

    # obliquité vraie = premier élément
    eps_deg = float(obl[0])

    eps = math.radians(eps_deg)

    lam = math.radians(lon_deg)
    beta = math.radians(lat_deg)

    # Formules standard écliptique -> équatorial
    sin_dec = (math.sin(beta) * math.cos(eps) +
               math.cos(beta) * math.sin(eps) * math.sin(lam))
    dec = math.asin(sin_dec)

    y = math.sin(lam) * math.cos(eps) - math.tan(beta) * math.sin(eps)
    x = math.cos(lam)
    ra = math.atan2(y, x)

    ra_deg = (math.degrees(ra) % 360.0)
    dec_deg = math.degrees(dec)
    return ra_deg, dec_deg

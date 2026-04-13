def _fallback_equal(asc_deg: float):
    houses = []
    for i in range(12):
        start = (asc_deg + i*30.0) % 360.0
        end = (start + 30.0) % 360.0
        houses.append({"i": i+1, "lon_start": start, "lon_end": end})
    return houses

def compute_houses_ecliptic(settings: dict):
    """
    Si SwissEph est présent -> Placidus + vrais AS/MC.
    Sinon -> fallback 12 maisons égales, AS fourni par settings (ou 90° à gauche).
    """
    import importlib, math

    asc_given = float(settings.get("ascendant", 90.0))  # 90° = haut ; on redéfinit plus loin si SWE
    if not (importlib.util.find_spec("swisseph") or importlib.util.find_spec("pyswisseph")):
        return _fallback_equal(asc_given)

    import swisseph as swe

    dt_utc = settings["dt_utc"]           # datetime aware UTC (fourni par Theme)
    lat = float(settings["lat"]); lon = float(settings["lon"])

    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                    dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0)

    # Placidus, positions écliptiques vraies
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P')  # b'P' = Placidus
    # ascmc: [ASC, MC, ARMC, Vertex, Equasc, CoAsc1, CoAsc2, PolAsc, ...] selon build
    asc = float(ascmc[0]) % 360.0
    mc  = float(ascmc[1]) % 360.0

    houses = []
    for i in range(12):
        start = float(cusps[i]) % 360.0
        end   = float(cusps[(i+1) % 12]) % 360.0
        houses.append({"i": i+1, "lon_start": start, "lon_end": end})

    return houses, {"AS": asc, "MC": mc, "DS": (asc+180)%360, "IC": (mc+180)%360}

from datetime import datetime

from astromap.core.theme import Theme
from astromap.core.domitude_conditionaliste import build_domitude_payload


def compute_theme_payload(
    name: str,
    datetime_local: str,
    latitude: float,
    longitude: float,
    tz: str,
    settings: dict,
) -> dict:
    # 1) Calcul du thème avec la logique correcte de conversion locale -> UTC
    result = Theme.compute(
        name=name,
        datetime_local=datetime_local,
        latitude=latitude,
        longitude=longitude,
        tz=tz,
        settings=settings,
    )

    data = result.to_json()

    # 2) Récupérer la datetime UTC réellement utilisée par Theme.compute
    #    puis la passer au moteur de domitude
    dt_utc_raw = data.get("meta", {}).get("datetime_utc")
    if not dt_utc_raw:
        raise ValueError("datetime_utc missing from theme payload metadata")

    # isoformat avec offset, ex: 1986-04-15T12:21:00+00:00
    dt_utc = datetime.fromisoformat(dt_utc_raw)

    # Le moteur de domitude attend une datetime UTC exploitable directement.
    # On enlève le tzinfo pour rester cohérent avec le moteur Tkinter.
    dt_utc_naive = dt_utc.replace(tzinfo=None)

    domitude_data = build_domitude_payload(
        date_naissance=dt_utc_naive,
        latitude_deg=latitude,
        longitude_deg=longitude,
    )

    data.update(domitude_data)
    return data

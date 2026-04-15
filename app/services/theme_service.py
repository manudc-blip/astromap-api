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
    result = Theme.compute(
        name=name,
        datetime_local=datetime_local,
        latitude=latitude,
        longitude=longitude,
        tz=tz,
        settings=settings,
    )

    data = result.to_json()

    dt_obj = datetime.strptime(datetime_local, "%Y-%m-%d %H:%M")

    domitude_data = build_domitude_payload(
        date_naissance=dt_obj,
        latitude_deg=latitude,
        longitude_deg=longitude,
    )
    data.update(domitude_data)

    return data

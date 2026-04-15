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

    domitude_data = build_domitude_payload(
        data,
        latitude_deg=latitude,
        longitude_deg=longitude,
    )
    data.update(domitude_data)

    return data

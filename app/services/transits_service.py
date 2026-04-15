from astromap.core.transits import Transits


def compute_transits_payload(
    name: str,
    natal_datetime_local: str,
    transit_datetime_local: str,
    latitude: float,
    longitude: float,
    tz: str,
    settings: dict,
    aspect_mode: str = "TN",
) -> dict:
    result = Transits.compute(
        name=name,
        natal_datetime_local=natal_datetime_local,
        transit_datetime_local=transit_datetime_local,
        latitude=latitude,
        longitude=longitude,
        tz=tz,
        settings=settings,
        aspect_mode=aspect_mode,
    )
    return result.to_json()

from astromap.core.theme import Theme


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
    return result.to_json()

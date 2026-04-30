from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import pytz

from .eph import compute_positions
from .aspects import detect_aspects, detect_aspects_between
from .theme import Theme, _parse_tz


@dataclass
class TransitResult:
    payload: dict

    def to_json(self):
        return self.payload


class Transits:
    @staticmethod
    def compute(
        name: str,
        natal_datetime_local: str,
        transit_datetime_local: str,
        latitude: float,
        longitude: float,
        tz: str,
        settings: dict,
        aspect_mode: str = "TN",
    ):
        natal = Theme.compute(
            name=name,
            datetime_local=natal_datetime_local,
            latitude=latitude,
            longitude=longitude,
            tz=tz,
            settings=settings,
        ).to_json()

        tzinfo = _parse_tz(tz)
        dt_local = tzinfo.localize(datetime.strptime(transit_datetime_local, "%Y-%m-%d %H:%M"))
        dt_utc = dt_local.astimezone(pytz.UTC)

        transit_planets = compute_positions(dt_utc, latitude, longitude, altitude=0.0)

        mode = (aspect_mode or "TN").upper()
        if mode == "TT":
            transit_aspects = detect_aspects(transit_planets, exclude_sextiles_from_saturn=False)
        else:
            transit_aspects = detect_aspects_between(
                transit_planets,
                natal.get("planets", []),
                side_a="T",
                side_b="N",
                exclude_sextiles_from_saturn=False,
            )

        payload = {
            "meta": {
                "name": name,
                "datetime_utc": dt_utc.isoformat(),
                "datetime_local": transit_datetime_local,
                "tz": tz,
                "aspect_mode": mode,
            },
            "settings": settings,
            "natal": natal,
            "transit": {
                "meta": {
                    "datetime_utc": dt_utc.isoformat(),
                    "datetime_local": transit_datetime_local,
                    "tz": tz,
                },
                "planets": transit_planets,
                "aspects": transit_aspects,
            },
        }

        return TransitResult(payload)

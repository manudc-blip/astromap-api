from typing import Any, Optional
from pydantic import BaseModel, Field


class ThemeSettings(BaseModel):
    house_system: str = Field(default="Placidus")


class ThemeRequest(BaseModel):
    name: Optional[str] = Field(default="")
    datetime_local: str = Field(
        ...,
        description="Date/heure locale au format YYYY-MM-DD HH:MM",
        examples=["1879-03-14 11:30"],
    )
    latitude: float
    longitude: float
    tz: str = Field(
        ...,
        description='Fuseau horaire IANA ou offset, ex: "Europe/Paris" ou "+01:00"',
    )
    settings: ThemeSettings = Field(default_factory=ThemeSettings)


class ThemeResponse(BaseModel):
    data: dict[str, Any]


class CitySearchItem(BaseModel):
    display: str
    name: str
    lat: float
    lon: float
    tz: str


class HealthResponse(BaseModel):
    status: str

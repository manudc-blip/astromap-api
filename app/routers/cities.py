from fastapi import APIRouter, Query

from astromap.utils.cities import search_cities
from app.schemas import CitySearchItem

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/search", response_model=list[CitySearchItem])
def city_search(
    q: str = Query(..., min_length=1, description="Texte recherché"),
    lang: str = Query("fr", pattern="^(fr|en)$"),
    max_results: int = Query(10, ge=1, le=20),
) -> list[CitySearchItem]:
    results = search_cities(q, max_results=max_results, lang=lang)

    return [
        CitySearchItem(
            display=display,
            name=name,
            lat=lat,
            lon=lon,
            tz=tz,
        )
        for display, name, lat, lon, tz in results
    ]

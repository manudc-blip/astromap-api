import os
import re
import unicodedata

import psycopg
from psycopg.rows import dict_row


def _normalize_name(s: str) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'")
    s = re.sub(r"[\s\-_]+", " ", s)
    return s.strip()


def _get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL manquante")
    return database_url


def _run_query(sql: str, params: dict):
    with psycopg.connect(_get_database_url(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def search_cities(prefix, max_results=20, lang="en"):
    """
    Retourne une liste de tuples :
    (display, name, lat, lon, tz)
    """
    prefix_norm = _normalize_name(prefix)
    if not prefix_norm:
        return []

    display_col = (
        "COALESCE(c.display_fr, c.name_fr, c.name)"
        if lang == "fr"
        else "COALESCE(c.display_en, c.name_en, c.name)"
    )
    name_col = (
        "COALESCE(c.name_fr, c.name)"
        if lang == "fr"
        else "COALESCE(c.name_en, c.name)"
    )

    sql_prefix = f"""
        WITH ranked AS (
            SELECT
                c.geonameid AS geoname_id,
                {display_col} AS display_name,
                {name_col} AS city_name,
                c.lat,
                c.lon,
                c.tz,
                COALESCE(c.population, 0) AS population,
                CASE
                    WHEN c.search_text = %(q)s THEN 0
                    WHEN ca.alias_norm = %(q)s THEN 0
                    ELSE 1
                END AS rank,
                ROW_NUMBER() OVER (
                    PARTITION BY c.geonameid
                    ORDER BY
                        CASE
                            WHEN c.search_text = %(q)s THEN 0
                            WHEN ca.alias_norm = %(q)s THEN 0
                            ELSE 1
                        END,
                        CASE
                            WHEN ca.alias_norm IS NOT NULL AND ca.alias_norm LIKE %(prefix)s
                                THEN LENGTH(ca.alias_norm)
                            ELSE LENGTH(c.search_text)
                        END ASC,
                        COALESCE(c.population, 0) DESC,
                        {display_col} ASC
                ) AS rn
            FROM cities c
            LEFT JOIN city_aliases ca
                ON ca.geonameid = c.geonameid
            WHERE c.search_text LIKE %(prefix)s
               OR ca.alias_norm LIKE %(prefix)s
        )
        SELECT
            geoname_id,
            display_name,
            city_name,
            lat,
            lon,
            tz
        FROM ranked
        WHERE rn = 1
        ORDER BY rank ASC, population DESC, display_name ASC
        LIMIT %(limit)s
    """

    rows = _run_query(
        sql_prefix,
        {
            "q": prefix_norm,
            "prefix": f"{prefix_norm}%",
            "limit": max_results,
        },
    )

    if not rows and len(prefix_norm) >= 3:
        sql_contains = f"""
            WITH ranked AS (
                SELECT
                    c.geonameid AS geoname_id,
                    {display_col} AS display_name,
                    {name_col} AS city_name,
                    c.lat,
                    c.lon,
                    c.tz,
                    COALESCE(c.population, 0) AS population,
                    CASE
                        WHEN c.search_text = %(q)s THEN 0
                        WHEN ca.alias_norm = %(q)s THEN 0
                        ELSE 1
                    END AS rank,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.geonameid
                        ORDER BY
                            CASE
                                WHEN c.search_text = %(q)s THEN 0
                                WHEN ca.alias_norm = %(q)s THEN 0
                                ELSE 1
                            END,
                            COALESCE(c.population, 0) DESC,
                            {display_col} ASC
                    ) AS rn
                FROM cities c
                LEFT JOIN city_aliases ca
                    ON ca.geonameid = c.geonameid
                WHERE c.search_text LIKE %(contains)s
                   OR ca.alias_norm LIKE %(contains)s
            )
            SELECT
                geoname_id,
                display_name,
                city_name,
                lat,
                lon,
                tz
            FROM ranked
            WHERE rn = 1
            ORDER BY rank ASC, population DESC, display_name ASC
            LIMIT %(limit)s
        """

        rows = _run_query(
            sql_contains,
            {
                "q": prefix_norm,
                "contains": f"%{prefix_norm}%",
                "limit": max_results,
            },
        )

    return [
        (
            row["display_name"] or "",
            row["city_name"] or "",
            float(row["lat"]),
            float(row["lon"]),
            row["tz"] or "",
        )
        for row in rows
    ]


def find_city(name: str):
    """
    Retourne (lat, lon, tz) ou None
    """
    if "—" in name:
        name = name.split("—", 1)[0].strip()

    key = _normalize_name(name)
    if not key:
        return None

    sql = """
        SELECT
            c.lat,
            c.lon,
            c.tz,
            COALESCE(c.population, 0) AS population
        FROM cities c
        LEFT JOIN city_aliases ca
            ON ca.geonameid = c.geonameid
        WHERE c.search_text = %(q)s
           OR ca.alias_norm = %(q)s
        ORDER BY population DESC
        LIMIT 1
    """

    rows = _run_query(sql, {"q": key})
    if rows:
        row = rows[0]
        return float(row["lat"]), float(row["lon"]), row["tz"] or ""

    res = search_cities(key, max_results=1, lang="en")
    if res:
        _, _, lat, lon, tz = res[0]
        return lat, lon, tz

    return None

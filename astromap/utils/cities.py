import sqlite3
import unicodedata
import re
from pathlib import Path

_DB_CONN = None


def _normalize_name(s: str) -> str:
    """
    Cohérent avec build_cities_db_sqlite.py
    """
    if not s:
        return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'")
    s = re.sub(r"[\s\-_]+", " ", s)
    return s.strip()


def _get_db_path() -> Path:
    base_dir = Path(__file__).resolve().parent.parent  # .../astromap
    return base_dir / "data" / "cities.db"


def _get_conn() -> sqlite3.Connection:
    global _DB_CONN
    if _DB_CONN is not None:
        return _DB_CONN

    db_path = _get_db_path()
    if not db_path.exists():
        raise FileNotFoundError(
            f"cities.db introuvable : {db_path}. "
            "Lance build_cities_db_sqlite.py pour le générer."
        )

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    _DB_CONN = conn
    return _DB_CONN


def search_cities(prefix, max_results=20, lang="en"):
    """
    Retourne une liste de tuples :
    (display, name, lat, lon, tz)
    """
    prefix_norm = _normalize_name(prefix)
    if not prefix_norm:
        return []

    conn = _get_conn()
    cur = conn.cursor()

    display_col = "display_fr" if lang == "fr" else "display_en"
    name_col = "name_fr" if lang == "fr" else "name_en"

    # On récupère plus large puis on déduplique par geoname_id
    sql = f"""
        SELECT
            geoname_id,
            {display_col} AS display_name,
            {name_col} AS city_name,
            lat, lon, tz,
            key_norm
        FROM cities
        WHERE key_norm LIKE ?
        ORDER BY
            CASE WHEN key_norm = ? THEN 0 ELSE 1 END,
            LENGTH(key_norm) ASC,
            display_name ASC
        LIMIT ?
    """

    rows = cur.execute(sql, (f"{prefix_norm}%", prefix_norm, max_results * 8)).fetchall()

    results = []
    seen_ids = set()

    for row in rows:
        gid = row["geoname_id"]
        if gid in seen_ids:
            continue
        seen_ids.add(gid)

        results.append((
            row["display_name"] or "",
            row["city_name"] or "",
            float(row["lat"]),
            float(row["lon"]),
            row["tz"] or "",
        ))

        if len(results) >= max_results:
            break

    # fallback léger si rien trouvé : contient au lieu de préfixe
    if not results and len(prefix_norm) >= 3:
        sql2 = f"""
            SELECT
                geoname_id,
                {display_col} AS display_name,
                {name_col} AS city_name,
                lat, lon, tz,
                key_norm
            FROM cities
            WHERE key_norm LIKE ?
            ORDER BY
                LENGTH(key_norm) ASC,
                display_name ASC
            LIMIT ?
        """
        rows = cur.execute(sql2, (f"%{prefix_norm}%", max_results * 8)).fetchall()

        for row in rows:
            gid = row["geoname_id"]
            if gid in seen_ids:
                continue
            seen_ids.add(gid)

            results.append((
                row["display_name"] or "",
                row["city_name"] or "",
                float(row["lat"]),
                float(row["lon"]),
                row["tz"] or "",
            ))

            if len(results) >= max_results:
                break

    return results


def find_city(name: str):
    """
    Retourne (lat, lon, tz) ou None
    """
    if "—" in name:
        name = name.split("—", 1)[0].strip()

    key = _normalize_name(name)
    if not key:
        return None

    conn = _get_conn()
    cur = conn.cursor()

    row = cur.execute("""
        SELECT lat, lon, tz
        FROM cities
        WHERE key_norm = ?
        ORDER BY LENGTH(key_norm) ASC
        LIMIT 1
    """, (key,)).fetchone()

    if row:
        return float(row["lat"]), float(row["lon"]), row["tz"] or ""

    # fallback léger via search
    res = search_cities(key, max_results=1, lang="en")
    if res:
        _, _, lat, lon, tz = res[0]
        return lat, lon, tz

    return None

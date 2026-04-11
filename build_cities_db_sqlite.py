import sqlite3
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, Tuple, Optional


# ---------------------------------------------------------------------------
# Normalisation des noms
# ---------------------------------------------------------------------------

def normalize_name(s: str) -> str:
    """
    Normalise un nom de ville pour la recherche :
      - strip + lower
      - suppression des accents
      - remplacement espaces/tirets/underscores successifs par un espace
    """
    if not s:
        return ""
    s = s.strip().lower()

    s = "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )

    out = []
    last_sep = False
    for c in s:
        if c in " -_\t\r\n":
            if not last_sep:
                out.append(" ")
                last_sep = True
        else:
            out.append(c)
            last_sep = False

    return "".join(out).strip()


def pick_best_name(candidates, fallback: str) -> str:
    if not candidates:
        return fallback

    cleaned = [
        c.strip() for c in candidates
        if c and c.strip() and "," not in c and len(c.strip()) <= 60
    ]

    if not cleaned:
        cleaned = [c.strip() for c in candidates if c and c.strip()]

    return min(cleaned, key=lambda s: (len(s), s.lower()))


# ---------------------------------------------------------------------------
# Chargement GeoNames brut
# ---------------------------------------------------------------------------

def load_cities5000(src_path: Path) -> Dict[str, dict]:
    """
    Charge cities5000(.txt)
    Retourne { geonameid -> info }
    """
    cities_by_id: Dict[str, dict] = {}

    with src_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) < 18:
                continue

            geonameid = parts[0]
            name = parts[1]
            asciiname = parts[2]
            alternatenames = parts[3]
            lat = parts[4]
            lon = parts[5]
            feature_class = parts[6]
            feature_code = parts[7]
            country_code = parts[8]
            admin1_code = parts[10]
            timezone = parts[17]

            # Exclure subdivisions locales
            if feature_class == "P" and feature_code == "PPLX":
                continue

            try:
                lat_f = float(lat)
                lon_f = float(lon)
            except ValueError:
                continue

            cities_by_id[geonameid] = {
                "id": geonameid,
                "name": name,
                "asciiname": asciiname,
                "alt_names_raw": alternatenames,
                "lat": lat_f,
                "lon": lon_f,
                "tz": timezone,
                "country_code": country_code,
                "admin1_code": admin1_code,
                "feature_class": feature_class,
                "feature_code": feature_code,
            }

    return cities_by_id


def iter_alternate_names(src_path: Path) -> Iterable[Tuple[str, str, str]]:
    """
    Lit alternateNamesV2.txt / alternateNames.txt
    Rend (geonameid, isolanguage, alt_name)
    """
    with src_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")
            if len(parts) < 4:
                continue

            geonameid = parts[1]
            isolanguage = parts[2]
            alt_name = parts[3]

            if alt_name:
                yield geonameid, isolanguage, alt_name


def load_countries(countryinfo_path: Path) -> Dict[str, str]:
    countries = {}
    with countryinfo_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 5:
                continue
            cc = parts[0]
            name = parts[4]
            if cc and name:
                countries[cc] = name
    return countries


def load_admin1(admin1_path: Path) -> Dict[str, str]:
    admin1 = {}
    with admin1_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            key = parts[0]
            name = parts[1]
            if key and name:
                admin1[key] = name
    return admin1


LANGS_TO_KEEP = {
    "fr", "en", "de", "es", "it", "pt", "pl", "nl",
    "sv", "no", "da", "fi",
    "ru", "uk", "be",
    "cs", "sk", "hu",
    "ro", "bg", "el", "tr",
    "ar", "he",
    "zh", "ja", "ko",
    "und", "link", "",
}


# ---------------------------------------------------------------------------
# SQLite helpers
# ---------------------------------------------------------------------------

def create_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS cities")

    cur.execute("""
        CREATE TABLE cities (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            geoname_id TEXT NOT NULL,
            key_norm TEXT NOT NULL,
            name TEXT,
            name_fr TEXT,
            name_en TEXT,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            tz TEXT,
            country TEXT,
            region TEXT,
            display TEXT,
            display_fr TEXT,
            display_en TEXT,
            feature_class TEXT,
            feature_code TEXT
        )
    """)

    cur.execute("CREATE INDEX idx_cities_key_norm ON cities(key_norm)")
    cur.execute("CREATE INDEX idx_cities_geoname_id ON cities(geoname_id)")
    cur.execute("CREATE INDEX idx_cities_name_fr ON cities(name_fr)")
    cur.execute("CREATE INDEX idx_cities_name_en ON cities(name_en)")
    cur.execute("CREATE INDEX idx_cities_display_fr ON cities(display_fr)")
    cur.execute("CREATE INDEX idx_cities_display_en ON cities(display_en)")

    conn.commit()


def insert_rows(conn: sqlite3.Connection, rows: list[tuple]) -> None:
    conn.executemany("""
        INSERT INTO cities (
            geoname_id, key_norm, name, name_fr, name_en,
            lat, lon, tz, country, region,
            display, display_fr, display_en,
            feature_class, feature_code
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_cities_db_sqlite() -> None:
    root = Path(__file__).resolve().parent

    def find_existing(*names: str) -> Path:
        for name in names:
            p = root / name
            if p.exists():
                return p
        raise FileNotFoundError(f"Fichier introuvable parmi : {names}")

    countryinfo_path = find_existing("countryInfo.txt", "countryInfo")
    admin1_path = find_existing("admin1CodesASCII.txt", "admin1CodesASCII")
    cities_src = find_existing("cities5000.txt", "cities5000")
    alt_src = find_existing("alternateNamesV2.txt", "alternateNames.txt", "alternateNamesV2")

    countries = load_countries(countryinfo_path)
    admin1_map = load_admin1(admin1_path)

    print(f"Chargement de {cities_src} ...")
    cities_by_id = load_cities5000(cities_src)
    print(f"{len(cities_by_id)} villes chargées.")

    print(f"Lecture de {alt_src} ...")
    alt_best = {}
    preferred = {}  # {geonameid: {"fr": ..., "en": ...}}

    for geonameid, lang, alt_name in iter_alternate_names(alt_src):
        if geonameid not in cities_by_id:
            continue
        if lang not in ("fr", "en"):
            continue

        alt_best.setdefault(geonameid, {}).setdefault(lang, set()).add(alt_name)

        d = preferred.get(geonameid)
        if d is None:
            d = {"fr": None, "en": None}
            preferred[geonameid] = d

        cur = d[lang]
        if cur is None or (alt_name and len(alt_name) < len(cur)):
            d[lang] = alt_name

    dst_path = root / "astromap" / "data" / "cities.db"
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(dst_path)
    try:
        create_db(conn)

        batch = []
        seen_pairs = set()  # (key_norm, geonameid)
        total_inserted = 0

        def flush():
            nonlocal batch, total_inserted
            if batch:
                insert_rows(conn, batch)
                conn.commit()
                total_inserted += len(batch)
                batch = []

        for info in cities_by_id.values():
            gid = info["id"]
            cc = info.get("country_code", "") or ""
            a1 = info.get("admin1_code", "") or ""
            region = admin1_map.get(f"{cc}.{a1}", "")
            country = countries.get(cc, cc)

            best_fr = pick_best_name(
                alt_best.get(gid, {}).get("fr"),
                info["name"]
            )
            best_en = pick_best_name(
                alt_best.get(gid, {}).get("en"),
                info["name"]
            )

            display_fr = best_fr
            display_en = best_en
            if region and country:
                display_fr = f"{best_fr} — {region}, {country}"
                display_en = f"{best_en} — {region}, {country}"
            elif country:
                display_fr = f"{best_fr} — {country}"
                display_en = f"{best_en} — {country}"

            all_names = {info["name"], info["asciiname"]}
            if info["alt_names_raw"]:
                for alt in info["alt_names_raw"].split(","):
                    alt = alt.strip()
                    if alt:
                        all_names.add(alt)

            for geonameid, lang, alt_name in iter_alternate_names(alt_src):
                pass  # volontairement non utilisé ici

            # On repartit les aliases depuis alt_src serait trop coûteux ici,
            # donc on reconstruit une petite liste locale :
            # noms principaux + alternates embarqués
            local_aliases = set(all_names)

            # on ajoute aussi les meilleurs noms FR/EN
            if best_fr:
                local_aliases.add(best_fr)
            if best_en:
                local_aliases.add(best_en)

            for raw in local_aliases:
                key_norm = normalize_name(raw)
                if not key_norm:
                    continue

                pair = (key_norm, gid)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                batch.append((
                    gid,
                    key_norm,
                    info["name"],
                    best_fr,
                    best_en,
                    info["lat"],
                    info["lon"],
                    info["tz"],
                    country,
                    region,
                    display_en,
                    display_fr,
                    display_en,
                    info.get("feature_class", ""),
                    info.get("feature_code", ""),
                ))

                if len(batch) >= 10000:
                    flush()

        # deuxième passe : vrais alternateNames complets
        print("Insertion des alias supplémentaires depuis alternateNames ...")
        for geonameid, lang, alt_name in iter_alternate_names(alt_src):
            if lang not in LANGS_TO_KEEP:
                continue

            info = cities_by_id.get(geonameid)
            if info is None:
                continue

            gid = info["id"]
            key_norm = normalize_name(alt_name)
            if not key_norm:
                continue

            pair = (key_norm, gid)
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            cc = info.get("country_code", "") or ""
            a1 = info.get("admin1_code", "") or ""
            region = admin1_map.get(f"{cc}.{a1}", "")
            country = countries.get(cc, cc)

            best_fr = pick_best_name(
                alt_best.get(gid, {}).get("fr"),
                info["name"]
            )
            best_en = pick_best_name(
                alt_best.get(gid, {}).get("en"),
                info["name"]
            )

            display_fr = best_fr
            display_en = best_en
            if region and country:
                display_fr = f"{best_fr} — {region}, {country}"
                display_en = f"{best_en} — {region}, {country}"
            elif country:
                display_fr = f"{best_fr} — {country}"
                display_en = f"{best_en} — {country}"

            batch.append((
                gid,
                key_norm,
                info["name"],
                best_fr,
                best_en,
                info["lat"],
                info["lon"],
                info["tz"],
                country,
                region,
                display_en,
                display_fr,
                display_en,
                info.get("feature_class", ""),
                info.get("feature_code", ""),
            ))

            if len(batch) >= 10000:
                flush()

        flush()

        cur = conn.cursor()
        cur.execute("ANALYZE")
        conn.commit()

        print(f"{total_inserted} lignes écrites dans {dst_path}")

    finally:
        conn.close()


if __name__ == "__main__":
    build_cities_db_sqlite()

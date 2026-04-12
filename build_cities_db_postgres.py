from pathlib import Path
import os
import unicodedata
from typing import Dict, Iterable, Tuple

import psycopg


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

def normalize_name(s: str) -> str:
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
# Chargement GeoNames
# ---------------------------------------------------------------------------

def load_cities5000(src_path: Path) -> Dict[str, dict]:
    cities_by_id: Dict[str, dict] = {}

    with src_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) < 19:
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
            population = parts[14]
            timezone = parts[17]

            if feature_class == "P" and feature_code == "PPLX":
                continue

            try:
                lat_f = float(lat)
                lon_f = float(lon)
                population_i = int(population or 0)
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
                "population": population_i,
            }

    return cities_by_id


def iter_alternate_names(src_path: Path) -> Iterable[Tuple[str, str, str]]:
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


def build_cities_db_postgres() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL manquant")

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

    print(f"Chargement de {cities_src} ...")
    countries = load_countries(countryinfo_path)
    admin1_map = load_admin1(admin1_path)
    cities_by_id = load_cities5000(cities_src)
    print(f"{len(cities_by_id)} villes chargées.")

    print(f"Lecture de {alt_src} ...")
    alt_best = {}
    aliases_by_gid = {}

    for geonameid, lang, alt_name in iter_alternate_names(alt_src):
        if geonameid not in cities_by_id:
            continue

        aliases_by_gid.setdefault(geonameid, []).append((lang, alt_name))

        if lang not in ("fr", "en"):
            continue

        alt_best.setdefault(geonameid, {}).setdefault(lang, set()).add(alt_name)

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            print("Nettoyage des tables ...")
            cur.execute("TRUNCATE TABLE city_aliases RESTART IDENTITY CASCADE")
            cur.execute("TRUNCATE TABLE cities CASCADE")
            conn.commit()

            # ------------------------------------------------------------------
            # 1) Insert cities
            # ------------------------------------------------------------------
            print("Insertion des villes ...")
            city_batch = []

            for info in cities_by_id.values():
                gid = int(info["id"])
                cc = info.get("country_code", "") or ""
                a1 = info.get("admin1_code", "") or ""
                region = admin1_map.get(f"{cc}.{a1}", "")
                country = countries.get(cc, cc)

                best_fr = pick_best_name(
                    alt_best.get(info["id"], {}).get("fr"),
                    info["name"]
                )
                best_en = pick_best_name(
                    alt_best.get(info["id"], {}).get("en"),
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

                city_batch.append((
                    gid,
                    info["name"],
                    best_fr,
                    best_en,
                    cc,
                    country,
                    a1,
                    region,
                    info["lat"],
                    info["lon"],
                    info["tz"],
                    info.get("feature_class", ""),
                    info.get("feature_code", ""),
                    info.get("population", 0),
                    display_fr,
                    display_en,
                    normalize_name(info["name"]),
                ))

                if len(city_batch) >= 5000:
                    cur.executemany("""
                        INSERT INTO cities (
                            geonameid, name, name_fr, name_en,
                            country_code, country_name, admin1_code, region,
                            lat, lon, tz,
                            feature_class, feature_code, population,
                            display_fr, display_en, search_text
                        )
                        VALUES (
                            %s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s
                        )
                    """, city_batch)
                    conn.commit()
                    print(f"{len(city_batch)} villes insérées ...")
                    city_batch = []

            if city_batch:
                cur.executemany("""
                    INSERT INTO cities (
                        geonameid, name, name_fr, name_en,
                        country_code, country_name, admin1_code, region,
                        lat, lon, tz,
                        feature_class, feature_code, population,
                        display_fr, display_en, search_text
                    )
                    VALUES (
                        %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s
                    )
                """, city_batch)
                conn.commit()

            # ------------------------------------------------------------------
            # 2) Insert aliases
            # ------------------------------------------------------------------
            print("Insertion des alias ...")
            alias_batch = []
            seen_pairs = set()

            for info in cities_by_id.values():
                gid = int(info["id"])

                local_aliases = {info["name"], info["asciiname"]}
                if info["alt_names_raw"]:
                    for alt in info["alt_names_raw"].split(","):
                        alt = alt.strip()
                        if alt:
                            local_aliases.add(alt)

                best_fr = pick_best_name(
                    alt_best.get(info["id"], {}).get("fr"),
                    info["name"]
                )
                best_en = pick_best_name(
                    alt_best.get(info["id"], {}).get("en"),
                    info["name"]
                )

                if best_fr:
                    local_aliases.add(best_fr)
                if best_en:
                    local_aliases.add(best_en)

                for raw in local_aliases:
                    alias_norm = normalize_name(raw)
                    if not alias_norm:
                        continue
                    pair = (gid, alias_norm)
                    if pair in seen_pairs:
                        continue
                    seen_pairs.add(pair)

                    alias_batch.append((gid, raw, alias_norm, None))

                    if len(alias_batch) >= 10000:
                        cur.executemany("""
                            INSERT INTO city_aliases (
                                geonameid, alias, alias_norm, lang
                            )
                            VALUES (%s, %s, %s, %s)
                        """, alias_batch)
                        conn.commit()
                        print(f"{len(alias_batch)} alias insérés ...")
                        alias_batch = []

            for geonameid, lang, alt_name in iter_alternate_names(alt_src):
                if lang not in LANGS_TO_KEEP:
                    continue
                info = cities_by_id.get(geonameid)
                if info is None:
                    continue

                gid = int(info["id"])
                alias_norm = normalize_name(alt_name)
                if not alias_norm:
                    continue

                pair = (gid, alias_norm)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                alias_batch.append((gid, alt_name, alias_norm, lang or None))

                if len(alias_batch) >= 10000:
                    cur.executemany("""
                        INSERT INTO city_aliases (
                            geonameid, alias, alias_norm, lang
                        )
                        VALUES (%s, %s, %s, %s)
                    """, alias_batch)
                    conn.commit()
                    print(f"{len(alias_batch)} alias insérés ...")
                    alias_batch = []

            if alias_batch:
                cur.executemany("""
                    INSERT INTO city_aliases (
                        geonameid, alias, alias_norm, lang
                    )
                    VALUES (%s, %s, %s, %s)
                """, alias_batch)
                conn.commit()

            print("Import PostgreSQL terminé.")


if __name__ == "__main__":
    build_cities_db_postgres()

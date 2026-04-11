import difflib
import json
import unicodedata
import re
from pathlib import Path

_CITIES = None

# Index: liste d'entrées uniques
# entry = (primary_norm, keys_set, tokens_set, display_fr, display_en, name_fr, name_en, lat, lon, tz)
_CITY_INDEX = None

# Buckets: accélération (1 lettre / 2 lettres)
_CITY_BUCKETS_1 = None  # dict "w"  -> [entry, ...]
_CITY_BUCKETS_2 = None  # dict "wa" -> [entry, ...]

# Cache simple: (prefix_norm, max_results) -> results
_SEARCH_CACHE = {}
_SEARCH_CACHE_ORDER = []
_SEARCH_CACHE_MAX = 200

def _cache_get(prefix_norm: str, max_results: int, lang: str):
    return _SEARCH_CACHE.get((prefix_norm, max_results, lang))

def _cache_put(prefix_norm: str, max_results: int, lang: str, results):
    key = (prefix_norm, max_results, lang)

    if key in _SEARCH_CACHE:
        _SEARCH_CACHE[key] = results
        return

    _SEARCH_CACHE[key] = results
    _SEARCH_CACHE_ORDER.append(key)

    if len(_SEARCH_CACHE_ORDER) > _SEARCH_CACHE_MAX:
        old = _SEARCH_CACHE_ORDER.pop(0)
        _SEARCH_CACHE.pop(old, None)

def _normalize_name(s: str) -> str:
    """
    Doit être cohérent avec normalize_name() de build_cities_db.py.
    Permet de retrouver une ville quelle que soit la casse / accents / tirets.
    """
    if not s:
        return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'")
    s = re.sub(r"[\s\-_]+", " ", s)
    return s


def load_cities():
    """Charge le JSON des villes une seule fois (lazy)."""
    global _CITIES
    if _CITIES is not None:
        return _CITIES

    base_dir = Path(__file__).resolve().parent.parent  # .../astromap
    data_path = base_dir / "data" / "cities5000.json"

    if not data_path.exists():
        raise FileNotFoundError(
            f"cities5000.json introuvable : {data_path}. "
            "Lance build_cities_db.py pour le générer."
        )

    with data_path.open(encoding="utf-8") as f:
        _CITIES = json.load(f)

    # --- Build a fast index (unique by geonameid) but keeping ALL aliases for matching ---
    global _CITY_INDEX, _CITY_BUCKETS_1, _CITY_BUCKETS_2
    _CITY_INDEX = []
    _CITY_BUCKETS_1 = {}
    _CITY_BUCKETS_2 = {}

    # reset cache (base vient de changer)
    _SEARCH_CACHE.clear()
    _SEARCH_CACHE_ORDER.clear()

    # Regroupe toutes les clés (alias) par geonameid
    by_id = {}
    for k, info in _CITIES.items():
        gid = info.get("id")
        if not gid:
            continue

        rec = by_id.get(gid)
        if rec is None:
            # Champs multilingues (issus de build_cities_db.py)
            name_fr = info.get("name_fr") or info.get("name") or ""
            name_en = info.get("name_en") or info.get("name") or ""

            display_fr = info.get("display_fr") or info.get("display") or name_fr or name_en or ""
            display_en = info.get("display_en") or info.get("display") or name_en or name_fr or ""

            tz = info.get("tz")

            rec = {
                "name_fr": name_fr,
                "name_en": name_en,
                "display_fr": display_fr,
                "display_en": display_en,
                "lat": info["lat"],
                "lon": info["lon"],
                "tz": tz,
                "keys": set(),
                "tokens": set(),
            }
            by_id[gid] = rec

            for nm in (name_fr, name_en):
                norm = _normalize_name(nm)
                if norm:
                    rec["keys"].add(norm)
                    rec["tokens"].update(norm.split())

        # k est une clé (souvent déjà normalisée), on renormalise par sécurité
        kn = _normalize_name(k)
        if kn:
            rec["keys"].add(kn)
            for tok in kn.split():
                rec["tokens"].add(tok)

        # ajoute aussi le nom canonique
        nm = _normalize_name(info.get("name", "") or "")
        if nm:
            rec["keys"].add(nm)
            for tok in nm.split():
                rec["tokens"].add(tok)

        # ajoute aussi le display (utile si "Warsaw — Mazovia, Poland" a été indexé)
        dn = _normalize_name(info.get("display", "") or "")
        if dn:
            rec["keys"].add(dn)
            for tok in dn.split():
                rec["tokens"].add(tok)

        # ajoute aussi les variantes FR/EN (tolérance de saisie, affichage strict)
        nm_fr = _normalize_name(info.get("name_fr", "") or "")
        if nm_fr:
            rec["keys"].add(nm_fr)
            for tok in nm_fr.split():
                rec["tokens"].add(tok)

        nm_en = _normalize_name(info.get("name_en", "") or "")
        if nm_en:
            rec["keys"].add(nm_en)
            for tok in nm_en.split():
                rec["tokens"].add(tok)

        dn_fr = _normalize_name(info.get("display_fr", "") or "")
        if dn_fr:
            rec["keys"].add(dn_fr)
            for tok in dn_fr.split():
                rec["tokens"].add(tok)

        dn_en = _normalize_name(info.get("display_en", "") or "")
        if dn_en:
            rec["keys"].add(dn_en)
            for tok in dn_en.split():
                rec["tokens"].add(tok)

    # Fabrique l’index final + buckets
    for rec in by_id.values():
        keys = rec["keys"]
        tokens = rec["tokens"]
        if not keys:
            continue

        # Clé “primaire” pour scoring/fuzzy (la plus courte en général)
        primary_norm = min(keys, key=len)

        # Limite les checks startswith() à une petite liste (plus rapide que sur tout le set)
        keys_short = sorted(keys, key=len)[:30]

        entry = (
            primary_norm, keys, keys_short, tokens,
            rec["display_fr"], rec["display_en"],
            rec["name_fr"], rec["name_en"],
            rec["lat"], rec["lon"], rec["tz"]
        )

        _CITY_INDEX.append(entry)

        # Buckets premium (1 lettre / 2 lettres) basés sur primary + tokens
        b1_set = set()
        b2_set = set()

        if primary_norm:
            b1_set.add(primary_norm[:1])
            if len(primary_norm) >= 2:
                b2_set.add(primary_norm[:2])

        for tok in tokens:
            if tok:
                b1_set.add(tok[:1])
                if len(tok) >= 2:
                    b2_set.add(tok[:2])

        for b1 in b1_set:
            _CITY_BUCKETS_1.setdefault(b1, []).append(entry)

        for b2 in b2_set:
            _CITY_BUCKETS_2.setdefault(b2, []).append(entry)

    return _CITIES


def search_cities(prefix, max_results=20, lang="en"):

    """
    Retourne une liste de tuples (display, name, lat, lon, tz)

    Premium:
    - buckets 1/2 lettres (réduit drastiquement le scan)
    - match sur alias + tokens
    - fuzzy fallback (typos) si rien trouvé
    - cache LRU léger
    """
    prefix_norm = _normalize_name(prefix)
    if not prefix_norm:
        return []

    load_cities()  # s'assure que _CITY_INDEX/_CITY_BUCKETS sont prêts

    cached = _cache_get(prefix_norm, max_results, lang)
    if cached is not None:
        return cached

    # Choix du bucket: 2 lettres si possible, sinon 1 lettre
    if len(prefix_norm) >= 2:
        base = _CITY_BUCKETS_2.get(prefix_norm[:2], _CITY_INDEX)
    else:
        base = _CITY_BUCKETS_1.get(prefix_norm[:1], _CITY_INDEX)

    candidates = []
    seen = set()

    # Limites pour garder Tkinter fluide
    scan_limit = 2500 if len(prefix_norm) == 1 else 20000
    soft_cap = max_results * (30 if len(prefix_norm) == 1 else 60)

    for i, (primary_norm, keys, keys_short, tokens, disp_fr, disp_en, name_fr, name_en, la, lo, tz) in enumerate(base):
        if i >= scan_limit:
            break

        display = disp_fr if lang == "fr" else disp_en
        name = name_fr if lang == "fr" else name_en

        # Match préfixe: sur n'importe quel alias OU token
        # STRICT: uniquement si un alias complet commence par le préfixe
        if not (primary_norm.startswith(prefix_norm) or any(k.startswith(prefix_norm) for k in keys_short)):
            continue

        key = (la, lo, tz)
        if key in seen:
            continue
        seen.add(key)

        score = 0

        # Exact match (très fort)
        if prefix_norm in keys:
            score += 2000
        # Match sur token entier
        elif prefix_norm in tokens:
            score += 600
        # Match sur primary
        elif primary_norm.startswith(prefix_norm):
            score += 300

        # Bonus TZ (optionnel)
        if tz == "Europe/Paris":
            score += 120

        # Plus court = souvent meilleur
        score -= len(display)

        candidates.append((score, display, name, la, lo, tz))

        # arrêt anticipé
        if len(candidates) >= soft_cap:
            break

    # Fuzzy fallback (typos) seulement si rien trouvé et si assez de lettres
    if not candidates and len(prefix_norm) >= 4:
        # On fait le fuzzy sur les primary_norm du bucket (rapide)
        primaries = [e[0] for e in base[:8000]]
        close = difflib.get_close_matches(prefix_norm, primaries, n=max_results, cutoff=0.78)

        if close:
            quick = {}
            for (pn, keys, keys_short, tokens, disp_fr, disp_en, name_fr, name_en, la, lo, tz) in base[:8000]:
                if pn not in quick:
                    display = disp_fr if lang == "fr" else disp_en
                    name = name_fr if lang == "fr" else name_en
                    quick[pn] = (display, name, la, lo, tz)

            for cn in close:
                if cn in quick:
                    display, name, la, lo, tz = quick[cn]
                    key = (la, lo, tz)
                    if key in seen:
                        continue
                    seen.add(key)
                    candidates.append((250, display, name, la, lo, tz))

    candidates.sort(key=lambda x: x[0], reverse=True)
    results = [(d, n, la, lo, tz) for _, d, n, la, lo, tz in candidates[:max_results]]

    _cache_put(prefix_norm, max_results, lang, results)
    return results


def find_city(name: str):
    """Retourne (lat, lon, tz) pour une ville ou None si introuvable."""
    if "—" in name:
        name = name.split("—", 1)[0].strip()

    key = _normalize_name(name)
    if not key:
        return None

    cities = load_cities()

    # 1) tentative de clé exacte
    info = cities.get(key)
    if info is not None:
        return info["lat"], info["lon"], info["tz"]

    # 2) fallback rapide : réutilise le moteur (buckets + scan_limit + cache)
    res = search_cities(key, max_results=1, lang="en")
    if res:
        _, _, la, lo, tz = res[0]
        return la, lo, tz

    # Rien trouvé
    return None

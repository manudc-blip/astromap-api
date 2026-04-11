# astromap/utils/i18n.py

_current_lang = "fr"

# Dictionnaire des traductions.
# Les *clés* sont les chaînes utilisées dans le code (en anglais).
# Pour l'anglais on renvoie simplement la clé.
_TRANSLATIONS = {
    "fr": {
        "Name (optional)": "Nom (facultatif)",
        "Search DN": "Rechercher une DN",
        "Date (local) DD/MM/YYYY": "Date (locale) JJ/MM/AAAA",
        "Time (local) HH:MM": "Heure (locale) HH:MM",
        "Time reference": "Référence heure",
        "Time (UTC) HH:MM": "Heure (TU) HH:MM",
        "Time (local) HH:MM": "Heure (locale) HH:MM",
        "City (search)": "Ville (recherche)",
        "City hint": "Saisie assistée",
        "Latitude, Longitude (deg)": "Latitude, Longitude (°)",
        "Time zone (e.g., Europe/Paris, or +01:00)":
            "Fuseau horaire (ex. Europe/Paris ou +01:00)",
        "Language": "Langue",
        "Compute": "Calculer",
        "Export…": "Exporter…",
        "Export": "Exporter",
        "Cancel": "Annuler",
        "What do you want to export?": "Que voulez-vous exporter ?",
        "PNG image": "Image PNG",
        "SVG image": "Image SVG",
        "JSON data": "Données JSON",
        "Ecliptic": "Écliptique",
        "Domitude": "Domitude",
        "RET / HP": "RET / HP",
        "Transits": "Transits",
        "Aspects": "Aspects",
        "Interpretation": "Interprétation",
        "City": "Ville",
        "City not found in local database. Please enter coordinates manually.":
            "Ville introuvable dans la base locale. Veuillez entrer les "
            "coordonnées manuellement.",
        "Please fill in date and time completely.":
            "Veuillez compléter la date et l'heure.",
        "Invalid date or time.": "Date ou heure invalide.",
        "Details": "Détails",
        "Aspects": "Aspects",
        "Ephemeris": "Éphémérides",
        "Click a planet": "Cliquez sur une planète",
        "Copy": "Copier",
        "Copied": "Copié !",
        # --- Sidebar section headers ---
        "Identification": "Identification",
        "Date & time": "Date & heure",
        "Location": "Localisation",
        "Options": "Options",
        "Actions": "Actions",
    }
}


def set_language(lang: str):
    """Change la langue courante ('fr' ou 'en')."""
    global _current_lang
    # On ne gère que fr/en, tout autre valeur = en (clé brute)
    if lang not in ("fr", "en"):
        lang = "en"
    _current_lang = lang


def get_language() -> str:
    return _current_lang


def t(key: str) -> str:
    """
    Traduit une clé en fonction de la langue courante.

    - Si langue = 'fr' et une traduction existe, on la renvoie.
    - Sinon on renvoie la clé elle-même (comportement anglais).
    """
    if _current_lang == "fr":
        return _TRANSLATIONS["fr"].get(key, key)
    else:
        # anglais -> on renvoie la clé telle quelle
        return key

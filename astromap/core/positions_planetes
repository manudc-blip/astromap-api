# astromap/core/positions_planetes.py

from __future__ import annotations
import math

# --- Seuils canoniques en degrés (repris de GéoAstro) ---
DECL_T1 = 11 + 48/60      # 11.8°
DECL_T2 = 20 + 16/60      # 20.266666...
DECL_T3 = 23 + 45/60      # 23.75°

def sign_from_declination(decl_deg: float, lambda_deg: float) -> str:
    """
    Affecte un 'Signe' selon (δ, branche géométrique du cycle via λ), indépendant de la rétro.

    Règle conditionaliste :
      - Nord montant  : Bélier (0..T1), Taureau (T1..T2), Gémeaux (T2..T3)
      - Nord descendant: Vierge (T1..0), Lion (T2..T1), Cancer (T3..T2)
      - Sud descendant : Balance (0..-T1), Scorpion (-T1..-T2), Sagittaire (-T2..-T3)
      - Sud montant   : Poissons (-T1..0), Verseau (-T2..-T1), Capricorne (-T3..-T2)

    Le sens 'montant/descendant' est déterminé par la branche δ(λ) avec λ supposé croissant
    (mouvement direct) : dir_up := sign(cos λ).
    Aux tournants (cos λ ≈ 0), on force: Nord → descendant ; Sud → montant.
    À δ = 0 pile, on force: dir_up ? Bélier : Balance.
    """
    # Branche géométrique via λ (en radians)
    lam = math.radians(lambda_deg % 360.0)
    c = math.cos(lam)
    eps = 1e-12

    if   c >  eps:
        dir_up = True        # δ augmente le long de λ
    elif c < -eps:
        dir_up = False       # δ diminue le long de λ
    else:
        # Aux solstices (cos λ ≈ 0) : tournant
        # Nord -> descend ; Sud -> monte
        dir_up = (decl_deg < 0)

    # Cas exact à l'équateur : tranche sur la branche
    if abs(decl_deg) < 1e-12:
        return "Bélier" if dir_up else "Balance"

    north = (decl_deg > 0.0)
    d = abs(decl_deg)

    # Bande 0: [0..T1[  |  Bande 1: [T1..T2[  |  Bande 2: [T2..∞[
    if d < DECL_T1:
        band = 0
    elif d < DECL_T2:
        band = 1
    else:
        band = 2  # inclut aussi au-delà de T3 (Lune en grande déclinaison)

    if north:
        if dir_up:         # Nord montant
            return ("Bélier", "Taureau", "Gémeaux")[band]
        else:              # Nord descendant
            return ("Vierge", "Lion", "Cancer")[band]
    else:
        if dir_up:         # Sud montant
            return ("Poissons", "Verseau", "Capricorne")[band]
        else:              # Sud descendant
            return ("Balance", "Scorpion", "Sagittaire")[band]

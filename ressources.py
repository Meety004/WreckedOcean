import math

def calc_distance(x1, y1, x2, y2):
    # fonction pour calculer une distance
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

liste_benedictions = [
    "Bénédiction Dash", 
    "Bénédiction Santé",
    "Bénédiction d'aura", 
    "Bénédiciton de rage",
    "Bénédiction GodMode", 
    "Bénédiction Projectile"
        ]

liste_malus = [
    "Canons Rouillés",
    "Voile Trouée",
    "Coque Trouée"
        ]

listeCanons = [
    "+1 Canon",
    "Canon en bronze",
    "+2 Canons", 
    "Canon en argent", 
    "Canon Ballistique",
    "+3 Canons", 
    "Canon en or", 
    "Canon à tirs doubles",
    "+4 Canons", 
    "Canon légendaire"
        ]

listeCoques = [
    "Coque épicéa",
    "Coque chêne",
    "Coque en bouleau", 
    "Coque en chêne massif",
    "Coque en bois magique",
    "Coque légendaire"
        ]

listeVoiles = [
    "Voile en toile de jute",
    "Voile Latine",
    "Voile Enchantée", 
    "Voile légendaire"
        ]

CoqueCommune = ""
CoqueRare = ""
CoqueMythique = ""
CoqueLegendaire = ""

VoileCommune = ""
VoileRare = ""
VoileMythique = ""
VoileLegendaire = ""

CanonCommune = ""
CanonRare = ""
CanonMythique = ""
CanonLegendaire = ""
import math, pygame

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
    "Canon de base",
    "+1 Canon",
    "Canon en bronze",
    "+2 Canons", 
    "Canon en argent", 
    "Canon ballistique",
    "+3 Canons", 
    "Canon en or", 
    "Canon à tirs doubles",
    "+4 Canons", 
    "Canon légendaire"
        ]

listeCoques = [
    "Coque de base",
    "Coque épicéa",
    "Coque chêne",
    "Coque en bouleau", 
    "Coque en chêne massif",
    "Coque en bois magique",
    "Coque légendaire"
        ]

listeVoiles = [
    "Voile de base",
    "Voile en toile de jute",
    "Voile latine",
    "Voile enchantée", 
    "Voile légendaire"
        ]

listeEquipementStart = [
    "Canons de base",
    "Voile de base",
    "Coque de base"
]

CoqueCommun = "images/Icons/Coques/coque_commun.png"
CoqueRare = "images/Icons/Coques/coque_rare.png"
CoqueMythique = "images/Icons/Coques/coque_mythique.png"
CoqueLegendaire = "images/Icons/Coques/coque_legendaire.png"

VoileCommun = "images/Icons/Voiles/voile_commun.png"
VoileRare = "images/Icons/Voiles/voile_rare.png"
VoileMythique = "images/Icons/Voiles/voile_mythique.png"
VoileLegendaire = "images/Icons/Voiles/voile_legendaire.png"

CanonCommun = "images/Icons/Canons/canon_commun.png"
CanonRare = "images/Icons/Canons/canon_rare.png"
CanonMythique = "images/Icons/Canons/canon_mythique.png"
CanonLegendaire = "images/Icons/Canons/canon_legendaire.png"

VoileMalus = "images/Icons/Voiles/voile_trouee.png"
CanonMalus = "images/Icons/Canons/canon_rouille.png"
CoqueMalus = "images/Icons/Coques/coque_trouee.png"

BeneAura = "images/Icons/Benedictions/bene_aura.png"
BeneDash = "images/Icons/Benedictions/bene_dash.png"
BeneGodMode = "images/Icons/Benedictions/bene_godmode.png"
BeneProjectile = "images/Icons/Benedictions/bene_projectile.png"
BeneRage = "images/Icons/Benedictions/bene_rage.png"
BeneSante = "images/Icons/Benedictions/bene_sante.png"

keyBindList =  [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_RIGHT
]

keyBindCursedList =  [
    pygame.K_DOWN,
    pygame.K_RIGHT,
    pygame.K_LEFT
]

dictItemsBuff = {
    'Canons Rouillés': "Vitesse projectiles -15%",
    'Voile Trouée': "Vitesse Max -50%",
    'Coque Trouée': "Inverse les commandes",
    'Canon de base': "Aucun bonus",
    'Voile de base': "Aucun bonus",
    'Coque de base': "Aucun bonus",
    '+1 Canon': "Ajoute un canon à l'avant",
    'Canon en bronze': "Dégâts +20%",
    '+2 Canons': "Ajoute un canon à l'avant et à l'arrière",
    'Canon en argent': "Dégâts +33% | Vitesse projectiles +5%",
    'Canon ballistique': "Les projectiles vont deux fois plus loin",
    '+3 Canons': "Ajoute un canon à à l'arrière et deux en diagonale",
    'Canon en or': "Dégâts +66% | Vitesse projectiles +10% | Cadence +40%",
    'Canon à tirs doubles': "Tire un deuxième projectile à chaque tir",
    '+4 Canons': "Ajoute quatre canons",
    'Canon légendaire': "Dégâts +133% | Vitesse projectiles +15% |\n Cadence +40%",
    'Coque épicéa': "PV Max +10",
    'Coque chêne': "Vitesse Max +10%",
    'Coque en bouleau': "PV Max +10 | Vitesse Max +5%",
    'Coque en chêne massif': "PV Max +75",
    'Coque en bois magique': "PV Max +50 | Vitesse Max +20% |\n Chance d'esquive",
    'Coque légendaire': "PV Max +60 | Vitesse Max +30%",
    'Voile en toile de jute': "Vitesse Max +5%",
    'Voile latine': "Vitesse Max +10%",
    'Voile enchantée': "Vitesse Max +25% | Maniabilité +2%",
    'Voile légendaire': "Vitesse Max +30% | Maniabilité +5%"
}

fontPixel = "Fonts/pixel-font.otf"
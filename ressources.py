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
    '+1 Canon': "Ajoute un canon à l'avant",
    'Canon en bronze': "Dégâts +20%",
    '+2 Canons': "Ajoute un canon à l'avant et à l'arrière",
    'Canon en argent': "Dégâts +33% \nVitesse projectile +5%",
    'Canon Ballistique': "Les projectiles vont deux fois plus loin",
    '+3 Canons': "Ajoute un canon à l'avant, à l'arrière et dans la diagonale avant-droite",
    'Canon en or': "Dégâts +66% \nVitesse projectile +10% \nCadence +10%",
    'Canon à tirs doubles': "Tire un deuxième projectile à chaque tir",
    '+4 Canons': "Ajoute un canon à l'avant, à l'arrière et deux en diagonale devant",
    'Canon Légendaire': "Dégâts +133% \nVitesse projectile +15% \nCadence +10%",
    'Coque épicéa': "PV Max +10",
    'Coque chêne': "Vitesse Max +10%",
    'Coque en bouleau': "PV Max +10\nVitesse Max +5%",
    'Coque en chêne massif': "PV Max +75",
    'Coque en bois magique': "PV Max +50\nVitesse Max +20%\n20% de chance d'esquiver les projectiles",
    'Coque légendaire': "PV Max +60\nVitesse Max +30%",
    'Voile en toile de jute': "Vitesse Max +5%",
    'Voile Latine': "Vitesse Max +10%",
    'Voile Enchantée': "Vitesse Max +25% \nManiabilité +2%",
    'Voile légendaire': "Vitesse Max +30% \nManiabilité +5%"
}
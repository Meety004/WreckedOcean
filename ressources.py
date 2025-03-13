import math, pygame

def calc_distance(x1, y1, x2, y2):
    # fonction pour calculer une distance
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def valeur_equipement(objet):
    if objet in listeCanons:
        i = 0
        while i<2:
            if objet == listeCanons[i]:
                return 1
            i+=1
        while i<5:
            if objet == listeCanons[i]:
                return 2
            i+=1
        while i<8:
            if objet == listeCanons[i]:
                return 3
            i+=1
        while i<10:
            if objet == listeCanons[i]:
                return 4
            i+=1

    elif objet in listeCoques:
        i = 0
        while i<2:
            if objet == listeCoques[i]:
                return 1
            i+=1
        while i<4:
            if objet == listeCoques[i]:
                return 2
            i+=1
        while i<5:
            if objet == listeCoques[i]:
                return 3
            i+=1
        while i<6:
            if objet == listeCoques[i]:
                return 4
            i+=1

    elif objet in listeVoiles:
        i = 0
        while i<1:
            if objet == listeVoiles[i]:
                return 1
            i+=1
        while i<2:
            if objet == listeVoiles[i]:
                return 2
            i+=1
        while i<3:
            if objet == listeVoiles[i]:
                return 3
            i+=1
        while i<4:
            if objet == listeVoiles[i]:
                return 4
            i+=1

    elif objet in liste_benedictions:
        i = 0
        while i<2:
            if objet == liste_benedictions[i]:
                return 2
            i+=1
        while i<4:
            if objet == liste_benedictions[i]:
                return 3
            i+=1
        while i<6:
            if objet == liste_benedictions[i]:
                return 4
            i+=1

    elif objet in listeEquipementStart:
        return 0
    
    else:
        return -1

def comparaison_valeur_equipement_ile(ile, equipement):
    val_equip = (valeur_equipement(equipement['canons'])+valeur_equipement(equipement['voile'])+valeur_equipement(equipement['coque']))/3
    if ile.type == 'commun':
        val_ile = 1
    elif ile.type == 'rare':
        val_ile = 2
    elif ile.type == 'mythique':
        val_ile = 3
    else:
        val_ile = 4
    
    if val_equip<val_ile:
        return True
    else:
        return False

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
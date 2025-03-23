import math, pygame, os

def calc_distance(x1, y1, x2, y2):
    # fonction pour calculer une distance
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Timer:
    def __init__(self, duree_secondes):
        self.duree_secondes = duree_secondes
        self.temps_initial = pygame.time.get_ticks() / 1000  # Convertir en secondes

    def elapse(self):
        self.temps_actuel = pygame.time.get_ticks() / 1000  # Convertir en secondes

    def timer_ended(self):
        self.elapse()
        if self.temps_actuel - self.temps_initial >= self.duree_secondes:
            return True
        else:
            return False

    def reset(self):
        self.temps_initial = pygame.time.get_ticks() / 1000  # Convertir en secondes

    def timer_ended_special(self, duree):
        self.elapse()
        if self.temps_actuel - self.temps_initial >= duree:
            return True
        else:
            return False

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
    "Bénédiction de rage",
    "Bénédiction GodMode", 
    "Bénédiction Projectiles"
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

CoqueCommun = os.path.join("data",'images', 'Icons', 'Coques', 'coque_commun.png')
CoqueRare = os.path.join("data",'images', 'Icons', 'Coques', 'coque_rare.png') 
CoqueMythique = os.path.join("data",'images', 'Icons', 'Coques', 'coque_mythique.png')
CoqueLegendaire = os.path.join("data",'images', 'Icons', 'Coques', 'coque_legendaire.png')

VoileCommun = os.path.join("data",'images', 'Icons', 'Voiles', 'voile_commun.png')
VoileRare = os.path.join("data",'images', 'Icons', 'Voiles', 'voile_rare.png')
VoileMythique = os.path.join("data",'images', 'Icons', 'Voiles', 'voile_mythique.png')
VoileLegendaire = os.path.join("data",'images', 'Icons', 'Voiles', 'voile_legendaire.png')

CanonCommun = os.path.join("data",'images', 'Icons', 'Canons', 'canon_commun.png')
CanonRare = os.path.join("data",'images', 'Icons', 'Canons', 'canon_rare.png')
CanonMythique = os.path.join("data",'images', 'Icons', 'Canons', 'canon_mythique.png')
CanonLegendaire = os.path.join("data",'images', 'Icons', 'Canons', 'canon_legendaire.png')

VoileMalus = os.path.join("data",'images', 'Icons', 'Voiles', 'voile_trouee.png')
CanonMalus = os.path.join("data",'images', 'Icons', 'Canons', 'canon_rouille.png')
CoqueMalus = os.path.join("data",'images', 'Icons', 'Coques', 'coque_trouee.png')

BeneAura = os.path.join("data",'images', 'Icons', 'Benedictions', 'bene_aura.png')
BeneDash = os.path.join("data",'images', 'Icons', 'Benedictions', 'bene_dash.png')
BeneGodMode = os.path.join("data",'images', 'Icons', 'Benedictions', 'bene_godmode.png')
BeneProjectiles = os.path.join("data",'images', 'Icons', 'Benedictions', 'bene_projectiles.png')
BeneRage = os.path.join("data",'images', 'Icons', 'Benedictions', 'bene_rage.png')
BeneSante = os.path.join("data",'images', 'Icons', 'Benedictions', 'bene_sante.png')

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
    'Canons de base': "Aucun bonus",
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
    'Coque en chêne massif': "PV Max +75 | Vitesse Max -15%",
    'Coque en bois magique': "PV Max +50 | Vitesse Max +20% |\n Chance d'esquive",
    'Coque légendaire': "PV Max +60 | Vitesse Max +30%",
    'Voile en toile de jute': "Vitesse Max +5%",
    'Voile latine': "Vitesse Max +10%",
    'Voile enchantée': "Vitesse Max +25% | Maniabilité +2%",
    'Voile légendaire': "Vitesse Max +30% | Maniabilité +5%"
}

dictBenedictionsBuff = {
    "Bénédiction Dash": "Vous permet de faire une forte accélération",
    "Bénédiction Santé": "Ajoute 50% de votre PV max",
    "Bénédiction d'aura": "Crée une aura qui fait des dégâts aux ennemis proches",
    "Bénédiction de rage": "Augmente les dégâts et la vitesse de 50%, réduit les PV à 20",
    "Bénédiction GodMode": "Vous rend invincible",
    "Bénédiction Projectiles": "Envoie une multitude de projectiles autour de vous"
}

fontPixel = os.path.join("data", 'Fonts', 'pixel-font.otf')
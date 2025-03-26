# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM

#importation des modules
import math, pygame, os

def calc_distance(x1, y1, x2, y2):
    """ fonction pour calculer une distance 
    Prend en argument les positions x et y des deux objets """
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Timer:
    def __init__(self, duree_secondes):
        """
        Constructeur de timer
        Prend en argument la durée
        """
        self.duree_secondes = duree_secondes
        self.temps_initial = pygame.time.get_ticks() / 1000  # Convertir en secondes

    def elapse(self):
        """ Actualise le temps actuel """
        self.temps_actuel = pygame.time.get_ticks() / 1000  # Convertir en secondes

    def timer_ended(self):
        """ Revoie True si la bénédiction en utilisation peut toujours être utilisée, sinon False """
        self.elapse()
        if self.temps_actuel - self.temps_initial >= self.duree_secondes:
            return True
        else:
            return False

    def reset(self):
        """ Réinitialise le temps initial """
        self.temps_initial = pygame.time.get_ticks() / 1000  # Convertir en secondes

    def timer_ended_special(self, duree):
        """ Revoie True si la bénédiction en utilisation peut toujours être utilisée, sinon False. Dans les cas où la durée d'utilisation est différente"""
        self.elapse()
        if self.temps_actuel - self.temps_initial >= duree:
            return True
        else:
            return False
        
    def getTime(self):
        """ Renvoie le temps actuel """
        self.elapse()
        return self.temps_actuel

def valeur_equipement(objet):
    """ Revoie la valeur d'un équipement en fonction de sa rareté
    Argument : objet(équipement étudié)"""
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
    
    elif objet is None:
        return 1
    
    else:
        return -1

def comparaison_valeur_equipement_ile(ile, equipement, benedictions):
    """ Compare la valeur potentielle d'un équipement sur une île à la valeur des équipements déjà portés
    Prend en argument l'île et les équipement et bénédictions du navire"""
    val_equip = (valeur_equipement(equipement['canons'])+valeur_equipement(equipement['voile'])+valeur_equipement(equipement['coque'])+valeur_equipement(benedictions[0])+valeur_equipement(benedictions[1]))/5
    if ile.type == 'commun':
        val_ile = 1
    elif ile.type == 'rare':
        val_ile = 2
    elif ile.type == 'mythique':
        val_ile = 3
    else:
        val_ile = 4
    
    if val_equip<val_ile:#renvoie True si 
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

CoqueCommun = os.path.join("data",'images', 'icons', 'Coques', 'coque_commun.png')
CoqueRare = os.path.join("data",'images', 'icons', 'Coques', 'coque_rare.png') 
CoqueMythique = os.path.join("data",'images', 'icons', 'Coques', 'coque_mythique.png')
CoqueLegendaire = os.path.join("data",'images', 'icons', 'Coques', 'coque_legendaire.png')

VoileCommun = os.path.join("data",'images', 'icons', 'Voiles', 'voile_commun.png')
VoileRare = os.path.join("data",'images', 'icons', 'Voiles', 'voile_rare.png')
VoileMythique = os.path.join("data",'images', 'icons', 'Voiles', 'voile_mythique.png')
VoileLegendaire = os.path.join("data",'images', 'icons', 'Voiles', 'voile_legendaire.png')

CanonCommun = os.path.join("data",'images', 'icons', 'Canons', 'canon_commun.png')
CanonRare = os.path.join("data",'images', 'icons', 'Canons', 'canon_rare.png')
CanonMythique = os.path.join("data",'images', 'icons', 'Canons', 'canon_mythique.png')
CanonLegendaire = os.path.join("data",'images', 'icons', 'Canons', 'canon_legendaire.png')

VoileMalus = os.path.join("data",'images', 'icons', 'Voiles', 'voile_trouee.png')
CanonMalus = os.path.join("data",'images', 'icons', 'Canons', 'canon_rouille.png')
CoqueMalus = os.path.join("data",'images', 'icons', 'Coques', 'coque_trouee.png')

BeneAura = os.path.join("data",'images', 'icons', 'Benedictions', 'bene_aura.png')
BeneDash = os.path.join("data",'images', 'icons', 'Benedictions', 'bene_dash.png')
BeneGodMode = os.path.join("data",'images', 'icons', 'Benedictions', 'bene_godmode.png')
BeneProjectiles = os.path.join("data",'images', 'icons', 'Benedictions', 'bene_projectiles.png')
BeneRage = os.path.join("data",'images', 'icons', 'Benedictions', 'bene_rage.png')
BeneSante = os.path.join("data",'images', 'icons', 'Benedictions', 'bene_sante.png')

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
    'Canons Rouillés': "Vitesse projectiles -25%",
    'Voile Trouée': "Vitesse Max -25%",
    'Coque Trouée': "Inverse les commandes",
    'Canons de base': "Aucun bonus",
    'Voile de base': "Aucun bonus",
    'Coque de base': "Aucun bonus",
    '+1 Canon': "Ajoute un canon à l'avant",
    'Canon en bronze': "Dégats +20%",
    '+2 Canons': "Ajoute un canon à l'avant et à l'arrière",
    'Canon en argent': "Dégats +33% | Vitesse projectiles +5%",
    'Canon ballistique': "Les projectiles vont deux fois plus loin",
    '+3 Canons': "Ajoute un canon à à l'arrière et deux en diagonale",
    'Canon en or': "Dégats +66% | Vitesse projectiles +10% | Cadence +40%",
    'Canon à tirs doubles': "Tire un deuxième projectile à chaque tir",
    '+4 Canons': "Ajoute quatre canons",
    'Canon légendaire': "Dégats +133% |Vitesse projectiles +15% |Cadence +40%",
    'Coque épicéa': "PV Max +10",
    'Coque chêne': "Vitesse Max +10%",
    'Coque en bouleau': "PV Max +10 | Vitesse Max +5%",
    'Coque en chêne massif': "PV Max +75 | Vitesse Max -20%",
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
    "Bénédiction d'aura": "Crée une aura qui fait des Dégats aux ennemis proches",
    "Bénédiction de rage": "Augmente les Dégats et la vitesse de 50%, réduit les PV à 20",
    "Bénédiction GodMode": "Vous rend invincible",
    "Bénédiction Projectiles": "Envoie une multitude de projectiles autour de vous"
}

fontPixel = os.path.join("data", 'Fonts', 'pixel-font.otf')
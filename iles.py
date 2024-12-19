from fonction_auxiliere import *
from random import *

class Iles:
    def __init__(self, screen_width, screen_height, imageC, imageR, imageM, imageL, xPlayer, yPlayer):

        #Liste des raretés des iles
        self.ile_rarete = ['commun', 'rare','mythique', 'légendaire']

        #On associe une image par rareté
        self.imageC = imageC
        self.imageR = imageR
        self.imageM = imageM
        self.imageL = imageL
        self.imageDisplay = self.imageC

        self.xPlayer = xPlayer
        self.yPlayer = yPlayer

        #Liste des récompenses de chaque type d'ile, ainsi que leurs probabilités
        self.liste_recompenses_communes = ['1_canon', 'canon_en_bronze', 'voile_toile_de_jute', 'coque_epicea', 'coque_chene', self.random_malus(), 'rien']
        self.probabilité_commun = [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3]
        self.liste_recompenses_rares = ['2_canons', 'canon_en_argent', 'canon_balistique', 'voile_latine', 'coque_bouleau', 'coque_chene_massif', self.random_malus(), 'rien', 'bene_dash', 'bene_sante']
        self.probabilité_rare = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.1, 0.125, 0.125]
        self.liste_recompenses_mythiques = ['3_canons', 'canon_en_or', 'canon_tir_double', 'voile_enchantee', 'coque_bois_magique', 'bene_aura', 'bene_rage']
        self.probabilité_mythique = [0.12, 0.12, 0.12, 0.12, 0.12, 0.2, 0.2]
        self.liste_recompenses_legendaires = ['4_canons', 'canon_legendaire', 'voile_legendaire', 'coque_legendaire', 'bene_godmode', 'bene_projectile']
        self.probabilité_legendaire = [0.125, 0.125, 0.125, 0.125, 0.25, 0.25]
        
        #Dictionnaire qui associe le type d'ile à ses probabilités
        self.dict_iles = {
            'commun' : self.probabilité_commun, 
            'rare' : self.probabilité_rare,
            'mythique' : self.probabilité_mythique, 
            'légendaire': self.probabilité_legendaire}

        #Position nulles à l'origine
        self.x = None
        self.y = None

    #Fonction qui retourne le type d'île (str)
    def type_ile(self):
        self.typeList = choices(self.ile_rarete, weights=[0.55, 0.30, 0.14, 0.01], k=1)
        self.type = self.typeList[0]
        return self.type


    #Fonction qui retourne un un malus alééatoire (str)
    def random_malus(self):
        self.malus = [
            "Canons Rouillés",
            "Toile Trouée",
            "Coque Trouée"
        ]
        choice = choices(self.malus)
        return choice

    #Fonction qui retourne une récompense en fonction du type de l'île (str)
    def type_recompenses(self):
        self.weights = self.dict_iles[self.type]
        if self.type == 'légendaire':
            self.liste_recompenses = self.liste_recompenses_legendaires
        elif self.type == 'mythique':
            self.liste_recompenses = self.liste_recompenses_mythiques
        elif self.type == "rare":
            self.liste_recompenses = self.liste_recompenses_rares
        elif self.type == "commun":
            self.liste_recompenses = self.liste_recompenses_communes

        self.recompenseListe = choices(self.liste_recompenses, weights=self.weights, k=1)
        self.recompense = self.recompenseListe[0]
        return self.recompense


    #Fonction qui calcule la distance entre le joueur et l'île et retourne un booléen
    def calccoords(self):
        verifProx = False

        while verifProx == False:
            self.x = random.randint(35, (screen_width-35))
            self.y = random.randint(35, (screen_width-35))
            distance =  calc_distance(self.x, self.y, self.xPlayer, self.yPlayer)

            if distance >= 40:
                verifProx = True
            else:
                verifProx = False
        return verifProx

    #Permet d'afficher l'île sur la map en fonction de sa rareté
    def afficher(self, screen):
        self.calccoords()

        if self.type == "rare":
            self.imageDisplay = self.imageR

        elif self.type == "mythique":
            self.imageDisplay = self.imageM

        elif self.type == "légendaire":
            self.imageDisplay = self.imageL

        else:
            self.imageDisplay = self.imageC
        rect = imageDisplay.get_rect(center=(self.x, self.y))
        screen.blit(imageDisplay, rect)


coucou = Iles()

coucou.type_ile()
coucou.type_recompenses()
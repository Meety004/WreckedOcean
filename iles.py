from fonction_auxiliere import *
from random import *
import pygame

class Iles:
    def __init__(self, screen_width, screen_height, imageC, imageR, imageM, imageL, liste_nav):

        # Liste des raretés des iles
        self.ile_rarete = ['commun', 'rare','mythique', 'légendaire']

        # Dimensions de l'écran
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Taille de l'île
        self.width = 50
        self.height = 50

        # Choix du type d'île
        self.typeList = choices(self.ile_rarete, weights=[0.50, 0.30, 0.14, 0.06], k=1)
        self.type = self.typeList[0]

        # On associe une image à l'île en fonction de son type
        if self.type == "rare":
            imageDisplay = imageR

        elif self.type == "mythique":
            imageDisplay = imageM

        elif self.type == "légendaire":
            imageDisplay = imageL

        else:
            imageDisplay = imageC
        
        imageDisplay = pygame.image.load(imageDisplay).convert_alpha()

        # On modifie la taille de l'image de l'île
        self.imageDisplay = pygame.transform.scale(imageDisplay, (self.width, self.height)).convert_alpha()

        # Liste avec tous les navires (joueur et ennemis)
        self.listeNav = liste_nav

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
        

        #On vérifie si l'île est assez éloignée des navires
        verifProx = False

        while verifProx == False:
            self.x = randint(35, (self.screen_width-35))
            self.y = randint(35, (self.screen_height-35))
            for i in range(len(liste_nav)):
                distance =  calc_distance(self.x, self.y, liste_nav[i].position_x(), liste_nav[i].position_y())

                if distance >= 40:
                    verifProx = True
                else:
                    verifProx = False

        self.timer = randint(600,1200)

    # Méthode qui retourne un un malus alééatoire (str)
    def random_malus(self):
        self.malus = [
            "Canons Rouillés",
            "Toile Trouée",
            "Coque Trouée"
        ]
        choice = choices(self.malus)
        return choice

    # Méthode qui retourne une récompense en fonction du type de l'île (str)
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


    # Permet d'afficher l'île sur la map en fonction de sa rareté
    def afficher(self, screen):
        rect = self.imageDisplay.get_rect(center=(self.x, self.y))
        screen.blit(self.imageDisplay, rect)

    # Méthode de gestion du temps d'existence de l'île
    def decompte(self):
        self.timer -= 1
        return self.timer

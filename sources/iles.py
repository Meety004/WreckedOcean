# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM

import ressources as res
from random import *
import pygame

class Iles:
    def __init__(self, screen_width, screen_height, imageC, imageR, imageM, imageL, liste_nav, liste_iles, niveau):

        # Liste des raretés des iles
        self.ile_rarete = ['commun', 'rare','mythique', 'légendaire']

        # Dimensions de l'écran
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Taille de l'île
        self.width = 5.20/100*screen_width
        self.height = 11.56/100*screen_height

        self.vague = niveau + 1

        # Choix du type d'île

        # if self.vague == 1:
        #     self.typeList = choices(self.ile_rarete, weights=[0.56, 0.41, 0.03, 0.00], k=1)
        # elif self.vague == 2:
        #     self.typeList = choices(self.ile_rarete, weights=[0.54, 0.38, 0.06, 0.02], k=1)
        # elif self.vague == 3:
        #     self.typeList = choices(self.ile_rarete, weights=[0.50, 0.36, 0.10, 0.04], k=1)
        # elif self.vague == 4:
        #     self.typeList = choices(self.ile_rarete, weights=[0.47, 0.35, 0.13, 0.05], k=1)
        # elif self.vague == 5:
        #     self.typeList = choices(self.ile_rarete, weights=[0.43, 0.33, 0.17, 0.07], k=1)
        # elif self.vague == 6:
        #     self.typeList = choices(self.ile_rarete, weights=[0.38, 0.30, 0.22, 0.10], k=1)
        # elif self.vague >= 7:
        #     self.typeList = choices(self.ile_rarete, weights=[0.22, 0.33, 0.30, 0.15], k=1)
        # else:
        #     print("au secours", self.vague)
        self.typeList = choices(self.ile_rarete, weights=[0, 0.33, 0.33, 0.33], k=1)
        
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

        self.liste_iles = liste_iles

        #Liste des récompenses de chaque type d'ile, ainsi que leurs probabilités
        self.liste_recompenses_communes = ['+1 Canon', 'Canon en bronze', 'Voile en toile de jute', 'Coque épicéa', 'Coque chêne', self.random_malus()[0]]
        self.probabilité_commun = [0, 0, 0, 0, 0.5, 0.5]
        self.liste_recompenses_rares = ['+2 Canons', 'Canon en argent', 'Canon ballistique', 'Voile latine', 'Coque en bouleau', 'Coque en chêne massif', 'Bénédiction Dash', 'Bénédiction Santé']
        self.probabilité_rare = [0, 0, 0, 0.5, 0, 0, 0.5, 0.5]
        self.liste_recompenses_mythiques = ['+3 Canons', 'Canon en or', 'Canon à tirs doubles', 'Voile enchantée', 'Coque en bois magique', "Bénédiction d'aura", 'Bénédiction de rage']
        self.probabilité_mythique = [0, 0, 0, 0, 0, 0.5, 0.5]
        self.liste_recompenses_legendaires = ['+4 Canons', 'Canon légendaire', 'Voile légendaire', 'Coque légendaire', 'Bénédiction GodMode', 'Bénédiction Projectiles']
        self.probabilité_legendaire = [0, 0, 0, 0, 0.5, 0.5]
        
        #Dictionnaire qui associe le type d'ile à ses probabilités
        self.dict_iles = {
            'commun' : self.probabilité_commun, 
            'rare' : self.probabilité_rare,
            'mythique' : self.probabilité_mythique, 
            'légendaire': self.probabilité_legendaire}
        
        #On vérifie si l'île est assez éloignée des navires
        verifProx = False
        if self.liste_iles is not None:
            verifProxIle = False
        else:
            verifProxIle = True

        while verifProx == False or verifProxIle == False:
            self.x = randint(100, (self.screen_width-100))
            self.y = uniform(100, (self.screen_height-100))
            verifProx2 = True
            for i in range(len(self.listeNav)):
                distanceIleNav =  res.calc_distance(self.x, self.y, self.listeNav[i].position_x(), self.listeNav[i].position_y())
                if distanceIleNav <= 150:
                    verifProx2 = False
            if verifProx2:
                verifProx = True
            
            if self.liste_iles is not None:
                verifProxIle2 = True
                for i in range(len(self.liste_iles)):
                    distanceIleIle = res.calc_distance(self.x, self.y, self.liste_iles[i].position_x(), self.liste_iles[i].position_y())
                    if distanceIleIle <= 250:
                        verifProxIle2 = False
                if verifProxIle2:
                    verifProxIle = True

        self.timer = randint(1000,2000)

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

    # Méthode qui retourne un un malus alééatoire (str)
    def random_malus(self):
        choice = choices(res.liste_malus)
        return choice

    # Méthode qui retourne une récompense en fonction du type de l'île (str)
    def type_recompenses(self):
        return (self.recompense, self.type)


    # Permet d'afficher l'île sur la map en fonction de sa rareté
    def afficher(self, screen):
        rect = self.imageDisplay.get_rect(center=(self.x, self.y))
        screen.blit(self.imageDisplay, rect)

    # Méthode de gestion du temps d'existence de l'île
    def decompte(self):
        self.timer -= 1
        return self.timer

    def position_x(self):
        return self.x
    
    def position_y(self):
        return self.y
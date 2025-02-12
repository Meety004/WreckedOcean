import ressources as res
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
        self.typeList = choices(self.ile_rarete, weights=[0.50, 0.36, 0.1, 0.04], k=1)
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
        self.liste_recompenses_communes = ['+1 Canon', 'Canon en bronze', 'Voile en toile de jute', 'Coque épicéa', 'Coque chêne', self.random_malus()[0], 'Rien']
        self.probabilité_commun = [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3]
        self.liste_recompenses_rares = ['+2 Canons', 'Canon en argent', 'Canon Ballistique', 'Voile Latine', 'Coque en bouleau', 'Coque en chêne massif', self.random_malus()[0], 'Rien', 'Bénédiction Dash', 'Bénédiction Santé']
        self.probabilité_rare = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.1, 0.125, 0.125]
        self.liste_recompenses_mythiques = ['+3 Canons', 'Canon en or', 'Canon à tirs doubles', 'Voile Enchantée', 'Coque en bois magique', "Bénédiction d'aura", 'Bénédiciton de rage']
        self.probabilité_mythique = [0.12, 0.12, 0.12, 0.12, 0.12, 0.2, 0.2]
        self.liste_recompenses_legendaires = ['+4 Canons', 'Canon légendaire', 'Voile légendaire', 'Coque légendaire', 'Bénédiction GodMode', 'Bénédiction Projectile']
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
            for i in range(len(self.listeNav)):
                distanceIleNav =  res.calc_distance(self.x, self.y, self.listeNav[i].position_x(), self.listeNav[i].position_y())
                if distanceIleNav >= 40:
                    verifProx = True
                else:
                    verifProx = False

        self.timer = randint(400,800)

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

# les IA ennemies
# importation des modules
import pygame
import random
import math

# importation de la classe Navire
from Navire import Navire

# comportement de l'IA
# actuel : avance sans jamais s'arreter et essaye de garder une direction coherente (ne vas jamais tt le temps tout droit et ne tourne pas en rond)
# fonctionnement : l'IA a une action de base. il a 2 chance sur 50 de changer d'action. si l'action est la meme 23 fois de suite il doit changer (permet de ne pas faire un trop gros tour)
# a venir : evitement des bordure de la map

class IA_ennemis(Navire):
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height):
        super().__init__(v_max, acceleration, maniabilite, image, screen_width, screen_height)
        self.action = random.randint(0, 2) # 0 = aller tout droit, 1 = tourner a gauche, 2 = tourner a droite
        self.compte_action = 0 # compte combien de fois l'IA fait la meme action (ne peut pas la faire plus de 23 fois)

    def bouger(self):
        nouvelle_action = random.randint(0, 50)
        if nouvelle_action > 3:
            nouvelle_action = self.action
        
        if self.compte_action >= 23:
            while nouvelle_action == self.action:
                nouvelle_action = random.randint(0, 50)
                if nouvelle_action > 3:
                    nouvelle_action = self.action

        if nouvelle_action == self.action: # si il refait la meme action ajoute 1 au compte
            self.compte_action += 1
        else:
            self.compte_action = 0
        
        self.action = nouvelle_action

        # si l'action est de 0 alors le bateau ne tourne pas
        if self.action == 1:
            super().tourne_gauche()
        if self.action == 2:
            super().tourne_droite()
        
        super().accelerer() # pour l'instant les ennemies avance tout le temps
        super().avancer()
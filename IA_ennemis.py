# les IA ennemies
# importation des modules
import pygame
import random
import math
import fonction_auxiliere

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

    # verifie si la cible de cette IA (le joueur pour l'instant) est a porté de cette IA
    def ennemi_in_range(self, ennemi_x, ennemi_y):
        if fonction_auxiliere.calc_distance(self.x, self.y, ennemi_x, ennemi_y) <= 150:
            return True
        return False

    # cette fonction sert uniquement a incliner la position de tire
    def position_de_tire(self, position_cible_x, position_cible_y):
            # calcule l'angle entre les 2 points
            angle_de_tire = math.degrees(math.atan2(position_cible_y - self.y, position_cible_x - self.x))
            # calcule lequel des 2 canon est le plus proche pour s'orienter dans le bon sens
            if angle_de_tire - self.angle + 90 < angle_de_tire - self.angle - 90:
                super().tourne_gauche()
            else:
                super().tourne_droite()

    def bouger(self, ennemi_x, ennemi_y):
        # a chaque fois que cette fonction est appelé elle a une action (tourner a droite, gauche ou tout droit)
        nouvelle_action = random.randint(0, 50) # 2 chance sur 50 de changer d'action
        if nouvelle_action > 3: # si c'est 0 elle va tout droit, si c'est 1 elle tourne a droite si c'est 2 a gauche et sinon elle refait la même action qu'avant pour eviter de changer tout le temps de trajectoire
            nouvelle_action = self.action
        
        if self.compte_action >= 23: # verifie si ca fait plus de 23 fois qu'elle fait la même chose pour changer un peu (23 car tourner 23 fois represente un 180 et c'est inutile d'aller au dela)
            while nouvelle_action == self.action: # tant que c'est la même action ca change
                nouvelle_action = random.randint(0, 50)
                if nouvelle_action > 3:
                    nouvelle_action = self.action

        # self.action est l'action qu'elle va faire et c'est definitif (dans cet appel de la fonction)

        if nouvelle_action == self.action: # si il refait la meme action ajoute 1 au compte
            self.compte_action += 1
        else:
            self.compte_action = 0
        
        self.action = nouvelle_action

        # si il y a un ennemi a porté il suit le paterne d'inslinaison pour tirer
        if self.ennemi_in_range(ennemi_x, ennemi_y):
            self.position_de_tire(ennemi_x, ennemi_y)
            self.vitesse_max = 8
        else: # si aucun ennemi est a portée il avance comme prevu
            self.vitesse_max = 5
            if self.action == 1:
                super().tourne_droite()
            if self.action == 2:
                super().tourne_gauche()
        
        super().accelerer() # pour l'instant les ennemies avance tout le temps
        super().avancer()

    def tirer(self, cible_x, cible_y):
        # si l'ennemi est a distance meme si il est pas bien incliner ca tire
        if fonction_auxiliere.calc_distance(self.x, self.y, cible_x, cible_y) <= 140:
            return super().shoot()
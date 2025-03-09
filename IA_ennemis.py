# les IA ennemies
# importation des modules
import pygame
import random
import math
import ressources as res

# importation de la classe Navire
from Navire import Navire

class IA_ennemis_basiques(Navire):
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt):
        super().__init__(v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, 1)
        self.action = random.randint(0, 2) # 0 = aller tout droit, 1 = tourner a gauche, 2 = tourner a droite
        self.compte_action = 0 # compte combien de fois l'IA fait la même action (ne peut pas la faire plus de 23 fois)
        self.verif_ile = (False, 0)

    # vérifie si la cible de cette IA est à portée de cette IA
    def ennemi_in_range(self, liste_adversaire):
        for ennemi in liste_adversaire:
            if ennemi.get_ID() != self.ID:
                if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 120:
                    return True
        return False
    
    def ile_in_range(self, liste_iles):
        for ile in range(len(liste_iles)):
            if res.calc_distance(self.x, self.y, liste_iles[ile].position_x(), liste_iles[ile].position_y()) <= 300:
                return (True, ile)
        return (False, 0)

    # cette fonction sert uniquement a incliner la position de tir
    def position_de_tir(self, liste_adversaire):
            for i in range(len(liste_adversaire)):
                if liste_adversaire[i].get_ID() != self.ID:
                    # calcule l'angle entre les 2 points
                    angle_de_tir = math.degrees(math.atan2(liste_adversaire[i].position_y() - self.y, liste_adversaire[i].position_x() - self.x))
            # calcule lequel des 2 canons est le plus proche pour s'orienter dans le bon sens
            if angle_de_tir - self.angle + 90 < angle_de_tir - self.angle - 90:
                super().tourne_droite()
            else:
                super().tourne_gauche()

    def bouger(self, liste_adversaire, liste_iles, inutile):
        self.verif_ile = self.ile_in_range(liste_iles)
        if self.verif_ile[0]:
            truc = self.y - liste_iles[self.verif_ile[1]].position_y()
            if truc < 0 :
                truc = -truc
            var_intermediaire = (truc)/(res.calc_distance(self.x, self.y, liste_iles[self.verif_ile[1]].position_x(), liste_iles[self.verif_ile[1]].position_y()))
            angle_ile = math.degrees(math.acos(var_intermediaire)) - self.angle
            if self.x < liste_iles[self.verif_ile[1]].position_x() :
                if angle_ile > 5 :
                    super().tourne_droite()
                elif angle_ile < -5:
                    super().tourne_gauche()
            else:
                angle_ile+=180
                if angle_ile > 5 :
                    super().tourne_droite()
                elif angle_ile < -5:
                    super().tourne_gauche()
        else:
            nouvelle_action = random.randint(0, 50) # 2 chances sur 50 de changer d'action
            if nouvelle_action > 3: # si c'est 0 elle va tout droit, si c'est 1 elle tourne à droite si c'est 2 à gauche et sinon elle refait la même action qu'avant pour eviter de changer tout le temps de trajectoire
                nouvelle_action = self.action
            
            if self.compte_action >= 23: # verifie si ça fait plus de 23 fois qu'elle fait la même chose pour changer un peu (23 car tourner 23 fois représente un 180 et c'est inutile d'aller au delà)
                while nouvelle_action == self.action: # tant que c'est la même action ca change
                    nouvelle_action = random.randint(0, 50)
                    if nouvelle_action > 3:
                        nouvelle_action = self.action

            # self.action est l'action qu'elle va faire et c'est définitif (dans cet appel de la fonction)

            if nouvelle_action == self.action: # s'il refait la même action ajoute 1 au compte
                self.compte_action += 1
            else:
                self.compte_action = 0
            
            self.action = nouvelle_action

            # s'il y a un ennemi à portée il suit le paterne d'inclinaison pour tirer
            if self.ennemi_in_range(liste_adversaire):
                self.position_de_tir(liste_adversaire)
                self.vitesse_max = 9
            else: # si aucun ennemi est à portée il avance comme prévu
                self.vitesse_max = 5 
                if self.action == 1:
                    super().tourne_droite()
                if self.action == 2:
                    super().tourne_gauche()
        
        super().accelerer() # Les ennemis basiques avancent tout le temps
        super().avancer()

    def tirer(self, cible_x, cible_y):
        # si l'ennemi est à distance même s'il n'est pas bien incliné ça tire
        if res.calc_distance(self.x, self.y, cible_x, cible_y) <= 140:
            return super().shoot()

    def position_x(self):
        return self.x
    
    def position_y(self):
        return self.y

class IA_ennemis_chasseurs(Navire):
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt):
        super().__init__(v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, 2)
    
    # vérifie si le joueur est à portée de cette IA
    def joueur_in_range(self, liste_joueur):
        if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 120:
            return True
        return False

    def bouger(self, inutile1, inutile2, liste_joueur):
        truc = self.y - liste_joueur[0].position_y()
        if truc < 0 :
            truc = -truc
        var_intermediaire = (truc)/(res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()))
        angle_ile = math.degrees(math.acos(var_intermediaire)) - self.angle
        if self.x < liste_joueur[0].position_x() :
            if angle_ile > 5 :
                super().tourne_droite()
            elif angle_ile < -5:
                super().tourne_gauche()
        else:
            angle_ile+=180
            if angle_ile > 5 :
                super().tourne_droite()
            elif angle_ile < -5:
                super().tourne_gauche()

        super().accelerer() # Les chasseurs avancent tout le temps
        super().avancer()
    
    def tirer(self, cible_x, cible_y):
        # si l'ennemi est à distance même s'il n'est pas bien incliné ça tire
        if res.calc_distance(self.x, self.y, cible_x, cible_y) <= 140:
            return super().shoot()

    def position_x(self):
        return self.x
    
    def position_y(self):
        return self.y
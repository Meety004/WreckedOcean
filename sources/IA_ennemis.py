# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM

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
        self.verif_ile = (False, 0) # infos sur une île à portée

    # vérifie si la cible de cette IA est à portée de cette IA
    def ennemi_in_range(self, liste_adversaire):
        for ennemi in liste_adversaire:
            if ennemi.get_ID() != self.ID:
                if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 120:
                    return True
        return False
    
    # vérifie si une île est à portée
    def ile_in_range(self, liste_iles):
        for ile in range(len(liste_iles)):
            if res.calc_distance(self.x, self.y, liste_iles[ile].position_x(), liste_iles[ile].position_y()) <= 300:
                return (True, ile)
        return (False, 0)

    # Gère les déplacements de l'IA
    def bouger(self, liste_adversaire, liste_iles, inutile):
        self.verif_ile = self.ile_in_range(liste_iles)
        if self.verif_ile[0]: # si une île est à portée, se dirige vers l'île, sinon, se déplace aléatoirement
            calcul_intermediaire = self.y - liste_iles[self.verif_ile[1]].position_y() # différence de la valeur y entre l'IA et l'île
            if calcul_intermediaire < 0 :
                calcul_intermediaire = -calcul_intermediaire
            var_intermediaire = (calcul_intermediaire)/(res.calc_distance(self.x, self.y, liste_iles[self.verif_ile[1]].position_x(), liste_iles[self.verif_ile[1]].position_y())) # rapport entre la différence de la valeur y entre l'IA et l'île et la distance entre l'IA et l'île
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

            if self.ennemi_in_range(liste_adversaire):
                self.vitesse_max = 5
            else: # si aucun ennemi est à portée il avance comme prévu
                self.vitesse_max = 4
                if self.action == 1:
                    super().tourne_droite()
                if self.action == 2:
                    super().tourne_gauche()
        
        super().accelerer() # Les ennemis basiques avancent tout le temps
        super().avancer()

    def tirer(self, cible_x, cible_y, inutile):
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

    # Gère les déplacements de l'IA
    def bouger(self, inutile1, inutile2, liste_joueur):
        calcul_intermediaire = self.y - liste_joueur[0].position_y()
        if calcul_intermediaire < 0 :
            calcul_intermediaire = -calcul_intermediaire
        var_intermediaire = (calcul_intermediaire)/(res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y())) # rapport entre la différence de la valeur y entre l'IA et le joueur et la distance entre l'IA et le joueur
        angle_joueur = math.degrees(math.acos(var_intermediaire)) - self.angle
        if self.x < liste_joueur[0].position_x() :
            if angle_joueur > 5 :
                super().tourne_droite()
            elif angle_joueur < -5:
                super().tourne_gauche()
        else:
            angle_joueur+=180
            if angle_joueur > 5 :
                super().tourne_droite()
            elif angle_joueur < -5:
                super().tourne_gauche()

        super().accelerer() # Les chasseurs avancent tout le temps
        super().avancer()
    
    def tirer(self, inutilex, inutiley, liste_joueur):
        # si l'ennemi est à distance même s'il n'est pas bien incliné ça tire
        if self.joueur_in_range(liste_joueur):
            return super().shoot()

    def position_x(self):
        return self.x
    
    def position_y(self):
        return self.y

class IA_ennemis_stage_2(Navire):
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt):
        super().__init__(v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, 3)
        self.action = random.randint(0, 2)

    # vérifie si le joueur est à portée de cette IA
    def joueur_in_range(self, liste_joueur):
        if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 250:
            return (True, True)
        elif res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 120:
            return (True, False)
        else:
            return (False, False)
        
    # vérifie si une île est à portée
    def ile_in_range(self, liste_iles):
        for ile in range(len(liste_iles)):
            if res.calc_distance(self.x, self.y, liste_iles[ile].position_x(), liste_iles[ile].position_y()) <= 300:
                return (True, ile)
        return (False, 0)
        
    def bouger(self, inutile, liste_iles, liste_joueur):
        if self.joueur_in_range(liste_joueur)[0]:
            if self.equipement['canons'] not in ('+1 Canon', '+2 Canons', '+4 Canons'):
                if self.x < liste_joueur[0].position_x():
                    operateur = 60
                elif self.x > liste_joueur[0].position_x():
                    operateur = -60
                else:
                    operateur = 180
            else:
                operateur = 0
            
            calcul_intermediaire = self.y - liste_joueur[0].position_y() - operateur
            if calcul_intermediaire < 0 :
                calcul_intermediaire = -calcul_intermediaire
            var_intermediaire = (calcul_intermediaire)/(res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y() + operateur)) # rapport entre la différence de la valeur y entre l'IA et le joueur et la distance entre l'IA et le joueur
            angle_joueur = math.degrees(math.acos(var_intermediaire)) - self.angle
            if self.x < liste_joueur[0].position_x() :
                if angle_joueur > 5 :
                    super().tourne_droite()
                elif angle_joueur < -5:
                    super().tourne_gauche()
            else:
                angle_joueur+=180
                if angle_joueur > 5 :
                    super().tourne_droite()
                elif angle_joueur < -5:
                    super().tourne_gauche()
        
        elif self.ile_in_range(liste_iles)[0] and res.comparaison_valeur_equipement_ile(liste_iles[self.ile_in_range(liste_iles)[1]], self.equipement):
            self.verif_ile = self.ile_in_range(liste_iles)
            if self.verif_ile[0]: # si une île est à portée, se dirige vers l'île, sinon, se déplace aléatoirement
                calcul_intermediaire = self.y - liste_iles[self.verif_ile[1]].position_y() # différence de la valeur y entre l'IA et l'île
                if calcul_intermediaire < 0 :
                    calcul_intermediaire = -calcul_intermediaire
                var_intermediaire = (calcul_intermediaire)/(res.calc_distance(self.x, self.y, liste_iles[self.verif_ile[1]].position_x(), liste_iles[self.verif_ile[1]].position_y())) # rapport entre la différence de la valeur y entre l'IA et l'île et la distance entre l'IA et l'île
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
            change = random.randint(0, 20)
            if change == 0:
                self.action = random.randint(0, 3)
            if self.action == 0 :
                super().tourne_droite()
            elif self.action == 1:
                super().tourne_gauche()
        
        super().accelerer() # Les chasseurs avancent tout le temps
        super().avancer()

    def tirer(self, inutilex, inutiley, liste_joueur):
        # si l'ennemi est à distance même s'il n'est pas bien incliné ça tire
        if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) < 80 :
            return super().shoot()

    def position_x(self):
        return self.x
    
    def position_y(self):
        return self.y
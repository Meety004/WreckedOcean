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
        """
        Constructeur des IA basiques
        Prend en argument la vitesse max, l'acceleration, la maniabilité, l'image du navire et la taille de l'écran
        """
        super().__init__(v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, 1)
        self.action = random.randint(0, 2) # 0 = aller tout droit, 1 = tourner a gauche, 2 = tourner a droite
        self.compte_action = 0 # compte combien de fois l'IA fait la même action (ne peut pas la faire plus de 23 fois d'affilée)
        self.verif_ile = (False, 0) # infos sur une île à portée

    def ennemi_in_range(self, liste_adversaire):
        """ 
        Vérifie si la cible de cette IA est à portée de cette IA
        Argument : liste des adversaires(liste_navire)
        """
        for ennemi in liste_adversaire:
            if ennemi.get_ID() != self.ID:
                if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 120:
                    return True
        return False
    
    def ile_in_range(self, liste_iles):
        """ 
        Vérifie si une île est à portée
        Argument : liste des îles
        """
        for ile in range(len(liste_iles)):
            if res.calc_distance(self.x, self.y, liste_iles[ile].position_x(), liste_iles[ile].position_y()) <= 300:
                return (True, ile)
        return (False, 0)

    def bouger(self, liste_adversaire, liste_iles, inutile):
        """
        Gère les déplacements de l'IA
        Prend en compte la liste_adversaire(la liste liste_navire), la liste des îles et un quatrième argument non utilisé
        """
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
            
            if self.compte_action >= 23: # verifie si ça fait plus de 23 fois qu'elle fait la même action pour changer un peu (car tourner 23 fois représente un 180 et c'est inutile d'aller au delà)
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

            if self.ennemi_in_range(liste_adversaire):# si un ennemi est à portée, sa vitesse est augmentée
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
        """ 
        Gère les tirs de l'IA
        Prend en argument la position x et y de la cible et un argument non utilisé 
        """
        # si l'ennemi est à distance même s'il n'est pas bien incliné ça tire
        if res.calc_distance(self.x, self.y, cible_x, cible_y) <= 140:
            return super().shoot()

    def position_x(self):
        """ 
        Renvoie la position x 
        """
        return self.x
    
    def position_y(self):
        """ 
        Renvoie la position y 
        """
        return self.y

class IA_ennemis_chasseurs(Navire):
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt):
        """
        Constructeur des IA chasseurs
        Prend en argument la vitesse max, l'acceleration, la maniabilité, l'image du navire et la taille de l'écran
        """
        super().__init__(v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, 2)
    
    def joueur_in_range(self, liste_joueur):
        """ vérifie si le joueur est à portée de cette IA
        Argument : liste_joueur"""
        if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 120:
            return True
        return False

    def bouger(self, inutile1, inutile2, liste_joueur):
        """
        Gère les déplacements de l'IA
        Prend en compte deux arguments non utilisés et la liste_joueur
        """
        #L'IA chasseur se dirige constamment vers le joueur
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
        """ 
        Gère les tirs de l'IA 
        Prend deux arguments non utiilisés et la liiste_joueur 
        """
        # si le joueur est à distance ça tire
        if self.joueur_in_range(liste_joueur):
            return super().shoot()

    def position_x(self):
        """ 
        Renvoie la position x de l'IA 
        """
        return self.x
    
    def position_y(self):
        """ 
        Renvoie la position y de l'IA
          """
        return self.y

class IA_ennemis_stage_2(Navire):
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt):
        """
        Constructeur des IA stage 2 (ou "intelligentes")
        Prend en argument la vitesse max, l'acceleration, la maniabilité, l'image du navire et la taille de l'écran
        """
        super().__init__(v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, 3)
        self.action = random.randint(0, 2)

    def joueur_in_range(self, liste_joueur):
        """ 
        Vérifie si le joueur est à portée de cette IA
        Argument : liste_joueur
        """
        if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 250:
            return (True, True)
        elif res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 120:
            return (True, False)
        else:
            return (False, False)
        
    def ile_in_range(self, liste_iles):
        """ 
        Vérifie si une île est à portée
        Argument : liste des îles
        """
        for ile in range(len(liste_iles)):
            if res.calc_distance(self.x, self.y, liste_iles[ile].position_x(), liste_iles[ile].position_y()) <= 300:
                return (True, ile)
        return (False, 0)
        
    def bouger(self, inutile, liste_iles, liste_joueur):
        """
        Gère les déplacements de l'IA
        Prend en compte un argument non utilisé, la liste des îles et la liste_joueur
        """
        if self.joueur_in_range(liste_joueur)[0]:# Si le joueur est proche, se dirige vers lui
            if self.equipement['canons'] not in ('+1 Canon', '+2 Canons', '+4 Canons'):# Si l'IA a un équipement qui lui permet de tirer devant elle, elle se dirige tout droit vers le joueur, sinon s'incline de façon à l'atteindre
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
        
        elif self.ile_in_range(liste_iles)[0] and res.comparaison_valeur_equipement_ile(liste_iles[self.ile_in_range(liste_iles)[1]], self.equipement, self.benedictions):# Si le joueur n'est pas proche et qu'une île de valeur suffisante par rapport à l'équipement de l'IA est proche
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

        else:# Se déplace aléatoirement
            change = random.randint(0, 20)
            if change == 0:
                self.action = random.randint(0, 3)
            if self.action == 0 :
                super().tourne_droite()
            elif self.action == 1:
                super().tourne_gauche()
        
        self.utilisation_benediction(liste_joueur)
        super().accelerer() # Les chasseurs avancent tout le temps
        super().avancer()

    def utilisation_benediction(self, liste_joueur):
        """ 
        Gère l'utilisation des bénédictions 
        Argument : liste_joueur
        """

        if "Bénédiction Dash" in self.benedictions:# Utilise le dash si le joueur est à plus de 500px de distance
            if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) > 500:
                if self.benedictions[0] == "Bénédiction Dash":
                    self.use_benediction_1()
                else:
                    self.use_benediction_2()
        
        if "Bénédiction Santé" in self.benedictions:# Utilise le soin si sa vie est à moitié ou moins
            if self.vie <= (self.maxVie/2):
                if self.benedictions[0] == "Bénédiction Santé":
                    self.use_benediction_1()
                else:
                    self.use_benediction_2()
        
        if "Bénédiction d'aura" in self.benedictions:# Utilise l'aura si le joueur est assès proche
            if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 120:
                if self.benedictions[0] == "Bénédiction d'aura":
                    self.use_benediction_1()
                else:
                    self.use_benediction_2()

        if "Bénédiction Projectiles" in self.benedictions:# Utilise le méga tir si le joueur est assès proche
            if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 100:
                if self.benedictions[0] == "Bénédiction Projectiles":
                    self.use_benediction_1()
                else:
                    self.use_benediction_2()

        if "Bénédiction GodMode" in self.benedictions:# Utilise le godmode si le joueur est proche et l'IA a peu de vie
            if self.vie <= 30 and res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) <= 400:
                if self.benedictions[0] == "Bénédiction GodMode":
                    self.use_benediction_1()
                else:
                    self.use_benediction_2()

        if self.benedictions[0] == "Bénédiction de rage":# Utilise la rage dès qu'elle est disponible
            self.use_benediction_1()
        elif self.benedictions[1] == "Bénédiction de rage":
            self.use_benediction_2()

    def choix_slot_benediction(self):
        """ 
        Gère le choix de positionnement de la bénédiction 
        """
        if self.recompense[0] in res.liste_benedictions:
            if self.benedictions[0] == None:
                return 0
            elif self.benedictions[1] == None:
                return 1
            elif res.valeur_equipement(self.benedictions[0]) < res.valeur_equipement(self.benedictions[1]):
                return 0
            else:
                return 1

    def tirer(self, inutilex, inutiley, liste_joueur):
        """ 
        Gère les tirs
        Prend en argument deux arguments non utilisés et la liste_joueur 
        """
        if res.calc_distance(self.x, self.y, liste_joueur[0].position_x(), liste_joueur[0].position_y()) < 80 :
            return super().shoot()

    def position_x(self):
        """ 
        Renvoie la position x 
        """
        return self.x
    
    def position_y(self):
        """ 
        Renvoie la position y 
        """
        return self.y
# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM

# Imports des librairies et des modules
import math
import pygame
import ressources as res

class Shot:
    def __init__(self, x, y, angle, distance_max, img, tireur, canons, inraged, tupleScreen):
        """ 
        Constructeur de la classe Shot
        Chaque tir est un objet
        Arguments: la position initiale, l'angle de tir (les cotés du tireur), la distance maximale qu'ils peuvent parcourir, l'image du boulet, l'ID du tireur, le type de canon et si le tireur est enragé ou non 
        """
        self.x = x
        self.y = y
        self.position_initiale_x = x
        self.position_initiale_y = y
        self.screen_width = tupleScreen[0]
        self.screen_height = tupleScreen[1]
        self.width = self.screen_width*0.01125*1.75
        self.height = self.screen_height*0.025*1.75
        self.angle = angle
        self.vitesse = 9
        self.distance_max = distance_max
        image = pygame.image.load(img)
        self.image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()
        self.ID_tireur = tireur
        self.canons = canons

        # On change les caractéristiques des canons en fonction de l'équipement
        if self.canons == "Canon en argent":
            self.vitesse = self.vitesse * 1.05
        elif self.canons == "Canon en or":
            self.vitesse = self.vitesse * 1.1
        elif self.canons == "Canon ballistique":
            self.distance_max = self.distance_max * 2
        elif self.canons == "Canon légendaire":
            self.vitesse = self.vitesse * 1.15
        elif self.canons == "Canons Rouillés":
            self.vitesse = self.vitesse * 0.75

        self.inraged = inraged

    # On fait avancer le boulet
    def avancer(self, liste_navire):
        """
        Le boulet avance tant qu'il ne croise pas un navire avec le même ID que le tireur
        Argument: liste_navire
        """
        bateaux_in_range = []
        bateau_proche = None

        # Calcule la position des bateaux pour voir il n'y en a pas un a proximité
        for i in range(len(liste_navire)):
            if res.calc_distance(self.x, self.y, liste_navire[i].position_x(), liste_navire[i].position_y()) <= 40 and self.ID_tireur != liste_navire[i].ID:
                bateaux_in_range.append((liste_navire[i], res.calc_distance(self.x, self.y, liste_navire[i].position_x(), liste_navire[i].position_y())))
        
        # La cible sera le premier bateau dans la liste si ils sont tous a la même distance
        if len(bateaux_in_range) > 0:
            bateau_proche = bateaux_in_range[0]
        # Si un navire se rapproche du boulet et se trouve plus proche que la cible actuelle, il devient la nouvelle cible.
        if bateau_proche is not None:
            for i in range(len(bateaux_in_range)):
                if bateaux_in_range[i][1] > bateau_proche[1]:
                    bateau_proche = bateaux_in_range[i]

        # Ajuste la position du tire pour l'incliner vers le bateau le plus proche afin d'aider le joueur a toucher sa cible
        if bateau_proche is not None:
            if self.x > bateau_proche[0].x: # ajuste les x
                self.x -= self.vitesse
            else:
                self.x += self.vitesse
            if self.y > bateau_proche[0].y: # ajuste les y
                self.y -= self.vitesse
            else:
                self.y += self.vitesse
        else:
            # Si il n'y a pas de bateau a proximité le boulet continue sa trajectoire
            self.x += self.vitesse * math.cos(math.radians(self.angle - 90))
            self.y += self.vitesse * math.sin(math.radians(self.angle - 90))


    
    def collision(self, cible_x, cible_y, cible_ID):
        """
        Vérifie si le boulet est entré en collision avec un navire
        Paramètres: Coordonnées de la cible et son ID
        """
        # Verifie si le boulet de canon est dans le bateau pour les ordonnées (on calcule par rapport a l'inclinaison du bateau aussi)
        if cible_ID != self.ID_tireur:
            if (cible_x - 15) < self.x < (cible_x + 15) and (cible_y - 15) < self.y < (cible_y + 15):
                return True
        return False
    
    # Si la distance parcourue par le boulet est trop grande il disparait    
    def despawn_distance(self):
        """
        On fait disparaitre le boulet s'il va trop loin
        """
        return res.calc_distance(self.x, self.y, self.position_initiale_x, self.position_initiale_y) >= self.distance_max
    
    
    # Affiche le boulet
    def afficher(self, screen):
        """
        On affiche le boulet à l'écran
        Argument: screen
        """
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)

    def getIDTireur(self):
        """
        Renvoie l'ID du tireur
        """
        return self.ID_tireur

    def is_inraged(self):
        """
        Renvoie l'état de la bénédiction de rage
        """
        return self.inraged
    

    def sortir_ecran(self):
        """
        Gère les sorties d'écran du boulet
        """
        if self.x > self.screen_width:
            self.x = 0
        if self.x < 0:
            self.x = self.screen_width
        if self.y > self.screen_height + 20:
            self.y = 0
        if self.y < 0:
            self.y = self.screen_height
import math
import pygame
import ressources as res

class Shot:
    def __init__(self, x, y, angle, distance_max, img, tireur, canons):
        self.x = x
        self.y = y
        self.position_initiale_x = x
        self.position_initiale_y = y
        self.width = 22
        self.height = 22
        self.angle = angle
        self.vitesse = 13
        self.distance_max = distance_max
        image = pygame.image.load(img)
        self.image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()
        self.ID_tireur = tireur
        self.canons = canons

        #On change les caractéristiques des canons en fonction de l'équipement

        if self.canons == "Canon en argent":
            self.vitesse = self.vitesse * 1.05
        elif self.canons == "Canon en or":
            self.vitesse = self.vitesse * 1.1
        elif self.canons == "Canon Ballistique":
            self.distance_max = self.distance_max * 2
        elif self.canons == "Canon légendaire":
            self.vitesse = self.vitesse * 1.15
        elif self.canons == "Canons Rouillés":
            self.vitesse = self.vitesse * 0.85

    # le boulet avance
    def avancer(self):
        self.x += self.vitesse * math.cos(math.radians(self.angle - 90))
        self.y += self.vitesse * math.sin(math.radians(self.angle - 90))
    
    def collision(self, cible_x, cible_y, cible_ID):
        # verifie si le boulet de canon est dans le bateau pour les x (on calcule par rapport a l'inclinaison du bateau aussi)
        if cible_ID != self.ID_tireur:
            if (cible_x - 15) < self.x < (cible_x + 15) and (cible_y - 15) < self.y < (cible_y + 15):
                return True
        return False
    
    # si la distance parcouru par le boulet est trop grande il despawn    
    def despawn_distance(self):
        return res.calc_distance(self.x, self.y, self.position_initiale_x, self.position_initiale_y) >= self.distance_max
    
    
    # affiche le boulet
    def afficher(self, screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)

    def getIDTireur(self):
        return self.ID_tireur
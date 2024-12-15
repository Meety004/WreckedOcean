import math
import pygame
import random
import shot

class Navire:
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height):
        # Contrôle du vaisseau
        self.vitesse_max = v_max
        self.acceleration = acceleration
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.vitesse = 0
        self.angle = 270
        self.maniabilite = maniabilite # le temps qu'il met pour tourner. c'est ca "vitesse de tournage"
        self.width = 40
        self.height = 60
        original_image = pygame.image.load(image).convert_alpha()
        #original_image = pygame.transform.rotate(original_image, 90).convert_alpha()
        original_image = pygame.transform.scale(original_image, (self.width, self.height)).convert_alpha()
        self.image = original_image  # Image qui sera affichée
        self.dernier_tire = 0 # le denier tire fait par le bateau pour le chrono
        self.cadance_tire = 1000 # en milliseconde

    # le bateau avance en permanence de la vitesse (donc si la vitesse vaut 0 il avance pas)
    def avancer(self):
        self.x += self.vitesse * math.cos(math.radians(self.angle - 90))
        self.y += self.vitesse * math.sin(math.radians(self.angle - 90))

    # auglente la vitesse
    def accelerer(self):
        if self.vitesse < self.vitesse_max:
            self.vitesse += self.acceleration

    # si il arrete d'avancer le bateau décelère
    def ralentit(self):
        if self.vitesse > 0:
            self.vitesse -= 0.07
        if self.vitesse < 0:
            self.vitesse = 0

    def tourne_gauche(self):
        if self.vitesse > 0:
            self.angle -= self.maniabilite
            if self.angle < 0:
                self.angle += 360

    def tourne_droite(self):
        if self.vitesse > 0:
            self.angle += self.maniabilite
            if self.angle >= 360:
                self.angle -= 360

    def sortir_ecran(self, largeur_ecran, longueur_ecran):
        if self.x > largeur_ecran:
            self.x = 0
        if self.x < 0:
            self.x = largeur_ecran
        if self.y > longueur_ecran:
            self.y = 0
        if self.y < 0:
            self.y = longueur_ecran

    def afficher(self, screen):
        # Appliquer la rotation à l'image d'origine sans la modifier définitivement
        rotated_image = pygame.transform.rotate(self.image, -self.angle).convert_alpha()
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect)

    def shoot(self):
        # verifie si il a rechargé
        if pygame.time.get_ticks() - self.dernier_tire >= self.cadance_tire:
            self.dernier_tire = pygame.time.get_ticks()

            #argument : x, y, angle, distance_max, image
            # l'angle est ajusté en fonction de la vitesse du bateau. si il avance les boulet continue dans sa direction
            tire_droite = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, 150, "images/boulet_canon.png")
            tire_gauche = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, 150, "images/boulet_canon.png")
            return [tire_droite, tire_gauche]
        else:
            return None

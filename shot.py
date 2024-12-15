import math
import pygame
import fonction_auxiliere as fonc_aux

class Shot:
    def __init__(self, x, y, angle, distance_max, img):
        self.x = x
        self.y = y
        self.position_initiale_x = x
        self.position_initiale_y = y
        self.width = 20
        self.height = 20
        self.angle = angle
        self.vitesse = 10
        self.distance_max = distance_max
        image = pygame.image.load(img)
        self.image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()

    # le boulet avance
    def avancer(self, delta_time):
        self.x += self.vitesse * math.cos(math.radians(self.angle - 90)) * delta_time
        self.y += self.vitesse * math.sin(math.radians(self.angle - 90)) * delta_time
    
    # si la distance parcouru par le boulet est trop grande il despawn
    def despawn_distance(self):
        return fonc_aux.calc_distance(self.x, self.y, self.position_initiale_x, self.position_initiale_y) >= self.distance_max
    
    def afficher(self, screen):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)
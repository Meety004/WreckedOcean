import pygame
import class_button as bouton

class Menu:
    def __init__(self, nb_bouton, texte, image, width, height):
        self.nombre_boutons = nb_bouton
        self.texte_affiche = texte
        self.width = width
        self.height = height
        
        image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()
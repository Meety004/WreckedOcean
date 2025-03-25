# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM

# Importation de pygame
import pygame

# Création de la classe qui gère les boutons
class Bouton:
    def __init__(self, x, y, width, height, image):
        """
        Constructeur de la classe Bouton.
        Prend en argument une longueur, une largeur, une abscisse et une ordonnées ainsi qu'une image.
        """
        # On centre le bouton
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # On convertit la taille de l'image en fonction de la fenêtre de jeu
        original_image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.width, self.height)).convert_alpha()
        self.image = original_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def is_pressed(self):
        """
        Détecte si le bouton est cliqué.
        Renvoie True si c'est le cas, False sinon.
        """
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pressed()[0]:
            if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
                return True
        return False
    
    def affichage(self, screen):
        """
        Affiche le bouton sur l'écran
        Prend en argument l'écran sur lequel il faut afficher le bouton.
        """
        screen.blit(self.image, self.rect)
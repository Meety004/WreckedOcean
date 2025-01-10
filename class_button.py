import pygame

class Bouton:
    def __init__(self, x, y, width, height, image):
        # pour mettre le bouttons au centre
        self.x = x - width/2
        self.y = y - height/2
        self.width = width
        self.height = height
        
        original_image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.width, self.height)).convert_alpha()
        self.image = original_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def is_pressed(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if pygame.mouse.get_pressed()[0]:
            if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
                return True
        return False
    
    def affichage(self, screen):
        screen.blit(self.image, self.rect)
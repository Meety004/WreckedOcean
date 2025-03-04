import pygame
import class_button as bouton

class Menu:
    def __init__(self, nb_bouton, texte, image, width, height):
        self.nombre_boutons = nb_bouton
        self.texte_affiche = texte
        self.width = width
        self.height = height
        self.est_actif = True
        
        self.image = pygame.image.load(image).convert_alpha()
        #self.image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()
        #self.rect = self.image.get_rect(center=(width/2, height/2))

    def affichage(self, screen):
        screen.blit(self.image, (-30,0))

    def les_boutons(self, screen_width, screen_height):
        self.liste_boutons = []
        y_start = (screen_height + 50 ) / 2  # Départ centré verticalement
        for i in range(self.nombre_boutons):
            y = y_start + i * 170  # Espacement uniforme de 70 pixels
            if i == 0:
                self.liste_boutons.append(bouton.Bouton(screen_width/2 - 200, y - 225/2, 400, 225, "images/Interfaces/start.png"))
            else:
                self.liste_boutons.append(bouton.Bouton(screen_width/2 - 200, y - 225/2, 400, 225, "images/Interfaces/bouton.png"))

    def actif(self, screen_width, screen_height, screen):
        if self.est_actif:
            self.les_boutons(screen_width, screen_height)
            lst_btn = self.liste_boutons
            
            while self.est_actif:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        pygame.quit()
                        return

                for i, btn in enumerate(lst_btn):
                    if btn.is_pressed():
                        if i == 0:
                            self.est_actif = False

                self.affichage(screen)
                for btn in lst_btn:
                    btn.affichage(screen)

                pygame.display.flip()


    def est_toujours_actif_point_d_interogation(self):
        return self.est_actif
import pygame
import class_button as bouton

class Menu:
    def __init__(self, nb_bouton, texte, image, width, height):
        self.nombre_boutons = nb_bouton
        self.texte_affiche = texte
        self.width = width
        self.height = height
        self.est_actif = True
        
        image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect(center=(width/2, height/2))

    def affichage(self, screen):
        screen.blit(self.image, self.rect)

    def les_boutons(self, screen_width, screen_height):
        self.liste_boutons = []
        y = screen_height - 70*(self.nombre_boutons - 1)/2 # pour ecarter les boutons de 20 centimetre chacun si il y en a plusieur (/2 pour centrer)
        for i in range(self.nombre_boutons):
            self.liste_boutons.append(bouton.Bouton(screen_width/2 - 40, y - 25, 80, 50, "images/bouton.png"))

    def actif(self, screen_width, screen_height, screen):
        if self.est_actif:
            self.les_boutons(screen_width, screen_height)
            lst_btn = self.liste_boutons
            
            while self.est_actif:
                # Gestion des événements (quitter le jeu)
                for event in pygame.event.get():
                    if event.type == pygame.key.get_pressed()[pygame.K_TAB]:
                        pygame.quit()

                for i in range(len(lst_btn)):
                    if lst_btn[i].is_pressed():
                        if i == 0:
                            self.est_actif = False

                self.affichage(screen)
                for btn in lst_btn:
                    btn.affichage(screen)

                pygame.display.flip()

    def est_toujours_actif_point_d_interogation(self):
        return self.est_actif            
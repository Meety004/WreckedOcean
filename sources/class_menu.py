# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM

import pygame, os
import class_button as bouton

class Menu:
    def __init__(self, nb_bouton, image, width, height):
        """ Constructeur de la classe Menu. chaque menu est un objet avec une taille, une image de fond, un nombre de boutons et une variable qui indique si le menu est actif ou non """
        self.nombre_boutons = nb_bouton
        self.width = width
        self.height = height
        self.est_actif = True
        

        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        #self.rect = self.image.get_rect(center=(width/2, height/2))
        self.quitter_jeu = False

    def affichage(self, screen):
        screen.blit(self.image, (0,0))

    def les_boutons(self, screen_width, screen_height):
        # créer les boutons espacé uniformément automatiquement
        self.liste_boutons = []
        y_start = 52.3/100*screen_height  # Départ centré verticalement
        for i in range(self.nombre_boutons):
            y = y_start + i * 15.7/100*screen_height  # Espacement uniforme de 15.7% de la taille de l'ecran
            if i == 0:
                # chaque bouton est un objet de la classe Bouton
                self.liste_boutons.append(bouton.Bouton(screen_width/2 - 10.4/100*screen_width, y - 10.4/100*screen_height, 23.4/100*screen_width, 13.9/100*screen_height, os.path.join("data", "images", "Interfaces", "start.png")))
            else:
                self.liste_boutons.append(bouton.Bouton(screen_width/2 - 10.4/100*screen_width, y - 10.4/100*screen_height, 23.4/100*screen_width, 13.9/100*screen_height, os.path.join("data", "images", "Interfaces", "quitter.png")))

    def actif(self, screen_width, screen_height, screen):
        """ vérifie si le menu est actif et affiche les boutons. elle prend en paramètre la largeur et la hauteur de l'écran et l'écran lui-même et return False si le bouton quitter est pressé et True si le bouton start est pressé """
        if self.est_actif:
            self.les_boutons(screen_width, screen_height)
            lst_btn = self.liste_boutons
            
            while self.est_actif:
                for event in pygame.event.get(): # la premiere touche pour quitter etait tab
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    
                # affiche chaque bouton
                self.affichage(screen)
                for btn in lst_btn:
                    btn.affichage(screen)

                pygame.display.flip()

                # verifie si un bouton est pressé
                for i, btn in enumerate(lst_btn):
                    if btn.is_pressed():
                        if i == 0:
                            self.est_actif = False
                            return True
                        if i == 1:
                            return False

    # je sais pas a quoi ca sert
    def est_toujours_actif_point_d_interogation(self):
        return self.est_actif
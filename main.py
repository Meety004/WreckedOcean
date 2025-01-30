import pygame
from Navire import *
from IA_ennemis import *
from iles import *
import shot as module_shot
import class_menu
from random import randint

# Initialisation de Pygame
pygame.init()
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Définition de la couleur de fond (noir)
BLACK = (0, 0, 0)

class GameState:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()
    
    def reset(self):
        self.liste_joueur = [Navire(7, 0.2, 5, "images/bato_j1.png", self.screen_width, self.screen_height)]
        self.liste_ennemis = [IA_ennemis(5, 0.2, 5, "images/bato.png", self.screen_width, self.screen_height),
                              IA_ennemis(5, 0.2, 5, "images/bato.png", self.screen_width, self.screen_height)]
        self.liste_navire = self.liste_joueur + self.liste_ennemis
        self.liste_iles = [Iles(self.screen_width, self.screen_height, "images/ile_commune.png", 
                                "images/ile_rare.png", "images/ile_mythique.png", 
                                "images/ile_legendaire.png", self.liste_navire)]
        self.liste_shot = []
        self.nbrIles = 1
        self.maxIles = 5
        self.timer = randint(100, 300)

game = GameState(screen_width, screen_height)

# ECRAN TITRE
menu = class_menu.Menu(2, "pas besoin pour l'instant", "images/menu.png", screen_width, screen_width)
menu.actif(screen_width, screen_height, screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pause = class_menu.Menu(2, "pas besoin pour l'instant", "images/menu.png", screen_width, screen_width)
        pause.actif(screen_width, screen_height, screen)
    
    if keys[pygame.K_RETURN]:  # Touche "entrer" pour redémarrer le jeu
        game.reset()

    if len(game.liste_joueur) > 0:
        for navire_i in game.liste_joueur:
            if keys[pygame.K_UP]:
                navire_i.accelerer()
            else:
                navire_i.ralentit()
            if keys[pygame.K_LEFT]:
                navire_i.tourne_gauche()
            if keys[pygame.K_RIGHT]:
                navire_i.tourne_droite()
            if keys[pygame.K_SPACE]:
                tire_du_navire = navire_i.shoot()
                if tire_du_navire is not None:
                    game.liste_shot.extend(tire_du_navire)
            navire_i.avancer()
            navire_i.sortir_ecran(game.screen_width, game.screen_height)
    
    for ennemis in game.liste_ennemis:
        ennemis.bouger(game.liste_navire)
        for adversaire in game.liste_navire:
            if adversaire.get_ID() != ennemis.get_ID():
                tire_ennemi = ennemis.tirer(adversaire.position_x(), adversaire.position_y())
                if tire_ennemi is not None:
                    game.liste_shot.extend(tire_ennemi)
        ennemis.sortir_ecran(game.screen_width, game.screen_height)
    
    for shot_i in game.liste_shot[:]:
        if shot_i is not None:
            shot_i.avancer()
            if shot_i.despawn_distance():
                game.liste_shot.remove(shot_i)
            for i in range(len(game.liste_navire)-1, -1, -1):
                if shot_i.collision(game.liste_navire[i].position_x(), game.liste_navire[i].position_y(), game.liste_navire[i].get_ID()):
                    game.liste_navire[i].get_damaged(10)
                    game.liste_shot.remove(shot_i)
        else:
            game.liste_shot.remove(shot_i)
    
    for navire_i in game.liste_navire[:]:
        if navire_i.is_dead():
            if navire_i in game.liste_joueur:
                game.liste_joueur.remove(navire_i)
            if navire_i in game.liste_ennemis:
                game.liste_ennemis.remove(navire_i)
            game.liste_navire.remove(navire_i)
    
    for ile in game.liste_iles[:]:
        ile.decompte()
        if ile.decompte() <= 0:
            game.liste_iles.remove(ile)
            game.nbrIles -= 1
    
    screen.fill(BLACK)
    ocean = pygame.image.load("images/ocean background.jpg").convert_alpha()
    ocean = pygame.transform.scale(ocean, (screen_width, screen_height)).convert_alpha()
    screen.blit(ocean, (0, 0))
    
    for navire_i in game.liste_navire:
        navire_i.afficher(screen)
    for shot_i in game.liste_shot:
        shot_i.afficher(screen)
    for ile in game.liste_iles:
        ile.afficher(screen)
    
    pygame.display.flip()
    if keys[pygame.K_TAB]:
        running = False
    
    clock.tick(60)

pygame.quit()
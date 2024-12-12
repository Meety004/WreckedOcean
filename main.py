import pygame
from Navire import *
from IA_ennemis import *
import shot as module_shot

# Initialisation de Pygame
pygame.init()
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# listes avec les ennemis et les joueurs (pour l'instant le joueur)
liste_joueur = [Navire(7, 0.2, 5, "images/bato.png", screen_width, screen_height)] #vitesse_max, acceleration, maniabilité, image
liste_ennemis = [IA_ennemis(7, 0.2, 5, "images/bato.png", screen_width, screen_height)]
liste_shot = []

# Définition de la couleur de fond (noir)
BLACK = (0, 0, 0)

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

# Boucle de jeu
while running:



    # UPDATE


    # Gestion des événements (quitter le jeu)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer l'état des touches
    keys = pygame.key.get_pressed()

    # Gestion des touches du premier navire
    for navire_i in liste_joueur:
        if keys[pygame.K_UP]:
            navire_i.accelerer()
        else:
            navire_i.ralentit()

        if keys[pygame.K_LEFT]:
            navire_i.tourne_gauche()

        if keys[pygame.K_RIGHT]:
            navire_i.tourne_droite()
        
        if keys[pygame.K_SPACE]:
            liste_shot.append(navire_i.shoot())

        # Mettre à jour la position des vaisseau
        navire_i.avancer()

        # verifie qu'ils ne sortent pas de l'ecran
        navire_i.sortir_ecran(screen_width, screen_height)
    

    # fait les deplacement de l'ennemi
    
    for ennemis in liste_ennemis:
        ennemis.bouger()
        ennemis.sortir_ecran(screen_width, screen_height)

    for shot_i in liste_shot:
        shot_i.avancer()
        if shot_i.despawn_distance():
            liste_shot.remove(shot_i)

    # Remplir l'écran avec une couleur de fond
    screen.fill(BLACK)



    # DRAW



    # affichage de l'ocean en fond
    ocean = pygame.image.load("images/ocean background.jpg").convert_alpha()
    ocean = pygame.transform.scale(ocean, (screen_width, screen_height)).convert_alpha()
    screen.blit(ocean, (0, 0))

    # Dessine les navires
    for navire_i in liste_joueur:
        navire_i.afficher(screen)
    
        ennemis.afficher(screen)

    # dessine les tires
    for shot_i in liste_shot:
        shot_i.afficher(screen)

    # Rafraîchir l'écran
    pygame.display.flip()
    

    

    # pour quitter le jeux
    if keys[pygame.K_TAB]:
        running = False

    # Limiter la boucle à 60 images par seconde
    clock.tick(60)

# Quitter Pygame proprement
pygame.quit()
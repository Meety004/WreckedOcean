import pygame
from Navire import *
from IA_ennemis import *
from iles import *
import shot as module_shot
import class_menu

# Initialisation de Pygame
pygame.init()
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
playHeight = screen_height -  (1/5 * screen_height)
screen = pygame.display.set_mode((screen_width, screen_height))
print(screen_width, screen_height)

police = pygame.font.Font(None, 36) # gere la police lors de l'affichage de texte a l'ecran

# la bouteille sous la barre de vie
design_barre_de_vie = pygame.transform.scale(pygame.image.load("images/Interfaces/barre_de_vie.png").convert_alpha(), (screen_width*0.09, screen_height*0.265))
design_barre_de_vie = pygame.transform.rotate(design_barre_de_vie, 90)

# Initialisation du delta time pour avoir la même vitesse sur tout les ordis
framerate = 60
clock = pygame.time.Clock()
dt = clock.tick(framerate)

pause = None

keyBindList =  [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_RIGHT
    ]

def start_game():
        # Listes des éléments du jeu
        liste_joueur = [Navire(7, 0.2, 5, "images/Textures/Bateaux/bato_j1.png", screen_width, playHeight, dt)] #vitesse_max, acceleration, maniabilité, image
        liste_ennemis = []
        for i in range(3):
            liste_ennemis.append(IA_ennemis(5, 0.2, 5, "images/Textures/Bateaux/bato.png", screen_width, playHeight, dt))

        # dans linterface utilisateur
        liste_texte_degats = []

        # Liste avec les joueur et les ennemis (contenant donc tout les Navire a l'ecran)
        liste_navire = liste_joueur + liste_ennemis

        # Liste de tuples avec les coordonées des navires.
        liste_coords = []
        # Liste avec les îles
        liste_iles = [Iles(
            screen_width, 
            playHeight,
            "images/Textures/Iles/ile_commune.png", 
            "images/Textures/Iles/ile_rare.png", 
            "images/Textures/Iles/ile_mythique.png", 
            "images/Textures/Iles/ile_legendaire.png",
            liste_navire
            )]

        for i in range(len(liste_navire)):
            coords = ("(", liste_navire[i].position_x(), ",", liste_navire[i].position_y(), ")")
            liste_coords.append(coords)

        # Liste de tout les tirs à l'écran
        liste_shot = []
        
        # Nombre maximal d'îles sur la map
        maxIles = 5

        # Variable contenant le nombre d'îles affichées
        nbrIles = 1

        # Nombre maximul d'îles sur la map
        maxIles = 5

        # On crée un timer d'un nombre de ticks avant la prochaine apparition d'île
        def setTimer():
            timer = randint(100, 300)
            return timer

        #On fait apparaitre des îles sous certaines conditions (timer à 0, 5 îles au total maximum)
        def apparitionIles(nbrIles, maxIles, timer):
            timer -= 1
            if timer <= 0:
                timer = setTimer()
                if nbrIles < maxIles:
                    liste_iles.append(Iles(screen_width, playHeight,"images/Textures/Iles/ile_commune.png","images/Textures/Iles/ile_rare.png","images/Textures/Iles/ile_mythique.png","images/Textures/Iles/ile_legendaire.png",liste_navire))
                    nbrIles += 1
            return nbrIles, maxIles, timer

        #On appelle le timer pour la première fois
        timer = setTimer()

        return liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats

liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats = start_game()

# Définition de la couleur de fond (noir)
BLACK = (0, 0, 0)

# Boucle principale du jeu
running = True

# ECRAN TITRE
menu = class_menu.Menu(2, "pas besoin pour l'instant", "images/Interfaces/menu.png", screen_width, screen_height)
running = menu.actif(screen_width, screen_height, screen)

# Boucle de jeu
while running:
    #menu.actif(screen_width, screen_height, screen)


    # UPDATE

 
    # Gestion des événements (quitter le jeu)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for i in liste_navire:
            i.GererEventTir(event, liste_shot)

    # Récupérer l'état des touches
    keys = pygame.key.get_pressed()

    # Gestion des touches du premier navire (pour l'instant impossible de rajouter d'autre joueurs ils ont tous les même touches)
    if len(liste_joueur) > 0:

        for navire_i in liste_joueur:
            if navire_i.getEquipement()['coque'] == "Coque Trouée":
                keyBindList = res.keyBindCursedList
            else:
                keyBindList = res.keyBindList

            if keys[keyBindList[0]]: # fleche du haut
                navire_i.accelerer()
            else:
                navire_i.ralentit()

            if keys[keyBindList[1]]: # fleche gauche
                navire_i.tourne_gauche()

            if keys[keyBindList[2]]: # fleche droite
                navire_i.tourne_droite()
            
            if keys[pygame.K_SPACE]: # espace
                tir_du_navire = navire_i.shoot()
                if tir_du_navire is not None:
                    liste_shot.extend(tir_du_navire)

            if keys[pygame.K_s]:
                navire_i.use_benediction_1()


            # Mettre à jour la position des navires
            navire_i.avancer()

            # verifie qu'ils ne sortent pas de l'ecran
            navire_i.sortir_ecran(screen_width, playHeight)
    
    for navire in liste_navire: # verifie la rage et l'aura des navires
        navire.still_inraged()
        navire.aura_activated(liste_ennemis)

    # fait les deplacements de l'ennemi
    
    for ennemis in liste_ennemis:
        # a besoin de la position des joueurs pour incliner le deplacement
        ennemis.bouger(liste_navire)
        
        for adversaire in liste_navire:
            if adversaire.get_ID() != ennemis.get_ID():
                # gère le tir de l'ennemi. return None si le joueur n'est pas a porté de l'ennemi
                tir_ennemi = ennemis.tirer(adversaire.position_x(), adversaire.position_y())
                if tir_ennemi != None: # si ça return none alors il l'efface
                    liste_shot.extend(tir_ennemi) # la fonction de tir return une liste. il faut donc extend pour fusionner les liste et pas append

        ennemis.sortir_ecran(screen_width, playHeight)

    for shot_i in reversed(liste_shot):
        if shot_i[0] is not None: # deuxieme verification pour voir si il n'y a pas de None dans les tir car ca casse tout
            shot_i[0].avancer()
            if shot_i[0].despawn_distance():
                liste_shot.remove(shot_i)
            for i in range(len(liste_navire)-1, -1, -1):
                if shot_i[0].collision(liste_navire[i].position_x(), liste_navire[i].position_y(), liste_navire[i].get_ID()):
                    damage = 15
                    if shot_i[1] == "Canon en bronze":
                        damage = 18
                    elif shot_i[1] == "Canon en argent":
                        damage = 20
                    elif shot_i[1] == "Canon en or":
                        damage = 25
                    elif shot_i[1] == "Canon légendaire":
                        damage = 35
                    if not shot_i[0].getIDTireur() == liste_navire[i].get_ID():
                        liste_navire[i].get_damaged(damage)
                        if shot_i[0].is_inraged():
                            liste_navire[i].get_damaged(damage)
                        cible_du_tir = i
                        liste_texte_degats.append([police.render(str(damage), True, (255, 0, 0)), 0])
                        if shot_i[0].is_inraged():
                            liste_texte_degats.append([police.render(str(damage * 2), True, (255, 0, 0)), 0])

                    if shot_i in liste_shot:
                        liste_shot.remove(shot_i)
        else:
            liste_shot.remove(shot_i) # si il y a un None ça le detruit
        
    for navire_i in liste_navire:
        if navire_i.is_dead():
            if len(liste_joueur) > 0:
                for i in range(len(liste_joueur)-1, -1, -1):
                    if liste_joueur[i].get_ID() == navire_i.get_ID():
                        liste_joueur.pop(i)
            if len(liste_ennemis) > 0:
                for i in range(len(liste_ennemis)-1, -1, -1):
                    if liste_ennemis[i].get_ID() == navire_i.get_ID():
                        liste_ennemis.pop(i)
            liste_navire.remove(navire_i)
    if len(liste_joueur) == 0:
        liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats = start_game()
        menu = class_menu.Menu(2, "pas besoin pour l'instant", "images/Interfaces/menu.png", screen_width, screen_height)
        running = menu.actif(screen_width, screen_height, screen)
        continue
            

    # Appelle la méthode de gestion du temps des  îles et les supprime au bout d'un certain temps.
    for ile in liste_iles:
        ile.decompte()
        timeLeft = ile.decompte()
        if timeLeft <= 0:
            liste_iles.remove(ile)
            nbrIles -= 1

        for n in liste_navire:
            if len(liste_navire) > 0:
                recompense = ile.type_recompenses()
                n.equipInterface(recompense, ile.position_x(), ile.position_y())
                if n.afficher_items == True:

                    if keys[pygame.K_a]:
                        if res.calc_distance(liste_joueur[0].position_x(), liste_joueur[0].position_y(), ile.position_x(), ile.position_y()) < 75:
                            if ile in liste_iles:
                                liste_iles.remove(ile)
                                nbrIles -= 1
                        liste_joueur[0].afficher_items = False
                        liste_joueur[0].equiper()
                elif res.calc_distance(n.position_x(), n.position_y(), ile.position_x(), ile.position_y()) < 75:
                    verifIleMalus = n.verifIleMalus
                    if verifIleMalus == True:
                        liste_iles.remove(ile)
                        verifIleMalus = False


    # Appelle de la fonction de compte à rebours pour apparition des îles
    nbrIles, maxIles, timer = apparitionIles(nbrIles, maxIles, timer)



    # DRAW



    #Remplir l'écran avec une couleur de fond
    screen.fill((170, 170, 170))

    # affichage de l'ocean en fond
    ocean = pygame.image.load("images/Backgrounds/ocean background.jpg").convert_alpha()
    ocean = pygame.transform.scale(ocean, (screen_width, (playHeight + (1/34 * screen_height)))).convert_alpha()
    screen.blit(ocean, (0, 0))

    # Dessine les navires
    for navire_i in liste_navire:
        navire_i.afficher(screen)

    # dessine les tirs
    for shot_i in liste_shot:
        shot_i[0].afficher(screen)

    # Dessine les iles
    for ile in liste_iles:
        ile.afficher(screen)

    # dessine l'aura
    for navire_i in liste_navire:
        if navire_i.aura_active():
            pygame.draw.circle(screen, (238, 11, 11), (int(navire_i.position_x()), int(navire_i.position_y())), 150, 4)
            pygame.draw.circle(screen, (207, 8, 8), (int(navire_i.position_x()), int(navire_i.position_y())), 100, 4)

    #Affiche l'interface de choix d'item pour le joueur uniquement
    if liste_joueur[0].afficher_items == True:
        screen.blit(liste_joueur[0].ItemsUI, (15, 15))
        
    # affiche la bare de vie du joueur
    
        # la bouteille
    rect_barre_de_vie = design_barre_de_vie.get_rect(center=(screen_width/2, 7 * screen_height/8))
    screen.blit(design_barre_de_vie, rect_barre_de_vie)
    
        # la bare de vie
    largeur = (screen_width*0.1) * ((liste_joueur[0].get_vie()*(screen_width*0.1) / liste_joueur[0].get_max_vie())/(screen_width*0.1))
    texte = police.render(str(liste_joueur[0].get_vie()), True, (255, 0, 0))
    bare_de_vie = pygame.Rect(screen_width*0.44, screen_height * 0.86, largeur, screen_width*0.02) # affiche a 44% de la largeur et 86% de la hauteur de l'ecran, la largeur est de 0.02% la taille de la hauteur de l'ecran
    pygame.draw.rect(screen, (255, 0, 0), bare_de_vie)
        # le texte pour avoir le nombre de vie exacte
    screen.blit(texte, (screen_width*0.48, screen_height*0.9))

    # affichage des degats lorsque le joueur est touché
    if len(liste_texte_degats) != 0:
        for i in range(len(liste_texte_degats)-1, -1, -1) :
            if cible_du_tir < len(liste_navire):
                screen.blit(liste_texte_degats[i][0], (liste_navire[cible_du_tir].position_x() + 10, liste_navire[cible_du_tir].position_y() - 35))
                liste_texte_degats[i][1] += 1
                if liste_texte_degats[i][1] >= 60:
                    liste_texte_degats.pop(i)
    
    # Rafraîchir l'écran
    pygame.display.flip()


    # pour quitter le jeux
    if keys[pygame.K_TAB]: # si on appuie sur tab ca quitte le jeu
        running = False

    if keys[pygame.K_ESCAPE]:
        menu = class_menu.Menu(2, "pas besoin pour l'instant", "images/Interfaces/menu.png", screen_width, screen_height)
        running = menu.actif(screen_width, screen_height, screen)

    # Limiter la boucle à 60 images par seconde
    dt = clock.tick(framerate) # enfaite non ca marche pas

# Quitter Pygame proprement
pygame.quit()
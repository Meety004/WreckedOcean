# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM

# Importation des librairies et des fichiers dont au aura besoin par la suite
import pygame
import os

from Navire import *
from IA_ennemis import *
from iles import *
from class_menu import *

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre de jeu
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
playHeight = screen_height -  (1/5 * screen_height)
screen = pygame.display.set_mode((screen_width, screen_height))

# Mise à zéro de la variable de pause
pause = None

# Initialisation du framerate pour egaliser la vitesse de jeu sur toutes les machines
framerate = 60
clock = pygame.time.Clock()
dt = clock.tick(framerate)

# Création et chargement de l'image d'arrière-plan
time_last_update = pygame.time.get_ticks()
frames = [] # stockage de chaque image
for i in range(28):
    tempPath = os.path.join("data", "images", "Backgrounds", "Ocean", "")
    temp = pygame.image.load(f"{tempPath}OCEAN_{i+1}.gif").convert_alpha()
    temp = pygame.transform.scale(temp, (screen_width, (playHeight + (1/34 * screen_height)))).convert_alpha()
    frames.append(temp)
current_frame = 1
spriteVY = 3

# Création du chemin du fichier du bateau du joueur
pathBateau = os.path.join("data", "images", "Textures", "Bateaux", "bateau.png")

# Chargement des images d'indication des bénédictions
giga_tir_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "giga_tir.png")), (70, 70)).convert_alpha() 
rage_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "rage.png")), (70, 70)).convert_alpha()
aura_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "aura.png")), (70, 70)).convert_alpha()
god_mode_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "god_mode.png")), (140, 140)).convert_alpha()


# Chargement de l'image de la bouteille sous la barre de vie
design_barre_de_vie = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "Interfaces", "barre_de_vie.png")).convert_alpha(), (screen_width*0.09, screen_height*0.265))
design_barre_de_vie = pygame.transform.rotate(design_barre_de_vie, 90)

# Chargement de l'image de croix des bénédictions
croixBenediction = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "Autres", "croix_bene.png")), (6.55/100*screen_width, 12.7/100*playHeight)).convert_alpha()

# Chargement de la police pour l'affichage des variables du joueur à l'écran
police = pygame.font.Font(None, 36)

# Création des zones de textes affichant l'équipement à l'écran
TypeFontPast = pygame.font.Font(res.fontPixel, 32)
TypeSurfacePast = TypeFontPast.render("Votre équipement actuel:", True, (0, 0, 0))
TypeSurfaceNew = TypeFontPast.render("Ce que vous avez trouvé:", True, (0, 0, 0))

# Création des zones de textes affichant les bénédictions à l'écran
TypeDisplayEquipement = pygame.font.Font(res.fontPixel, 16)
TypeDisplayBenediction = pygame.font.Font(res.fontPixel, 24)
Bene1Surface = TypeDisplayBenediction.render("Bénédiction 1", True, (0, 0, 0))
Bene2Surface = TypeDisplayBenediction.render("Bénédiction 2", True, (0, 0, 0))

# Création d'une liste contenant les touches de déplacement du joueur
keyBindList =  [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_RIGHT
    ]

# Fonction de lancement du jeu, lors que le bouton "START"
def start_game():

    # Liste contenant les joueurs (un seul élément)
    liste_joueur = [Navire(5, 0.1, 4, os.path.join("data", "images", "Textures", "Bateaux", "bateau_j1.png"), screen_width, playHeight, dt, 0)] #vitesse_max, acceleration, maniabilité, image
    
    # Liste contenant les ennemis
    liste_ennemis = []

    # Variable contenant le numéro de la
    niveau = 0

    # Liste contenant les dégats affichés à l'écran
    liste_texte_degats = []

    # Liste avec les joueur et les ennemis (contenant donc tout les navires a l'ecran)
    liste_navire = liste_joueur + liste_ennemis

    # Liste de tuples avec les coordonées des navires.
    liste_coords = []

    # Liste contenant les îles
    liste_iles = [Iles(
        screen_width, 
        playHeight,
        os.path.join("data", "images", "Textures", "Iles", "ile_commune.png"),
        os.path.join("data", "images", "Textures", "Iles", "ile_rare.png"), 
        os.path.join("data", "images", "Textures", "Iles", "ile_mythique.png"), 
        os.path.join("data", "images", "Textures", "Iles", "ile_legendaire.png"),
        liste_navire,
        None,
        niveau
        )]

    # Ajout des coordonées des navires à la liste des coordonées
    for i in range(len(liste_navire)):
        coords = ("(", liste_navire[i].position_x(), ",", liste_navire[i].position_y(), ")")
        liste_coords.append(coords)

    # Liste de tous les tirs affichés à l'écran
    liste_shot = []
    
    # Nombre maximal d'îles sur la map
    maxIles = 5

    # Variable contenant le nombre d'îles affichées
    nbrIles = 1

    # Création d'un timer du nombre de ticks avant la prochaine apparition d'île
    def setTimer():
        timer = randint(100, 300)
        return timer

    #Apparition des îles sous certaines conditions (timer à 0, 5 îles au total maximum)
    def apparitionIles(nbrIles, maxIles, timer):
        timer -= 1
        if len(liste_iles) == 0:
            nbrIles = 0
        if timer <= 0:
            timer = setTimer()
            if nbrIles < maxIles:
                liste_iles.append(Iles(screen_width, playHeight, os.path.join("data", "images", "Textures", "Iles", "ile_commune.png"), os.path.join("data", "images", "Textures", "Iles", "ile_rare.png"), os.path.join("data", "images", "Textures", "Iles", "ile_mythique.png"), os.path.join("data", "images", "Textures", "Iles", "ile_legendaire.png"),liste_navire, liste_iles, niveau))
                nbrIles += 1
        if nbrIles > maxIles:
            nbrIles = maxIles
            
        if nbrIles == 0:
            liste_iles.append(Iles(screen_width, playHeight,os.path.join("data", "images", "Textures", "Iles", "ile_commune.png"), os.path.join("data", "images", "Textures", "Iles", "ile_rare.png"), os.path.join("data", "images", "Textures", "Iles", "ile_mythique.png"), os.path.join("data", "images", "Textures", "Iles", "ile_legendaire.png"),liste_navire, liste_iles, niveau))
            timer = setTimer()
            nbrIles += 1
        return nbrIles, maxIles, timer

    # Appel du timer pour la première fois
    timer = setTimer()

    # Renvoi de toutes les variables pour le reste du jeu
    return liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats, niveau

# Association des variables pour le jeu
liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats, niveau = start_game()

# Définition de la couleur de fond (noir)
BLACK = (0, 0, 0)

# Boucle principale du jeu
running = True

# Création de l'écran titre
menu = Menu(2, os.path.join("data", "images", "Interfaces", "menu.png"), screen_width, screen_height)
running = menu.actif(screen_width, screen_height, screen)

# BOUCLE DE JEU PRINCIPALE
while running:

    # Création du menu de démarrage
    menu.actif(screen_width, screen_height, screen)

    # Gestion des événements pygame
    for event in pygame.event.get():
        
        # On quitte le jeu
        if event.type == pygame.QUIT:
            running = False

        # On appelle une méthode pour gérer le tir double
        for i in liste_navire:
            i.GererEventTir(event, liste_shot)

    # Récupération l'état des touches
    keys = pygame.key.get_pressed()

    # On gère les différentes vagues d'ennemis
    if len(liste_ennemis) == 0:
        if niveau%5 == 0 and niveau != 0:
            for i in range(niveau // 5):
                liste_ennemis.append(IA_ennemis_stage_2(4, 0.1, 4, pathBateau, screen_width, playHeight, dt))
            for i in range((niveau // 10) + 1):
                liste_ennemis.append(IA_ennemis_chasseurs(4, 0.1, 4, pathBateau, screen_width, playHeight, dt))
            for i in range(niveau // 3):
                liste_ennemis.append(IA_ennemis_basiques(4, 0.1, 4, pathBateau, screen_width, playHeight, dt))
        elif niveau%3 == 0 and niveau != 0:
            var_intermediaire = niveau // 3
            if var_intermediaire > 5:
                var_intermediaire = 5
            for i in range(var_intermediaire):
                liste_ennemis.append(IA_ennemis_chasseurs(4, 0.1, 4, pathBateau, screen_width, playHeight, dt))
            for i in range(var_intermediaire//2):
                liste_ennemis.append(IA_ennemis_basiques(4, 0.1, 4, pathBateau, screen_width, playHeight, dt))
        else:
            if niveau > 10:
                niveau = 10
            for i in range(niveau):
                liste_ennemis.append(IA_ennemis_basiques(4, 0.1, 4, pathBateau, screen_width, playHeight, dt))
        for i in range(len(liste_ennemis)):
            liste_navire.append(liste_ennemis[i])
        
        # On donne de la vie au joueur à chaque fin de vague
        liste_joueur[0].heal_par_vague()
        niveau += 1

    # Gestion des touches du joueur
    if len(liste_joueur) > 0:

        # On inverse les contrôles lorsque le joueur a la Coque Trouée
        for navire_i in liste_joueur:
            if navire_i.getEquipement()['coque'] == "Coque Trouée":
                keyBindList = res.keyBindCursedList
            else:
                keyBindList = res.keyBindList

            # On avance avec la flèche du haut
            if keys[keyBindList[0]]:
                navire_i.accelerer()
            else: 
                navire_i.ralentit()

            # On tourne à gauche avec la flèche gauche
            if keys[keyBindList[1]]:
                navire_i.tourne_gauche()

            # On tourne à droite avec la flèche droite
            if keys[keyBindList[2]]:
                navire_i.tourne_droite()
            
            # La barre d'espace fait tirer le bateau
            if keys[pygame.K_SPACE]:
                tir_du_navire = navire_i.shoot()
                if tir_du_navire is not None:
                    liste_shot.extend(tir_du_navire)

            # La touche 1 fait utiliser la bénédiction primaire
            if keys[pygame.K_z] and navire_i.afficher_benediction == False:
                navire_i.use_benediction_1()
            
            # La touche 2 fait utiliser la bénédiction secondaire
            if keys[pygame.K_e] and navire_i.afficher_benediction == False:
                navire_i.use_benediction_2()


            # Mettre à jour la position des navires
            navire_i.avancer()

            # On vérifie que le joueur ne sorte pas de l'écran
            navire_i.sortir_ecran(screen_width, playHeight)


    # On vérifie l'état des bénédictions des navires
    for navire in liste_navire:
        navire.still_inraged()
        navire.aura_activated(liste_ennemis)
        navire.in_godmode()
        navire.still_giga_tir()


    # On gère les actions des ennemis
    for ennemis in liste_ennemis:

        # On fait bouger les ennemis en fonction de la position des îles et celle du joueur
        ennemis.bouger(liste_navire, liste_iles, liste_joueur)
        
        for adversaire in liste_navire:

            # On évite que l'ennemi ne se tire dessus
            if adversaire.get_ID() != ennemis.get_ID():
                
                # Gère le tir de l'annemi
                tir_ennemi = ennemis.tirer(adversaire.position_x(), adversaire.position_y(), liste_joueur)

                # Si un adversaire est à portée, on ajoute le tir à la liste des tirs.
                if tir_ennemi != None:
                    liste_shot.extend(tir_ennemi)

        # On vérifie que les ennemis ne sortent pas de l'écran
        ennemis.sortir_ecran(screen_width, playHeight)

    for shot_i in reversed(liste_shot):
        shot_i[0].sortir_ecran()
        if shot_i[0] is not None: # deuxieme verification pour voir si il n'y a pas de None dans les tir car ca casse tout
            shot_i[0].avancer(liste_navire)
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
                            liste_navire[i].get_damaged(math.floor((damage+1)/2))
                        cible_du_tir = i
                        if not shot_i[0].is_inraged():
                            liste_texte_degats.append([police.render(str(damage), True, (255, 0, 0)), 0])
                        if shot_i[0].is_inraged():
                            liste_texte_degats.append([police.render(str(math.floor((damage+1)*1.5)), True, (255, 0, 0)), 0])                    
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
        liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats, niveau = start_game()
        menu = Menu(2, os.path.join("data", "images", "Interfaces", "menu.png"), screen_width, screen_height)
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
                n.equipInterface(recompense, ile.position_x(), ile.position_y(), ile)
                n.beneInterface(ile.position_x(), ile.position_y(), ile)
                n.verifIleExiste(liste_iles)
                if n.afficher_items == True:

                    if keys[pygame.K_a] or n.type in (1, 3):
                        if res.calc_distance(n.position_x(), n.position_y(), ile.position_x(), ile.position_y()) < 75:
                            if ile in liste_iles:
                                liste_iles.remove(ile)
                                nbrIles -= 1
                            n.afficher_items = False
                            n.equiper()

                if n.afficher_benediction == True:
                        if keys[pygame.K_1] or n.type in (1, 3):
                            if res.calc_distance(n.position_x(), n.position_y(), ile.position_x(), ile.position_y()) < 75:
                                if ile in liste_iles:
                                    liste_iles.remove(ile)
                                    nbrIles -= 1
                                n.afficher_benediction = False
                                n.equiper_benediction(0)

                        if keys[pygame.K_2] or n.type in (1, 3):
                            if res.calc_distance(n.position_x(), n.position_y(), ile.position_x(), ile.position_y()) < 75:
                                if ile in liste_iles:
                                    liste_iles.remove(ile)
                                    nbrIles -= 1
                                n.afficher_benediction = False
                                n.equiper_benediction(1)

                elif res.calc_distance(n.position_x(), n.position_y(), ile.position_x(), ile.position_y()) < 75:
                    verifIleMalus = n.verifIleMalus
                    if verifIleMalus == True:
                        if ile in liste_iles:
                            n.verifIleMalus = False
                            liste_iles.remove(ile)



    # Appelle de la fonction de compte à rebours pour apparition des îles
    nbrIles, maxIles, timer = apparitionIles(nbrIles, maxIles, timer)



    # DRAW


    #Remplir l'écran avec une couleur de fond
    screen.fill((245, 228, 156))

    # affichage de l'ocean en fond
    current_time = pygame.time.get_ticks()
    if current_time - time_last_update > 100:  # Changer de frame toutes les 100 ms
        current_frame = (current_frame + 1) % len(frames)
        image = frames[current_frame]
        time_last_update = current_time
    screen.blit(image, (0, 0))

    # Dessine les navires
    for navire_i in liste_navire:
        if navire_i.godmode_active():
            screen.blit(god_mode_image, god_mode_image.get_rect(center=(navire_i.position_x(), navire_i.position_y())))
        if navire_i.is_giga_tir():
            screen.blit(giga_tir_image, giga_tir_image.get_rect(center=(navire_i.position_x(), navire_i.position_y() - 35)))
        if navire_i.aura_active():
            screen.blit(aura_image, aura_image.get_rect(center=(navire_i.position_x(), navire_i.position_y() + 35)))
        if navire_i.is_inrage():
            screen.blit(rage_image, rage_image.get_rect(center=(navire_i.position_x(), navire_i.position_y() + 35)))
        
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
            pygame.draw.circle(screen, (0, 255, 255), (int(navire_i.position_x()), int(navire_i.position_y())), 150, 4)
        
    # affiche la bare de vie du joueur
    
    # la bouteille
    rect_barre_de_vie = design_barre_de_vie.get_rect(center=(screen_width/2, 7 * screen_height/8))
    screen.blit(design_barre_de_vie, rect_barre_de_vie)
    
    # la bare de vie
    largeur = (screen_width*0.1) * ((liste_joueur[0].get_vie()*(screen_width*0.1) / liste_joueur[0].get_max_vie())/(screen_width*0.1))
    StrVie = str(liste_joueur[0].get_vie()) + " / " + str(liste_joueur[0].get_max_vie())
    texteVie = police.render((StrVie), True, (255, 0, 0))
    bare_de_vie = pygame.Rect(screen_width*0.44, screen_height * 0.86, largeur, screen_width*0.02) # affiche a 44% de la largeur et 86% de la hauteur de l'ecran, la largeur est de 0.02% la taille de la hauteur de l'ecran
    pygame.draw.rect(screen, (255, 0, 0), bare_de_vie)

    # le texte pour avoir le nombre de vie exacte
    screen.blit(texteVie, (screen_width*0.473, screen_height*0.91))


    #Affiche l'équipement actuel du joueur
    (iconCanon, iconVoile, iconCoque) = liste_joueur[0].getImages()

    iconCanon = pygame.transform.scale(iconCanon, (2.616/100*screen_width, 5.072/100*screen_height))
    iconVoile = pygame.transform.scale(iconVoile, (2.616/100*screen_width, 5.072/100*screen_height))
    iconCoque = pygame.transform.scale(iconCoque, (2.616/100*screen_width, 5.072/100*screen_height))
    screen.blit(iconCanon, (0.77*screen_width, 0.829*screen_height))
    screen.blit(iconVoile, (0.77*screen_width, 0.889*screen_height))
    screen.blit(iconCoque, (0.77*screen_width, 0.949*screen_height))

    dictItems = liste_joueur[0].getEquipement()
    TypeSurfaceCanon = TypeFontPast.render(dictItems['canons'], True, (0, 0, 0))
    TypeSurfaceVoile = TypeFontPast.render(dictItems['voile'], True, (0, 0, 0))
    TypeSurfaceCoque = TypeFontPast.render(dictItems['coque'], True, (0, 0, 0))

    screen.blit(TypeSurfaceCanon, (0.80*screen_width, 0.955*screen_height))
    screen.blit(TypeSurfaceVoile, (0.80*screen_width, 0.897*screen_height))
    screen.blit(TypeSurfaceCoque, (0.80*screen_width, 0.837*screen_height))

    #Affiche les bénédictions du joueur
    Bene1 = liste_joueur[0].getBenedictionsImages()[1]
    Bene2 = liste_joueur[0].getBenedictionsImages()[2]
    if Bene1 == None:
        Bene1 = croixBenediction
    if Bene2 == None:
        Bene2 = croixBenediction
    screen.blit(Bene1, (0.050*screen_width, 0.860*screen_height))
    screen.blit(Bene2, (0.170*screen_width, 0.860*screen_height))

    screen.blit(Bene1Surface, (0.050*screen_width, 0.825*screen_height))
    screen.blit(Bene2Surface, (0.170*screen_width, 0.825*screen_height))

    TexteSurfaceBene1 = liste_joueur[0].getBenedictionsTexts()[0]
    TexteSurfaceBene2 = liste_joueur[0].getBenedictionsTexts()[1]

    if TexteSurfaceBene1 == None:
        TexteSurfaceBene1 = "Aucune"
    if TexteSurfaceBene2 == None:
        TexteSurfaceBene2 = "Aucune"

    TexteSurfaceBene1 = TypeDisplayBenediction.render(TexteSurfaceBene1, True, (0, 0, 0))
    TexteSurfaceBene2 = TypeDisplayBenediction.render(TexteSurfaceBene2, True, (0, 0, 0))

    screen.blit(TexteSurfaceBene1, (0.050*screen_width, 0.96*screen_height))
    screen.blit(TexteSurfaceBene2, (0.170*screen_width, 0.96*screen_height))

    # Affiche une croix sur l'icone de bénédiction si celle ci n'est pas utilisable
    if liste_joueur[0].timer_benediction_1 != None:
        if liste_joueur[0].getBenedictionsTexts()[0] == "Bénédiction Santé":
            if not liste_joueur[0].timer_benediction_1.timer_ended_special(liste_joueur[0].timer_sante):
                screen.blit(croixBenediction, (0.05*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[0] == "Bénédiction Dash":
            if not liste_joueur[0].timer_benediction_1.timer_ended_special(liste_joueur[0].timer_dash):
                screen.blit(croixBenediction, (0.05*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[0] == "Bénédiction d'aura":
            if not liste_joueur[0].timer_benediction_1.timer_ended_special(liste_joueur[0].timer_aura):
                screen.blit(croixBenediction, (0.05*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[0] == "Bénédiction de rage":
            if not liste_joueur[0].timer_benediction_1.timer_ended_special(liste_joueur[0].timer_rage):
                screen.blit(croixBenediction, (0.05*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[0] == "Bénédiction GodMode":
            if not liste_joueur[0].timer_benediction_1.timer_ended_special(liste_joueur[0].timer_godmode):
                screen.blit(croixBenediction, (0.05*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[0] == "Bénédiction Projectiles":
            if not liste_joueur[0].timer_benediction_1.timer_ended_special(liste_joueur[0].timer_giga_tir):
                screen.blit(croixBenediction, (0.05*screen_width, 0.860*screen_height))

    # Affiche une croix sur l'icone de bénédiction 2 si celle ci n'est pas utilisable
    if liste_joueur[0].timer_benediction_2 != None:
        if liste_joueur[0].getBenedictionsTexts()[1] == "Bénédiction Santé":
            if not liste_joueur[0].timer_benediction_2.timer_ended_special(liste_joueur[0].timer_sante):
                screen.blit(croixBenediction, (0.175*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[1] == "Bénédiction Dash":
            if not liste_joueur[0].timer_benediction_2.timer_ended_special(liste_joueur[0].timer_dash):
                screen.blit(croixBenediction, (0.175*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[1] == "Bénédiction d'aura":
            if not liste_joueur[0].timer_benediction_2.timer_ended_special(liste_joueur[0].timer_aura):
                screen.blit(croixBenediction, (0.175*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[1] == "Bénédiction de rage":
            if not liste_joueur[0].timer_benediction_2.timer_ended_special(liste_joueur[0].timer_rage):
                screen.blit(croixBenediction, (0.175*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[1] == "Bénédiction GodMode":
            if not liste_joueur[0].timer_benediction_2.timer_ended_special(liste_joueur[0].timer_godmode):
                screen.blit(croixBenediction, (0.175*screen_width, 0.860*screen_height))
        elif liste_joueur[0].getBenedictionsTexts()[1] == "Bénédiction Projectiles":
            if not liste_joueur[0].timer_benediction_2.timer_ended_special(liste_joueur[0].timer_giga_tir):
                screen.blit(croixBenediction, (0.175*screen_width, 0.860*screen_height))


    #Affiche l'interface de choix d'item pour le joueur uniquement
    if liste_joueur[0].afficher_items == True:
        screen.blit(liste_joueur[0].getItemUI(), (0.78/100*screen_width, 1.39/100*screen_height))
        PastIcon = liste_joueur[0].getPastDisplay()
        NewIcon = liste_joueur[0].getNewDisplay()


        screen.blit(PastIcon, (0.071 * screen_width, 0.077 * screen_height))
        screen.blit(NewIcon, (0.071 * screen_width, 0.215 * screen_height))

        PastTextTitle = liste_joueur[0].getTitleTextPast()
        NewTextTitle = liste_joueur[0].getTitleTextNew()
        PastTextDescription = liste_joueur[0].getDescriptionTextPast()
        NewTextDescription = liste_joueur[0].getDescriptionTextNew()


        screen.blit(TypeSurfacePast, (0.158*screen_width, 0.068*screen_height))
        screen.blit(PastTextTitle, (0.158*screen_width, 0.102*screen_height))
        screen.blit(PastTextDescription, (0.159*screen_width, 0.137*screen_height))

        screen.blit(TypeSurfaceNew, (0.158*screen_width, 0.200*screen_height))
        screen.blit(NewTextTitle, (0.158*screen_width, 0.234*screen_height))
        screen.blit(NewTextDescription, (0.159*screen_width, 0.272*screen_height))

    #Affiche l'interface de choix de bénédiction pour le joueur uniquement
    if liste_joueur[0].afficher_benediction == True:
        screen.blit(liste_joueur[0].getBenedictionUI(), (0.78/100*screen_width, 1.39/100*screen_height))
        NewBeneIcon = liste_joueur[0].getBenedictionsImages()[0]
        Bene1Icon = liste_joueur[0].getBenedictionsImages()[1]
        Bene2Icon = liste_joueur[0].getBenedictionsImages()[2]

        if Bene1Icon == None:
            Bene1Icon = croixBenediction
        if Bene2Icon == None:
            Bene2Icon = croixBenediction


        screen.blit(NewBeneIcon, (0.071 * screen_width, 0.215 * screen_height))
        screen.blit(Bene1Icon, (0.090 * screen_width, 0.040* screen_height))
        screen.blit(Bene2Icon, (0.255 * screen_width, 0.040 * screen_height))

        Bene1TextTitle = liste_joueur[0].getBenedictionsTexts()[0]
        Bene2TextTitle = liste_joueur[0].getBenedictionsTexts()[1]
        if Bene1TextTitle == None:
            Bene1TextTitle = "Aucune"
        if Bene2TextTitle == None:
            Bene2TextTitle = "Aucune"
        
        Bene1TextTitle = TypeDisplayBenediction.render(Bene1TextTitle, True, (0, 0, 0))
        Bene2TextTitle = TypeDisplayBenediction.render(Bene2TextTitle, True, (0, 0, 0))

        NewTextTitle = liste_joueur[0].getBenedictionsTexts()[2]
        NewTextDescription = liste_joueur[0].getBenedictionsTexts()[3]

        screen.blit(Bene1TextTitle, (0.098 * screen_width, 0.135* screen_height))
        screen.blit(Bene2TextTitle, (0.268 * screen_width, 0.135 * screen_height))
        screen.blit(NewTextTitle, (0.153 * screen_width, 0.230 * screen_height))
        screen.blit(NewTextDescription, (0.153 * screen_width, 0.265 * screen_height))

    # affiche la vitesse de joueur
    texte_vitesse = police.render("Vitesse Max: " + str(round(liste_joueur[0].get_max_speed(), 1)), True, (25, 128, 212))
    screen.blit(texte_vitesse, (screen_width*0.60, screen_height*0.91))

    # affiche les degats du joueur
    if liste_joueur[0].getEquipement()["canons"] == "Canon en bronze":
        texte_degats = police.render("Dégats: 18", True, (179, 0, 0))
    elif liste_joueur[0].getEquipement()["canons"] == "Canon en argent":
        texte_degats = police.render("Dégats: 20", True, (179, 0, 0))
    elif liste_joueur[0].getEquipement()["canons"] == "Canon en or":
        texte_degats = police.render("Dégats: 25", True, (179, 0, 0))
    elif liste_joueur[0].getEquipement()["canons"] == "Canon légendaire":
        texte_degats = police.render("Dégats: 35", True, (179, 0, 0))
    else:
        texte_degats = police.render("Dégats: 15", True, (179, 0, 0))
    screen.blit(texte_degats, (screen_width*0.60, screen_height*0.88))

    # affiche la cadence de tir du joueur
    cadence_rounded = round(1000/liste_joueur[0].get_cadence_tir(), 1)
    texte_cadence = police.render("Cadence: " + str(cadence_rounded) + "tirs/s" , True, (179, 0, 0))
    screen.blit(texte_cadence, (screen_width*0.60, screen_height*0.85))

    # Affiche la vague actuelle:
    if len(liste_ennemis) <= 1:
        textEnnemis = str(len(liste_ennemis)) +  " ennemi restant"
    else:
        textEnnemis = str(len(liste_ennemis)) +  " ennemis restants"
    
    textVague = police.render(("Vague: " + str(niveau-1)), True, (0, 0, 0))
    textEnnemis = police.render(textEnnemis, True, (0, 0, 0))

    screen.blit(textVague, (screen_width*0.45, screen_height*0.945))
    screen.blit(textEnnemis, (screen_width*0.45, screen_height*0.968))


    # affichage des degats lorsque le joueur est touché
    if len(liste_texte_degats) != 0:
        for i in range(len(liste_texte_degats)-1, -1, -1) :
            if cible_du_tir < len(liste_navire):
                if not liste_navire[cible_du_tir].godmode_active():
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
        menu = Menu(2,os.path.join("data", "images", "Interfaces", "menu.png"), screen_width, screen_height)
        running = menu.actif(screen_width, screen_height, screen)

    # Limiter la boucle à 60 images par seconde
    dt = clock.tick(framerate) # en fait non ca marche pas

# Quitter Pygame proprement
pygame.quit()
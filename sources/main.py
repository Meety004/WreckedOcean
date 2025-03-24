import pygame
from Navire import *
from IA_ennemis import *
from iles import *
import os
import class_menu

# Initialisation de Pygame
pygame.init()
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
playHeight = screen_height -  (1/5 * screen_height)
screen = pygame.display.set_mode((screen_width, screen_height))

pause = None

# Initialisation du delta time pour avoir la même vitesse sur tout les ordis
framerate = 60
clock = pygame.time.Clock()
dt = clock.tick(framerate)

#bg
ocean = pygame.image.load(os.path.join("data", "images", "Backgrounds", "ocean_background.jpg")).convert_alpha()
ocean = pygame.transform.scale(ocean, (screen_width, (playHeight + (1/34 * screen_height)))).convert_alpha()

pathBateau = os.path.join("data", "images", "Textures", "Bateaux", "bateau.png")

# chargment de l'image avec un giga tir
giga_tir_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "giga_tir.png")), (70, 70)).convert_alpha() 
rage_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "rage.png")), (70, 70)).convert_alpha()
aura_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "aura.png")), (70, 70)).convert_alpha()
god_mode_image = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "BenedictionsPlay", "god_mode.png")), (140, 140)).convert_alpha()


# la bouteille sous la barre de vie
design_barre_de_vie = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "Interfaces", "barre_de_vie.png")).convert_alpha(), (screen_width*0.09, screen_height*0.265))
design_barre_de_vie = pygame.transform.rotate(design_barre_de_vie, 90)

#Croix des bénédictions
croixBenediction = pygame.transform.scale(pygame.image.load(os.path.join("data", "images", "icons", "Autres", "croix_bene.png")), (6.55/100*screen_width, 12.7/100*playHeight)).convert_alpha()

police = pygame.font.Font(None, 36) # gere la police lors de l'affichage de texte a l'ecran

TypeFontPast = pygame.font.Font(res.fontPixel, 32)
TypeSurfacePast = TypeFontPast.render("Votre équipement actuel:", True, (0, 0, 0))
TypeSurfaceNew = TypeFontPast.render("Ce que vous avez trouvé:", True, (0, 0, 0))

TypeDisplayEquipement = pygame.font.Font(res.fontPixel, 16)
TypeDisplayBenediction = pygame.font.Font(res.fontPixel, 24)

Bene1Surface = TypeDisplayBenediction.render("Bénédiction 1", True, (0, 0, 0))
Bene2Surface = TypeDisplayBenediction.render("Bénédiction 2", True, (0, 0, 0))


keyBindList =  [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_RIGHT
    ]

def start_game():
        # Listes des éléments du jeu
        liste_joueur = [Navire(5, 0.1, 4, os.path.join("data", "images", "Textures", "Bateaux", "bateau_j1.png"), screen_width, playHeight, dt, 0)] #vitesse_max, acceleration, maniabilité, image
        liste_ennemis = []
        niveau = 0

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
            os.path.join("data", "images", "Textures", "Iles", "ile_commune.png"),
            os.path.join("data", "images", "Textures", "Iles", "ile_rare.png"), 
            os.path.join("data", "images", "Textures", "Iles", "ile_mythique.png"), 
            os.path.join("data", "images", "Textures", "Iles", "ile_legendaire.png"),
            liste_navire,
            None
            )]

        for i in range(len(liste_navire)):
            coords = ("(", liste_navire[i].position_x(), ",", liste_navire[i].position_y(), ")")
            liste_coords.append(coords)

        # Liste de tout les tirs à l'écran
        liste_shot = []
        
        # Nombre maximal d'îles sur la map
        maxIles = 7

        # Variable contenant le nombre d'îles affichées
        nbrIles = 1

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
                    liste_iles.append(Iles(screen_width, playHeight, os.path.join("data", "images", "Textures", "Iles", "ile_commune.png"), os.path.join("data", "images", "Textures", "Iles", "ile_rare.png"), os.path.join("data", "images", "Textures", "Iles", "ile_mythique.png"), os.path.join("data", "images", "Textures", "Iles", "ile_legendaire.png"),liste_navire, liste_iles))
                    nbrIles += 1
            if nbrIles > maxIles:
                nbrIles = maxIles
                
            if nbrIles == 0:
                liste_iles.append(Iles(screen_width, playHeight,os.path.join("data", "images", "Textures", "Iles", "ile_commune.png"), os.path.join("data", "images", "Textures", "Iles", "ile_rare.png"), os.path.join("data", "images", "Textures", "Iles", "ile_mythique.png"), os.path.join("data", "images", "Textures", "Iles", "ile_legendaire.png"),liste_navire, liste_iles))
                timer = setTimer()
                nbrIles += 1
            return nbrIles, maxIles, timer

        #On appelle le timer pour la première fois
        timer = setTimer()

        return liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats, niveau

liste_joueur, liste_ennemis, liste_navire, liste_coords, liste_iles, liste_shot, nbrIles, maxIles, setTimer, apparitionIles, timer, liste_texte_degats, niveau = start_game()

# Définition de la couleur de fond (noir)
BLACK = (0, 0, 0)

# Boucle principale du jeu
running = True

# ECRAN TITRE
menu = class_menu.Menu(2, os.path.join("data", "images", "Interfaces", "menu.png"), screen_width, screen_height)
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

    #différentes wave d'ennemis
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
        
        liste_joueur[0].heal_par_vague()
        niveau += 1

    # Gestion des touches du premier navire (pour l'instant impossible de rajouter d'autre joueurs ils ont tous les mêmes touches)
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

            if keys[pygame.K_z] and navire_i.afficher_benediction == False:
                navire_i.use_benediction_1()
            
            if keys[pygame.K_e] and navire_i.afficher_benediction == False:
                navire_i.use_benediction_2()


            # Mettre à jour la position des navires
            navire_i.avancer()

            # verifie qu'ils ne sortent pas de l'ecran
            navire_i.sortir_ecran(screen_width, playHeight)


    
    for navire in liste_navire: # verifie la rage, l'aura et le godmode des navires
        navire.still_inraged()
        navire.aura_activated(liste_ennemis)
        navire.in_godmode()
        navire.still_giga_tir()

    # fait les deplacements de l'ennemi
    
    for ennemis in liste_ennemis:
        # a besoin de la position des joueurs pour incliner le deplacement
        ennemis.bouger(liste_navire, liste_iles, liste_joueur)
        
        for adversaire in liste_navire:
            if adversaire.get_ID() != ennemis.get_ID():
                # gère le tir de l'ennemi. return None si le joueur n'est pas a porté de l'ennemi
                tir_ennemi = ennemis.tirer(adversaire.position_x(), adversaire.position_y(), liste_joueur)
                if tir_ennemi != None: # si ça return none alors il l'efface
                    liste_shot.extend(tir_ennemi) # la fonction de tir return une liste. il faut donc extend pour fusionner les liste et pas append

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
        menu = class_menu.Menu(2, os.path.join("data", "images", "Interfaces", "menu.png"), screen_width, screen_height)
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
                            liste_iles.remove(ile)
                            verifIleMalus = False


    # Appelle de la fonction de compte à rebours pour apparition des îles
    nbrIles, maxIles, timer = apparitionIles(nbrIles, maxIles, timer)



    # DRAW


    #Remplir l'écran avec une couleur de fond
    screen.fill((245, 228, 156))

    # affichage de l'ocean en fond
    screen.blit(ocean, (0, 0))

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
    screen.blit(iconCanon, (0.79*screen_width, 0.829*screen_height))
    screen.blit(iconVoile, (0.79*screen_width, 0.889*screen_height))
    screen.blit(iconCoque, (0.79*screen_width, 0.949*screen_height))

    dictItems = liste_joueur[0].getEquipement()
    TypeSurfaceCanon = TypeFontPast.render(dictItems['canons'], True, (0, 0, 0))
    TypeSurfaceVoile = TypeFontPast.render(dictItems['voile'], True, (0, 0, 0))
    TypeSurfaceCoque = TypeFontPast.render(dictItems['coque'], True, (0, 0, 0))

    screen.blit(TypeSurfaceCanon, (0.82*screen_width, 0.955*screen_height))
    screen.blit(TypeSurfaceVoile, (0.82*screen_width, 0.897*screen_height))
    screen.blit(TypeSurfaceCoque, (0.82*screen_width, 0.837*screen_height))

    #Affiche les bénédictions du joueur
    Bene1 = liste_joueur[0].getBenedictionsImages()[1]
    Bene2 = liste_joueur[0].getBenedictionsImages()[2]
    if Bene1 == None:
        Bene1 = croixBenediction
    if Bene2 == None:
        Bene2 = croixBenediction
    screen.blit(Bene1, (0.05*screen_width, 0.860*screen_height))
    screen.blit(Bene2, (0.175*screen_width, 0.860*screen_height))

    screen.blit(Bene1Surface, (0.055*screen_width, 0.825*screen_height))
    screen.blit(Bene2Surface, (0.180*screen_width, 0.825*screen_height))

    TexteSurfaceBene1 = liste_joueur[0].getBenedictionsTexts()[0]
    TexteSurfaceBene2 = liste_joueur[0].getBenedictionsTexts()[1]

    if TexteSurfaceBene1 == None:#not in res.liste_benedictions:
        TexteSurfaceBene1 = "Aucune"
    if TexteSurfaceBene2 == None:#not in res.liste_benedictions:
        TexteSurfaceBene2 = "Aucune"

    TexteSurfaceBene1 = TypeDisplayBenediction.render(TexteSurfaceBene1, True, (0, 0, 0))
    TexteSurfaceBene2 = TypeDisplayBenediction.render(TexteSurfaceBene2, True, (0, 0, 0))

    screen.blit(TexteSurfaceBene1, (0.060*screen_width, 0.96*screen_height))
    screen.blit(TexteSurfaceBene2, (0.185*screen_width, 0.96*screen_height))


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

        screen.blit(Bene1TextTitle, (0.105 * screen_width, 0.14* screen_height))
        screen.blit(Bene2TextTitle, (0.275 * screen_width, 0.14 * screen_height))
        screen.blit(NewTextTitle, (0.153 * screen_width, 0.230 * screen_height))
        screen.blit(NewTextDescription, (0.153 * screen_width, 0.265 * screen_height))

    # affiche la vitesse de joueur
    texte_vitesse = police.render("Vitesse Max : " + str(round(liste_joueur[0].get_max_speed(), 1)), True, (25, 128, 212))
    screen.blit(texte_vitesse, (screen_width*0.44, screen_height*0.95))

    # affiche les degats du joueur
    if liste_joueur[0].getEquipement()["canons"] == "Canon en bronze":
        texte_degats = police.render("Dégats : 18", True, (179, 0, 0))
    elif liste_joueur[0].getEquipement()["canons"] == "Canon en argent":
        texte_degats = police.render("Dégats : 20", True, (179, 0, 0))
    elif liste_joueur[0].getEquipement()["canons"] == "Canon en or":
        texte_degats = police.render("Dégats : 25", True, (179, 0, 0))
    elif liste_joueur[0].getEquipement()["canons"] == "Canon légendaire":
        texte_degats = police.render("Dégats : 35", True, (179, 0, 0))
    else:
        texte_degats = police.render("Dégats : 15", True, (179, 0, 0))
    screen.blit(texte_degats, (screen_width*0.34, screen_height*0.90))

    # affiche la cadence de tir du joueur
    cadence_rounded = round(1000/liste_joueur[0].get_cadence_tir(), 1)
    texte_cadence = police.render("Cadence : " + str(cadence_rounded) + "tirs/s" , True, (179, 0, 0))
    screen.blit(texte_cadence, (screen_width*0.55, screen_height*0.90))


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
        menu = class_menu.Menu(2,os.path.join("data", "images", "Interfaces", "menu.png"), screen_width, screen_height)
        running = menu.actif(screen_width, screen_height, screen)

    # Limiter la boucle à 60 images par seconde
    dt = clock.tick(framerate) # en fait non ca marche pas

# Quitter Pygame proprement
pygame.quit()
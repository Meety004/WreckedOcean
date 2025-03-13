# IMPORTS

import math
import pygame
import random
import shot
import string
import ressources as res

# On crée un évènement pour le tir double
tirDouble = pygame.USEREVENT + 1

class Navire:
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt):

        # Propriétés du vaisseau
        self.vitesse_max = v_max
        self.acceleration = acceleration
        self.x = random.randint(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.vitesse = 0
        self.angle = 270
        self.maniabilite = maniabilite # Vitesse de rotation du bateau
        self.width = 40
        self.height = 60

        self.screen_width = screen_width
        self.screen_height = screen_height

        #On charge et adapte la taille des images des bateaux
        original_image = pygame.image.load(image).convert_alpha()
        original_image = pygame.transform.scale(original_image, (self.width, self.height)).convert_alpha()
        self.image = original_image  # Image qui sera affichée
        self.dernier_tire = 0 # Le denier tir fait par le bateau
        self.cadance_tire = 1000 # Durée minimale entre deux tirs
        self.ID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.maxVie = 100
        self.vie = self.maxVie

        #On vérifie si l'île contient un malus
        self.verifIleMalus = False

        self.afficher_items = False  # Variable d'état pour suivre l'affichage de l'image

        #On charge l'image de l'interface de choix d'item
        self.ItemsUI = pygame.image.load("images/Interfaces/equip_menu_item.png").convert_alpha()
        self.ItemsUI = pygame.transform.scale(self.ItemsUI, (screen_width*0.4, pygame.display.Info().current_h*0.4)).convert_alpha()

        #On crée un dictionnaire qui contient l'équipement du bateau
        self.equipement = {
        'canons':   "Canon de base",
        'voile':    "Voile de base",
        'coque':    "Coque de base"
        }

        #On crée une liste qui contient les bénédictions du bateau
        self.benedictions = []

        #Stocke la récompense de l'île
        self.recompense = None

        #Variables qui contiennent les modificateurs de vie et de vitesse des coques et des voiles
        self.CoqueMaxVie = 0
        self.CoqueMaxVitesse = 1
        self.VoileMaxVie = 0
        self.VoileMaxVitesse = 1

        #Variables qui contiennent les chemins des icones pour chaque type d'équipement
        self.iconCoque = res.CoqueCommun
        self.iconVoile = res.VoileCommun
        self.iconCanon = res.CanonCommun

        #Variables qui contiennent les chemins des icones s'affichant sur l'interface de choix d'item
        self.DisplayIconNew = None
        self.DisplayIconPast = None

        self.image_loaded = False

        self.ile_actuelle = None  # Stocke l'île qui a ouvert l'interface

        self.TitleTextPast = None
        self.DescriptionTextPast = None

        self.TitleTextNew = None
        self.DescriptionTextNew = None

        self.TitleFont = pygame.font.Font(res.fontPixel, 28)
        self.DescriptionFont = pygame.font.Font(res.fontPixel, 20)

        self.text_loaded = False

        self.type= None





    # Le bateau avance en fonction de la vitesse, immobile si la vitesse est nulle
    def avancer(self):
        self.x += self.vitesse * math.cos(math.radians(self.angle - 90))
        self.y += self.vitesse * math.sin(math.radians(self.angle - 90))

    # Augmente la vitessse
    def accelerer(self):

        # Accelere tant que la vitesse max n'est pas atteinte
        if self.vitesse < self.vitesse_max:
            self.vitesse += self.acceleration
            
        # Si la vitesse max est atteinte il revient à la vitesse max
        if self.vitesse > self.vitesse_max:
            self.vitesse = self.vitesse_max

    #Si il arrete d'avancer le bateau décelère
    def ralentit(self):

        # Ralentit tant que la vitesse n'est pas nulle
        if self.vitesse > 0:
            self.vitesse -= ( 0.3 - self.vitesse_max/100)

        # Revient à 0 si la vitesse est négative
        if self.vitesse < 0:
            self.vitesse = 0

    def tourne_gauche(self):
        if self.vitesse > 0:
            self.angle -= self.maniabilite
            # Si l'angle est inférieur à 0, on lui rajoute 360 pour qu'il reste toujours entre 0 et 360
            if self.angle < 0:
                self.angle += 360

    def tourne_droite(self):
        if self.vitesse > 0:
            self.angle += self.maniabilite
            # Si l'angle est superieur à 360, on lui enlève 360 pour qu'il reste toujours entre 0 et 360
            if self.angle >= 360:
                self.angle -= 360

    # Pour que le bateau ne sorte pas de l'ecran et revienne de l'autre côté
    def sortir_ecran(self, largeur_ecran, longueur_ecran):
        if self.x > largeur_ecran:
            self.x = 0
        if self.x < 0:
            self.x = largeur_ecran
        if self.y > longueur_ecran:
            self.y = 0
        if self.y < 0:
            self.y = longueur_ecran

    def afficher(self, screen):
        # Appliquer la rotation à l'image d'origine sans la modifier définitivement
        rotated_image = pygame.transform.rotate(self.image, -self.angle).convert_alpha()
        rect = rotated_image.get_rect(center=(self.x, self.y))
        self.rect = rect
        screen.blit(rotated_image, self.rect)

    def shoot(self):
        # Vérifie si le tir à rechargé
        if pygame.time.get_ticks() - self.dernier_tire >= self.cadance_tire:
            self.dernier_tire = pygame.time.get_ticks()

            # 
            liste_tirs = []

            tir_droite = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
            liste_tirs.append((tir_droite, self.equipement['canons']))

            tir_gauche = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
            liste_tirs.append((tir_gauche, self.equipement['canons']))

            if self.equipement['canons'] == '+1 Canon' or self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_avant = shot.Shot(self.x, self.y, self.angle, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
                liste_tirs.append((tir_avant, self.equipement['canons']))

            if self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_arriere = shot.Shot(self.x, self.y, self.angle + 180, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
                liste_tirs.append((tir_arriere, self.equipement['canons']))

            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_diag1 = shot.Shot(self.x, self.y, self.angle + 30, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
                liste_tirs.append((tir_diag1, self.equipement['canons']))

            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_diag2 = shot.Shot(self.x, self.y, self.angle - 30, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
                liste_tirs.append((tir_diag2, self.equipement['canons']))

            if self.equipement['canons'] == "Canon à tirs doubles":     
                pygame.time.set_timer(tirDouble, 50, loops=1)

            return liste_tirs
        
    def GererEventTir(self, event, liste_tirs):
        if event.type == tirDouble:
            tir_droiteD = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
            liste_tirs.append((tir_droiteD, self.equipement['canons']))

            tir_gaucheD = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'])
            liste_tirs.append((tir_gaucheD, self.equipement['canons']))

        
    def get_damaged(self, damage):
        r = 5
        if self.equipement['coque'] == "Coque en bois magique":
            r = random.randint(1,5)
        if r != 1:
            self.vie -= damage
    
    def is_dead(self):
        if self.vie <= 0:
            return True
        return False

    # return pour return les caracteristique du bateau
    def position_x(self):
        return self.x
    def position_y(self):
        return self.y
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_angle(self):
        return self.angle
    def get_ID(self):
        return self.ID
    def get_rect(self):
        return self.rect
    
    def getEquipement(self):
        return self.equipement
    
    def getPastDisplay(self):
        return self.DisplayIconPast
     
    def getNewDisplay(self):
        return self.DisplayIconNew
    
    def getItemUI(self):
        return self.ItemsUI
    
    def getTitleTextPast(self):
        return self.TitleTextPast
    
    def getDescriptionTextPast(self):
        return self.DescriptionTextPast
    
    def getTitleTextNew(self):
        return self.TitleTextNew
    
    def getDescriptionTextNew(self):
        return self.DescriptionTextNew
    
    def LoadImage(self):
        if not isinstance(self.DisplayIconPast, pygame.Surface):
            print(self.DisplayIconPast)
            self.DisplayIconPast = pygame.image.load(self.DisplayIconPast).convert_alpha()
            self.DisplayIconPast = pygame.transform.scale(self.DisplayIconPast, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        if not isinstance(self.DisplayIconNew, pygame.Surface):
            print(self.DisplayIconNew)
            self.DisplayIconNew = pygame.image.load(self.DisplayIconNew).convert_alpha()
            self.DisplayIconNew = pygame.transform.scale(self.DisplayIconNew, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

    def LoadText(self):
        if not isinstance(self.TitleTextPast, pygame.Surface):
            self.TitleTextPast = self.TitleFont.render(self.equipement[self.type], True, (0, 0, 0))  # Noir
        if not isinstance(self.DescriptionTextPast, pygame.Surface):
            equip = self.equipement[self.type]
            self.DescriptionTextPast = self.DescriptionFont.render(res.dictItemsBuff[equip], True, (0, 0, 0))

        if not isinstance(self.TitleTextNew, pygame.Surface):
            self.TitleTextNew = self.TitleFont.render(self.recompense[0], True, (0, 0, 0))  # Noir
        if not isinstance(self.DescriptionTextNew, pygame.Surface):
            equip = self.recompense[0]
            self.DescriptionTextNew = self.DescriptionFont.render(res.dictItemsBuff[equip], True, (0, 0, 0))

    def verifIleExiste(self, liste_iles):
        if (self.ile_actuelle is not None) and (self.ile_actuelle not in liste_iles):
            self.afficher_items = False
            self.image_loaded = False
            self.text_loaded = False
            self.ile_actuelle = None



    def equipInterface(self, recompense, xIle, yIle, ile):
        self.recompense = recompense
        if self.recompense[0] in res.listeCanons:
            self.type = "canons"
        elif self.recompense[0] in res.listeVoiles:
            self.type = "voile"
        elif self.recompense[0] in res.listeCoques:
            self.type = "coque"

        # Si la récompense est un objet
        if (self.recompense[0] not in res.liste_benedictions) and (self.recompense[0] not in res.liste_malus):

            # On vérifie sa distance à l'île
            if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:

                # Si l'interface n'est pas affichée, ou si on s'approche d'une nouvelle île
                if not self.afficher_items or self.ile_actuelle is None:

                    if self.ile_actuelle != ile:
                        self.afficher_items = False
                        self.image_loaded = False
                        self.text_loaded = False
                        self.TitleTextPast = None
                        self.DescriptionTextPast = None
                        self.TitleTextNew = None
                        self.DescriptionTextNew = None
                        self.ile_actuelle = ile

                    self.updateDisplayIcon()
                    self.LoadImage()
                    self.LoadText()
                    self.image_loaded = True
                    self.text_loaded = True
                    self.ile_actuelle = ile  # On mémorise l'île qui a ouvert l'interface

                self.afficher_items = True

            # Si le joueur s'éloigne de l'île qui a affiché l'interface, on ferme
            elif self.ile_actuelle == ile:
                self.afficher_items = False
                self.image_loaded = False
                self.text_loaded = False
                self.ile_actuelle = None  # On oublie l'île actuelle

        else:
            self.afficher_items = False
            if self.recompense[0] in res.liste_malus and res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
                self.equiper()
                self.updateDisplayIcon()
                self.verifIleMalus = True


        
    def updateDisplayIcon(self): 
        print(f"Début Update {self.DisplayIconPast}, {self.DisplayIconNew}, {self.recompense}")
        if self.recompense[0] in res.listeCanons:
            self.DisplayIconPast = self.iconCanon
            if self.recompense[1] == "commun":
                self.DisplayIconNew = res.CanonCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = res.CanonRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = res.CanonMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = res.CanonLegendaire
        elif self.recompense[0] in res.listeCoques:
            self.DisplayIconPast = self.iconCoque
            if self.recompense[1] == "commun":
                self.DisplayIconNew = res.CoqueCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = res.CoqueRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = res.CoqueMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = res.CoqueLegendaire
        elif self.recompense[0] in res.listeVoiles:
            self.DisplayIconPast = self.iconVoile
            if self.recompense[1] == "commun":
                self.DisplayIconNew = res.VoileCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = res.VoileRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = res.VoileMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = res.VoileLegendaire
        elif self.recompense[0] in res.liste_malus:
            if self.recompense[0] == res.liste_malus[0]:
                self.DisplayIconNew = res.CanonCommun
            elif self.recompense[0] == res.liste_malus[1]:
                self.DisplayIconNew = res.VoileCommun
            elif self.recompense[0] == res.liste_malus[2]:
                self.DisplayIconNew = res.CoqueCommun
        print(f"Fin Update {self.DisplayIconPast}, {self.DisplayIconNew}, {self.recompense}")





    def equiper(self):
        # Mettre à jour l'équipement en fonction de la récompense
        if self.recompense[0] in res.listeCanons or self.recompense[0] == res.liste_malus[0]:
            self.equipement['canons'] = self.recompense[0]
        elif self.recompense[0] in res.listeVoiles or self.recompense[0] == res.liste_malus[1]:
            self.equipement['voile'] = self.recompense[0]
        elif self.recompense[0] in res.listeCoques or self.recompense[0] == res.liste_malus[2]:
            self.equipement['coque'] = self.recompense[0]
        print(self.equipement)
        self.effetItem()
        self.updateDisplayIcon()


    def effetItem(self):
        self.maxVie = 50
        self.vitesse_max = 7
        self.maniabilite = 5

        if self.recompense[0] in res.listeCoques:
            self.iconCoque = self.DisplayIconNew
            self.CoqueMaxVie = 0
            self.CoqueMaxVitesse = 1
            if self.equipement['coque'] == "Coque épicéa":
                self.CoqueMaxVie += 10
                self.vie += 10
            elif self.equipement['coque'] == "Coque en bouleau":
                self.CoqueMaxVie += 10
                self.vie += 10
                self.CoqueMaxVitesse = 1.05
            elif self.equipement['coque'] == "Coque en chêne massif":
                self.CoqueMaxVie += 75
                self.vie += 75
                self.CoqueMaxVitesse = 0.75
            elif self.equipement['coque'] == "Coque chêne":
                self.CoqueMaxVitesse = 1.05
            elif self.equipement['coque'] == "Coque en bois magique":
                self.CoqueMaxVie += 50
                self.vie += 50
                self.CoqueMaxVitesse = 1.2
            elif self.equipement['coque'] == "Coque légendaire":
                self.CoqueMaxVie += 60
                self.vie += 60
                self.CoqueMaxVitesse = 1.3

        if self.recompense[0] in res.listeVoiles:
            self.iconVoile = self.DisplayIconNew
            self.VoileMaxVitesse = 1
            self.VoileMaxVie = 0
            if self.equipement['voile'] == "Voile en toile de jute":
                self.VoileMaxVitesse = 1.05
            elif self.equipement['voile'] == "Voile Latine":
                self.VoileMaxVitesse = 1.1
            elif self.equipement['voile'] == "Voile Enchantée":
                self.VoileMaxVitesse = 1.25
                self.maniabilite = self.maniabilite * 1.02
            elif self.equipement['voile'] == "Voile légendaire":
                self.VoileMaxVitesse = 1.3
                self.maniabilite = self.maniabilite * 1.05

        if self.recompense[0] in res.listeCanons:
            self.iconCanon = self.DisplayIconNew
            if (self.equipement['canons'] == "Canon en or") or (self.equipement['canons'] == "Canon légendaire"):
                self.cadance_tir = 900

        if self.recompense[0] in res.liste_malus:
            if self.equipement['voile'] == "Voile Trouée":
                self.VoileMaxVitesse = 0.5

        self.maxVie = self.maxVie + self.VoileMaxVie + self.CoqueMaxVie
        self.vitesse_max = self.vitesse_max * self.VoileMaxVitesse * self.CoqueMaxVitesse
# Projet: WRECKED OCEAN
# Auteurs: BELLEC-ESCALERA Elliot, CADEAU--FLAUJAT Gabriel, KELEMEN Thomas, GABRIEL TOM


# IMPORTS

import math
import pygame
import random
import shot
import string
import os
import ressources as res

# On crée un évènement pour le tir double
tirDouble = pygame.USEREVENT + 1

class Navire:
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt, type):
        # Contrôle du vaisseau
        self.vitesse_max = v_max
        self.acceleration = acceleration
        self.x = random.randint(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.vitesse = 0
        self.angle = 270
        self.maniabilite = maniabilite # Vitesse de rotation du bateau
        self.width = screen_width*0.022
        self.height = screen_height*0.062

        self.screen_width = screen_width
        self.screen_height = screen_height

        #On charge et adapte la taille des images des bateaux
        original_image = pygame.image.load(image).convert_alpha()
        original_image = pygame.transform.scale(original_image, (self.width, self.height)).convert_alpha()

        self.image = original_image  # Image qui sera affichée
        self.dernier_tir = 0 # Le denier tir fait par le bateau
        self.cadence_tir = 1000 # Durée minimale entre deux tirs
        self.ID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.maxVie = 50
        self.vie = self.maxVie

        #On vérifie si l'île contient un malus
        self.verifIleMalus = False
        self.type = type

        self.afficher_items = False  # Variable d'état pour suivre l'affichage de l'image

        self.afficher_benediction = False

        #On charge l'image de l'interface de choix d'item
        self.ItemsUI = pygame.image.load(os.path.join("data", "images", "Interfaces", "equip_menu_item.png")).convert_alpha()
        self.ItemsUI = pygame.transform.scale(self.ItemsUI, (screen_width*0.4, pygame.display.Info().current_h*0.4)).convert_alpha()

        #On charge l'image de l'interface de choix de bénédiction
        self.benedictionUI = pygame.image.load(os.path.join("data", "images", "Interfaces", "equip_menu_bene.png")).convert_alpha()
        self.benedictionUI = pygame.transform.scale(self.benedictionUI, (screen_width*0.4, pygame.display.Info().current_h*0.4)).convert_alpha()
        
        if self.type == 2:
            self.equipement = {
            'canons':    "+2 Canons",
            'voile':    "Voile latine",
            'coque':    "Coque épicéa"
            }
        else:
            self.equipement = {
            'canons':    "Canons de base",
            'voile':    "Voile de base",
            'coque':    "Coque de base"
            }

        #On crée une liste qui contient les bénédictions du bateau
        self.benedictions = [None, None]


        #Stocke la récompense de l'île
        self.recompense = None

        #Variables qui contiennent les modificateurs de vie et de vitesse des coques et des voiles
        self.CoqueMaxVie = 0
        self.CoqueMaxVitesse = 1
        self.VoileMaxVie = 0
        self.VoileMaxVitesse = 1

        #Variables qui contiennent les chemins des icones pour chaque type d'équipement
        self.iconCoque = res.CoqueCommun
        self.iconCoque = pygame.image.load(self.iconCoque).convert_alpha()
        self.iconCoque = pygame.transform.scale(self.iconCoque, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.iconVoile = res.VoileCommun
        self.iconVoile = pygame.image.load(self.iconVoile).convert_alpha()
        self.iconVoile = pygame.transform.scale(self.iconVoile, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.iconCanon = res.CanonCommun
        self.iconCanon = pygame.image.load(self.iconCanon).convert_alpha()
        self.iconCanon = pygame.transform.scale(self.iconCanon, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.imageBoulet = os.path.join("data", "images", "Textures", "Autres", "boulet_canon.png")


        #Variables qui contiennent les chemins des icones s'affichant sur l'interface de choix d'item
        self.DisplayIconNew = None
        self.DisplayIconPast = None

        self.timer_benediction_1 = res.Timer(0)  # Initialiser avec une durée de 0 pour permettre l'utilisation immédiate
        self.timer_benediction_2 = res.Timer(0) # Initialiser avec une durée de 0 pour permettre l'utilisation immédiate
        self.timer_dash = 15
        self.timer_sante = 20
        self.timer_aura = 30
        self.timer_rage = 30
        self.timer_godmode = 40
        self.timer_giga_tir = 50

        self.inraged = False
        self.rage_timer = None
        self.life_before_rage = 0

        self.has_aura = False
        self.aura_timer = None
        self.aura_damage_timer = res.Timer(1)
        self.aura_degat = 1

        self.godmode = False
        self.godmode_timer = None

        self.giga_tir = False
        self.giga_tir_double = False
        self.timer_giga_tir_duree = res.Timer(1)

        self.ile_actuelle = None  # Stocke l'île qui a ouvert l'interface

        self.TitleTextPast = None
        self.DescriptionTextPast = None

        self.TitleTextNew = None
        self.DescriptionTextNew = None

        self.TitleFont = pygame.font.Font(res.fontPixel, 28)
        self.DescriptionFont = pygame.font.Font(res.fontPixel, 20)

        self.text_loaded = False

        self.distance_max = screen_height*0.20
        self.distance_maxFront = self.distance_max * 1.8

        self.screen = (self.screen_width, self.screen_height)

        self.typeRec = None

        self.iconBenediction1 = None
        self.iconBenediction2 = None

        self.newBenedictionIcon = None

        self.TitleTexteBeneNew = None
        self.DescriptionTextBeneNew = None

        self.text_loaded_bene = False

        self.loadImages()


    # le bateau avance en permanence de la vitesse (donc si la vitesse vaut 0 il avance pas)
    def avancer(self):
        if self.inraged:
            self.x += self.vitesse * 1.5 * math.cos(math.radians(self.angle - 90)) # multiplie la vitesse X par le cosinus de l'angle en fonction de l'incilaison
            self.y += self.vitesse * 1.5 * math.sin(math.radians(self.angle - 90)) # pareil mais avec les Y et le sinus
        else:
            self.x += self.vitesse * math.cos(math.radians(self.angle - 90)) # multiplie la vitesse X par le cosinus de l'angle en fonction de l'incilaison
            self.y += self.vitesse * math.sin(math.radians(self.angle - 90)) # pareil mais avec les Y et le sinus
            # augmente la vitesse


    #On charge toutes les icones pour éviter des ralentissements pendant le jeu
    def loadImages(self):
        self.CanonMalus = pygame.image.load(res.CanonMalus).convert_alpha()
        self.CanonMalus = pygame.transform.scale(self.CanonMalus, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileMalus = pygame.image.load(res.VoileMalus).convert_alpha()
        self.VoileMalus = pygame.transform.scale(self.VoileMalus, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueMalus = pygame.image.load(res.CoqueMalus).convert_alpha()
        self.CoqueMalus = pygame.transform.scale(self.CoqueMalus, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonCommun = pygame.image.load(res.CanonCommun).convert_alpha()
        self.CanonCommun = pygame.transform.scale(self.CanonCommun, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonRare = pygame.image.load(res.CanonRare).convert_alpha()
        self.CanonRare = pygame.transform.scale(self.CanonRare, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonMythique = pygame.image.load(res.CanonMythique).convert_alpha()
        self.CanonMythique = pygame.transform.scale(self.CanonMythique, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CanonLegendaire = pygame.image.load(res.CanonLegendaire).convert_alpha()
        self.CanonLegendaire = pygame.transform.scale(self.CanonLegendaire, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileCommun = pygame.image.load(res.VoileCommun).convert_alpha()
        self.VoileCommun = pygame.transform.scale(self.VoileCommun, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileRare = pygame.image.load(res.VoileRare).convert_alpha()
        self.VoileRare = pygame.transform.scale(self.VoileRare, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileMythique = pygame.image.load(res.VoileMythique).convert_alpha()
        self.VoileMythique = pygame.transform.scale(self.VoileMythique, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.VoileLegendaire = pygame.image.load(res.VoileLegendaire).convert_alpha()
        self.VoileLegendaire = pygame.transform.scale(self.VoileLegendaire, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueCommun = pygame.image.load(res.CoqueCommun).convert_alpha()
        self.CoqueCommun = pygame.transform.scale(self.CoqueCommun, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueRare = pygame.image.load(res.CoqueRare).convert_alpha()
        self.CoqueRare = pygame.transform.scale(self.CoqueRare, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueMythique = pygame.image.load(res.CoqueMythique).convert_alpha()
        self.CoqueMythique = pygame.transform.scale(self.CoqueMythique, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.CoqueLegendaire = pygame.image.load(res.CoqueLegendaire).convert_alpha()
        self.CoqueLegendaire = pygame.transform.scale(self.CoqueLegendaire, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Dash = pygame.image.load(res.BeneDash).convert_alpha()
        self.Dash = pygame.transform.scale(self.Dash, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Aura = pygame.image.load(res.BeneAura).convert_alpha()
        self.Aura = pygame.transform.scale(self.Aura, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.GodMode = pygame.image.load(res.BeneGodMode).convert_alpha()
        self.GodMode = pygame.transform.scale(self.GodMode, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Projectiles = pygame.image.load(res.BeneProjectiles).convert_alpha()
        self.Projectiles = pygame.transform.scale(self.Projectiles, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Rage = pygame.image.load(res.BeneRage).convert_alpha()
        self.Rage = pygame.transform.scale(self.Rage, (6.55/100*self.screen_width, 12.7/100*self.screen_height))

        self.Sante = pygame.image.load(res.BeneSante).convert_alpha()
        self.Sante = pygame.transform.scale(self.Sante, (6.55/100*self.screen_width, 12.7/100*self.screen_height))


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
            self.vitesse -= ( 0.15 - self.vitesse_max/100)

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
        # verifie si il a rechargé
        if pygame.time.get_ticks() - self.dernier_tir >= self.cadence_tir:
            self.dernier_tir = pygame.time.get_ticks()

            
            liste_tirs = []
            
            if not self.giga_tir:
                tir_droite = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_droite, self.equipement['canons']))

                tir_gauche = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_gauche, self.equipement['canons']))

            if self.equipement['canons'] == '+1 Canon' or self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                if self.vitesse != 0:
                    tir_avant = shot.Shot(self.x, self.y, self.angle, self.distance_maxFront, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                else:
                    tir_avant = shot.Shot(self.x, self.y, self.angle, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_avant, self.equipement['canons']))

            if self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                tir_arriere = shot.Shot(self.x, self.y, self.angle + 180, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_arriere, self.equipement['canons']))

            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                tir_diag1 = shot.Shot(self.x, self.y, self.angle + 30, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag1, self.equipement['canons']))

            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons' or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir):
                tir_diag2 = shot.Shot(self.x, self.y, self.angle - 30, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag2, self.equipement['canons']))

            if "Bénédiction Projectiles" in self.benedictions and self.giga_tir:
                tir_diag3 = shot.Shot(self.x, self.y, self.angle + 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag3, self.equipement['canons']))
                tir_diag4 = shot.Shot(self.x, self.y, self.angle - 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag4, self.equipement['canons']))
                tir_droite = shot.Shot(self.x, self.y, self.angle + 90, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_droite, self.equipement['canons']))
                tir_gauche = shot.Shot(self.x, self.y, self.angle - 90, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_gauche, self.equipement['canons']))

            if self.equipement['canons'] == "Canon à tirs doubles" or ("Bénédiction Projectiles" in self.benedictions and self.giga_tir_double): 
                pygame.time.set_timer(tirDouble, 70, loops=1)

            return liste_tirs
        
    def GererEventTir(self, event, liste_tirs):
        if event.type == tirDouble and (self.equipement["canons"] == "Canon à tirs doubles" or self.giga_tir_double):
            tir_droiteD = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
            liste_tirs.append((tir_droiteD, self.equipement['canons']))

            tir_gaucheD = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
            liste_tirs.append((tir_gaucheD, self.equipement['canons']))

            if ("Bénédiction Projectiles" in self.benedictions and self.giga_tir_double):
                tir_avantD = shot.Shot(self.x, self.y, self.angle, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_avantD, self.equipement['canons']))
                tir_arriereD = shot.Shot(self.x, self.y, self.angle + 180, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_arriereD, self.equipement['canons']))
                tir_diag1D = shot.Shot(self.x, self.y, self.angle + 45, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag1D, self.equipement['canons']))
                tir_diag2D = shot.Shot(self.x, self.y, self.angle - 45, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag2D, self.equipement['canons']))
                tir_diag3D = shot.Shot(self.x, self.y, self.angle + 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag3D, self.equipement['canons']))
                tir_diag4D = shot.Shot(self.x, self.y, self.angle - 225, self.distance_max, self.imageBoulet, self.ID, self.equipement['canons'], self.inraged, self.screen)
                liste_tirs.append((tir_diag4D, self.equipement['canons']))
        
    def get_damaged(self, damage):
        r = 5
        if self.equipement['coque'] == "Coque en bois magique":
            r = random.randint(1,5)
        if r != 1 and not self.godmode:
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
    def get_vie(self):
        return self.vie
    def get_max_vie(self):
        return self.maxVie
    def get_speed(self):
        return self.vitesse
    def get_max_speed(self):
        return self.vitesse_max
    def get_maniabilite(self):
        return self.maniabilite
    def get_cadence_tir(self):
        return self.cadence_tir
    
    def getEquipement(self):
        return self.equipement
    
    def getPastDisplay(self):
        return self.DisplayIconPast
     
    def getNewDisplay(self):
        return self.DisplayIconNew
    
    def getItemUI(self):
        return self.ItemsUI
    
    def getBenedictionUI(self):
        return self.benedictionUI
    
    def getTitleTextPast(self):
        return self.TitleTextPast
    
    def getDescriptionTextPast(self):
        return self.DescriptionTextPast
    
    def getTitleTextNew(self):
        return self.TitleTextNew
    
    def getDescriptionTextNew(self):
        return self.DescriptionTextNew
    
    def getImages(self):
        return self.iconCoque, self.iconVoile, self.iconCanon
    
    def getBenedictionsImages(self):
        return self.newBenedictionIcon, self.iconBenediction1, self.iconBenediction2
    
    def getBenedictionsTexts(self):
        return self.benedictions[0], self.benedictions[1], self.TitleTexteBeneNew, self.DescriptionTextBeneNew
    

    def LoadText(self):
        if not isinstance(self.TitleTextPast, pygame.Surface):
            self.TitleTextPast = self.TitleFont.render(self.equipement[self.typeRec], True, (0, 0, 0))  # Noir
        if not isinstance(self.DescriptionTextPast, pygame.Surface):
            equip = self.equipement[self.typeRec]
            self.DescriptionTextPast = self.DescriptionFont.render(res.dictItemsBuff[equip], True, (0, 0, 0))

        if not isinstance(self.TitleTextNew, pygame.Surface):
            self.TitleTextNew = self.TitleFont.render(self.recompense[0], True, (0, 0, 0))  # Noir
        if not isinstance(self.DescriptionTextNew, pygame.Surface):
            equip = self.recompense[0]
            self.DescriptionTextNew = self.DescriptionFont.render(res.dictItemsBuff[equip], True, (0, 0, 0))

    def LoadTextBene(self):
        self.TitleTexteBeneNew = self.TitleFont.render(self.recompense[0], True, (0, 0, 0))
        benediction = self.recompense[0]
        self.DescriptionTextBeneNew = self.DescriptionFont.render(res.dictBenedictionsBuff[benediction], True, (0, 0, 0))

    def verifIleExiste(self, liste_iles):
        if (self.ile_actuelle is not None) and (self.ile_actuelle not in liste_iles):
            self.afficher_benediction = False
            self.afficher_items = False
            self.text_loaded = False
            self.ile_actuelle = None



    def equipInterface(self, recompense, xIle, yIle, ile):
        self.recompense = recompense
        if self.recompense[0] in res.listeCanons:
            self.typeRec = "canons"
        elif self.recompense[0] in res.listeVoiles:
            self.typeRec = "voile"
        elif self.recompense[0] in res.listeCoques:
            self.typeRec = "coque"


        if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
            if (self.recompense[0] not in res.liste_benedictions) and (self.recompense[0] not in res.liste_malus):
                # Si l'interface n'est pas affichée, ou si on s'approche d'une nouvelle île
                if not self.afficher_items or self.ile_actuelle is None:

                    if self.ile_actuelle != ile:
                        self.afficher_items = False
                        self.text_loaded = False
                        self.TitleTextPast = None
                        self.DescriptionTextPast = None
                        self.TitleTextNew = None
                        self.DescriptionTextNew = None
                        self.ile_actuelle = ile
                    
                    self.updateDisplayIconItem()
                    self.LoadText()
                    self.text_loaded = True
                    self.ile_actuelle = ile  # On mémorise l'île qui a ouvert l'interface

                self.afficher_items = True

            elif self.recompense[0] in res.liste_malus:
                self.updateDisplayIconItem()
                self.equiper()
                self.verifIleMalus = True
                
        elif self.recompense[0] not in res.liste_benedictions and self.recompense[0] not in res.liste_malus and self.ile_actuelle == ile:
                self.afficher_items = False
                self.text_loaded = False
                self.ile_actuelle = None  # On oublie l'île actuelle
        
    def beneInterface(self, xIle, yIle, ile):
        if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
            if self.recompense[0] in res.liste_benedictions:

                # Si l'interface n'est pas affichée, ou si on s'approche d'une nouvelle île
                if not self.afficher_benediction or self.ile_actuelle is None:

                    if self.ile_actuelle != ile:
                        self.afficher_benediction = False
                        self.text_loaded_bene = False
                        self.TitleTexteBeneNew = None
                        self.DescriptionTextBeneNew = None
                        self.ile_actuelle = ile

                    #Update des icones et du texte
                    self.updateDisplayIconBene()
                    self.LoadTextBene()
                    self.text_loaded_bene = True
                    self.ile_actuelle = ile
                    
                self.afficher_benediction = True

        elif self.recompense[0] in res.liste_benedictions and self.ile_actuelle == ile:
            self.afficher_benediction = False
            self.text_loaded_bene = False
            self.ile_actuelle = None
            

        
    def updateDisplayIconItem(self):
        if self.recompense[0] in res.listeCanons:
            self.DisplayIconPast = self.iconCanon
            if self.recompense[1] == "commun":
                self.DisplayIconNew = self.CanonCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = self.CanonRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = self.CanonMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = self.CanonLegendaire
        elif self.recompense[0] in res.listeCoques:
            self.DisplayIconPast = self.iconCoque
            if self.recompense[1] == "commun":
                self.DisplayIconNew = self.CoqueCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = self.CoqueRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = self.CoqueMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = self.CoqueLegendaire
        elif self.recompense[0] in res.listeVoiles:
            self.DisplayIconPast = self.iconVoile
            if self.recompense[1] == "commun":
                self.DisplayIconNew = self.VoileCommun
            elif self.recompense[1] == "rare":
                self.DisplayIconNew = self.VoileRare
            elif self.recompense[1] == "mythique":
                self.DisplayIconNew = self.VoileMythique
            elif self.recompense[1] == "légendaire":
                self.DisplayIconNew = self.VoileLegendaire
        elif self.recompense[0] in res.liste_malus:
            if self.recompense[0] == res.liste_malus[0]:
                self.DisplayIconPast = self.iconCanon
                self.DisplayIconNew = self.CanonMalus
            elif self.recompense[0] == res.liste_malus[1]:
                self.DisplayIconPast = self.iconVoile
                self.DisplayIconNew = self.VoileMalus
            elif self.recompense[0] == res.liste_malus[2]:
                self.DisplayIconPast = self.iconCoque
                self.DisplayIconNew = self.CoqueMalus

    def updateDisplayIconBene(self):
        if self.recompense[0] == "Bénédiction Dash":
            self.newBenedictionIcon = self.Dash
        elif self.recompense[0] == "Bénédiction d'aura":
            self.newBenedictionIcon = self.Aura
        elif self.recompense[0] == "Bénédiction GodMode":
            self.newBenedictionIcon = self.GodMode
        elif self.recompense[0] == "Bénédiction Projectiles":
            self.newBenedictionIcon = self.Projectiles
        elif self.recompense[0] == "Bénédiction de rage":
            self.newBenedictionIcon = self.Rage
        elif self.recompense[0] == "Bénédiction Santé":
            self.newBenedictionIcon = self.Sante

    def equiper(self):
        # Mettre à jour l'équipement en fonction de la récompense
        if self.recompense[0] in res.listeCanons or self.recompense[0] == res.liste_malus[0]:
            self.equipement['canons'] = self.recompense[0]
        elif self.recompense[0] in res.listeVoiles or self.recompense[0] == res.liste_malus[1]:
            self.equipement['voile'] = self.recompense[0]
        elif self.recompense[0] in res.listeCoques or self.recompense[0] == res.liste_malus[2]:
            self.equipement['coque'] = self.recompense[0]
        self.effetItem()

    def equiper_benediction(self, emplacement):
        if self.recompense[0] in res.liste_benedictions:
            if emplacement == 0:
                self.benedictions[0] = self.recompense[0]
                self.iconBenediction1 = self.newBenedictionIcon
            elif emplacement == 1:
                self.benedictions[1] = self.recompense[0]
                self.iconBenediction2 = self.newBenedictionIcon
        


    def effetItem(self):
        self.maxVie = 50
        self.vitesse_max = 5
        self.maniabilite = 4

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
                self.CoqueMaxVitesse = 0.80
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

        elif self.recompense[0] in res.listeVoiles:
            self.iconVoile = self.DisplayIconNew
            self.VoileMaxVitesse = 1
            self.VoileMaxVie = 0
            if self.equipement['voile'] == "Voile en toile de jute":
                self.VoileMaxVitesse = 1.05
            elif self.equipement['voile'] == "Voile latine":
                self.VoileMaxVitesse = 1.1
            elif self.equipement['voile'] == "Voile enchantée":
                self.VoileMaxVitesse = 1.25
                self.maniabilite = self.maniabilite * 1.02
            elif self.equipement['voile'] == "Voile légendaire":
                self.VoileMaxVitesse = 1.3
                self.maniabilite = self.maniabilite * 1.05

        elif self.recompense[0] in res.listeCanons:
            self.iconCanon = self.DisplayIconNew
            if (self.equipement['canons'] == "Canon en or") or (self.equipement['canons'] == "Canon légendaire"):
                self.cadence_tir = 600

        elif self.recompense[0] in res.liste_malus:
            if self.recompense[0] == "Voile Trouée":
                self.iconVoile = self.DisplayIconNew
                self.VoileMaxVitesse = 0.75
            elif self.recompense[0] == "Canons Rouillés":
                self.iconCanon = self.DisplayIconNew
            elif self.recompense[0] == "Coque Trouée":
                self.iconCoque = self.DisplayIconNew

        self.maxVie = self.maxVie + self.VoileMaxVie + self.CoqueMaxVie
        self.vitesse_max = self.vitesse_max * self.VoileMaxVitesse * self.CoqueMaxVitesse
        if self.vie > self.maxVie:
            self.vie = self.maxVie

    # benediction 1 est comme benediction 2 mais en plus puissant
    def use_benediction_1(self):
        if len(self.benedictions) > 0:
            if self.timer_benediction_1.timer_ended_special(self.timer_dash) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction Dash": # te fait dasher de 200
                    self.x += 350 * math.cos(math.radians(self.angle - 90))
                    self.y += 350 * math.sin(math.radians(self.angle - 90))
                    self.timer_benediction_1 = res.Timer(50)
            
            if self.timer_benediction_1.timer_ended_special(self.timer_sante) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction Santé": # te rend 50% de ta vie max
                    self.vie += math.floor(self.maxVie*0.5)
                    if self.vie > self.maxVie:
                        self.vie = self.maxVie
                    self.timer_benediction_1 = res.Timer(50)
            
            if self.timer_benediction_1.timer_ended_special(self.timer_aura) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction d'aura":
                    self.aura_timer = res.Timer(10)
                    self.has_aura = True
                    self.timer_benediction_1 = res.Timer(50)
                    self.aura_degat = 2

            if self.timer_benediction_1.timer_ended_special(self.timer_rage) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction de rage":
                    self.rage_timer = res.Timer(15)
                    self.inraged = True
                    self.life_before_rage = self.vie/self.maxVie
                    self.vie = 20
                    self.timer_benediction_1 = res.Timer(50)
                    self.gif_rage = True
                
            if self.timer_benediction_1.timer_ended_special(self.timer_godmode) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction GodMode":
                    self.godmode = True
                    self.godmode_timer = res.Timer(20)
                    self.timer_benediction_1 = res.Timer(50)
            
            if self.timer_benediction_1.timer_ended_special(self.timer_giga_tir) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction Projectiles":
                    self.giga_tir = True
                    self.giga_tir_double = True
                    self.timer_giga_tir_duree = res.Timer(8)
                    self.timer_benediction_1 = res.Timer(50)
        

    def use_benediction_2(self):
        if len(self.benedictions) > 1:
            if self.timer_benediction_2.timer_ended_special(self.timer_dash) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction Dash": # te fait dasher de 200
                    self.x += 250 * math.cos(math.radians(self.angle - 90))
                    self.y += 250 * math.sin(math.radians(self.angle - 90))
                    self.timer_benediction_2 = res.Timer(50)
            
            if self.timer_benediction_2.timer_ended_special(self.timer_sante) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction Santé": # te rend 50% de ta vie max
                    self.vie += math.floor(self.maxVie*0.25)
                    if self.vie > self.maxVie:
                        self.vie = self.maxVie
                    self.timer_benediction_2 = res.Timer(50)
            
            if self.timer_benediction_2.timer_ended_special(self.timer_aura) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction d'aura":
                    self.aura_timer = res.Timer(10)
                    self.has_aura = True
                    self.timer_benediction_2 = res.Timer(50)
                    self.aura_degat = 1

            if self.timer_benediction_2.timer_ended_special(self.timer_rage) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction de rage":
                    self.rage_timer = res.Timer(10)
                    self.inraged = True
                    self.life_before_rage = self.vie/self.maxVie
                    self.vie = 20
                    self.timer_benediction_2 = res.Timer(50)
                    self.gif_rage = True
                
            if self.timer_benediction_2.timer_ended_special(self.timer_godmode) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction GodMode":
                    self.godmode = True
                    self.godmode_timer = res.Timer(10)
                    self.timer_benediction_2 = res.Timer(50)

            if self.timer_benediction_2.timer_ended_special(self.timer_giga_tir) or self.timer_benediction_2.timer_ended():
                if self.benedictions[1] == "Bénédiction Projectiles":    
                    self.giga_tir = True
                    self.timer_giga_tir_duree = res.Timer(5)
                    self.timer_benediction_2 = res.Timer(50)

    def still_inraged(self):
        if self.inraged:
            if self.rage_timer != None and self.rage_timer.timer_ended():
                self.inraged = False
                self.vie = int(math.floor(self.maxVie * self.life_before_rage))
                self.rage_timer = None

    def still_giga_tir(self):
        if self.giga_tir:
            if self.timer_giga_tir_duree.timer_ended():
                self.giga_tir = False
                self.giga_tir_double = False

    def is_giga_tir(self):
        return self.giga_tir
    
    def is_inrage(self):
        return self.inraged
    
    def in_godmode(self):
        if self.godmode:
            if self.godmode_timer.timer_ended():
                self.godmode = False
                self.godmode_timer = None
    
    def godmode_active(self):
        return self.godmode
    
    def stop_animation_rage(self):
        self.gif_rage = False
    
    def aura_activated(self, liste_navires):
        if self.has_aura:
            for n in liste_navires:
                if self.aura_damage_timer.timer_ended() and n.get_ID() != self.ID:
                    if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 150:
                        n.get_damaged(self.aura_degat)
                        if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 120:
                            n.get_damaged(self.aura_degat)
                            if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 90:
                                n.get_damaged(self.aura_degat)
                                if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 60:
                                    n.get_damaged(self.aura_degat)
                                    if res.calc_distance(self.x, self.y, n.position_x(), n.position_y()) <= 30:
                                        n.get_damaged(self.aura_degat)
                        self.aura_damage_timer.reset()
            if self.aura_timer.timer_ended():
                self.has_aura = False
                self.aura_timer = None

    def aura_active(self):
        return self.has_aura
            


    def updateIcons(self):
        if self.recompense[1] == "commun":
            if self.recompense[0] in res.listeCanons:
                self.AncienneiconCanon = self.iconCanon
                self.iconCanon = res.CanonCommun
            elif  self.recompense[0] in res.listeVoiles:
                self.AncienneiconVoile = self.iconVoile
                self.iconVoile = res.VoileCommun
            elif  self.recompense[0] in res.listeCoques:
                self.AncienneiconCoque = self.iconCoque
                self.iconCoque = res.CoqueCommun
            elif self.recompense[0] in res.liste_malus:
                if self.equipement['voile'] == "Voile Trouée":
                    self.AncienneiconVoile = self.iconVoile
                    self.iconVoile = res.VoileMalus
                if self.equipement['canons'] == "Canons Rouillés":
                    self.AncienneiconCanon = self.iconCanon
                    self.iconCanon = res.CanonMalus
                if self.equipement['coque'] == "Coque Trouée":
                    self.AncienneiconCoque = self.iconCoque
                    self.iconCoque = res.CoqueMalus
        elif self.recompense[1] == "rare":
            if self.recompense[0] in res.listeCanons:
                self.AncienneiconCanon = self.iconCanon
                self.iconCanon = res.CanonRare
            elif  self.recompense[0] in res.listeVoiles:
                self.AncienneiconVoile = self.iconVoile
                self.iconVoile = res.VoileRare
            elif  self.recompense[0] in res.listeCoques:
                self.AncienneiconCoque = self.iconCoque
                self.iconCoque = res.CoqueRare
        elif self.recompense[1] == "mythique":
            if self.recompense[0] in res.listeCanons:
                self.AncienneiconCanon = self.iconCanon
                self.iconCanon = res.CanonMythique
            elif  self.recompense[0] in res.listeVoiles:
                self.AncienneiconVoile = self.iconVoile
                self.iconVoile = res.VoileMythique
            elif  self.recompense[0] in res.listeCoques:
                self.AncienneiconCoque = self.iconCoque
                self.iconCoque = res.CoqueMythique
        elif self.recompense[1] == "légendaire":
            if self.recompense[0] in res.listeCanons:
                self.AncienneiconCanon = self.iconCanon
                self.iconCanon = res.CanonLegendaire
            elif  self.recompense[0] in res.listeVoiles:
                self.AncienneiconVoile = self.iconVoile
                self.iconVoile = res.VoileLegendaire
            elif  self.recompense[0] in res.listeCoques:
                self.AncienneiconCoque = self.iconCoque
                self.iconCoque = res.CoqueLegendaire

    
    def heal_par_vague(self):
        if self.maxVie - self.vie <= 30:
            self.vie = self.maxVie
        else:
            self.vie += 30

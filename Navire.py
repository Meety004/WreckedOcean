import math
import pygame
import random
import shot
import string
import ressources as res

tirDouble = pygame.USEREVENT + 1

class Navire:
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height, dt):
        # Contrôle du vaisseau
        self.vitesse_max = v_max
        self.acceleration = acceleration
        self.x = random.randint(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.vitesse = 0
        self.angle = 270
        self.maniabilite = maniabilite # le temps qu'il met pour tourner. c'est ca "vitesse de rotation"
        self.width = 40
        self.height = 60
        original_image = pygame.image.load(image).convert_alpha()
        original_image = pygame.transform.scale(original_image, (self.width, self.height)).convert_alpha()
        self.image = original_image  # Image qui sera affichée
        self.dernier_tire = 0 # le denier tire fait par le bateau pour le chrono
        self.cadance_tire = 1000 # en milliseconde
        self.ID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        self.maxVie = 50
        self.vie = self.maxVie
        self.verifIleMalus = False

        self.afficher_items = False  # Variable d'état pour suivre l'affichage de l'image
        self.ItemsUI = pygame.image.load("images/Interfaces/equip_menu_item.png").convert_alpha()
        self.ItemsUI = pygame.transform.scale(self.ItemsUI, (screen_width*0.4, pygame.display.Info().current_h*0.4)).convert_alpha()

        self.equipement = {
        'canons':    "gros caca tout moche",
        'voile':    "Voile de base",
        'coque':    "Coque de base"
        }

        self.benedictions = ["Bénédiction d'aura", "Bénédiction d'aura"]

        self.recompense = None

        self.CoqueMaxVie = 0
        self.CoqueMaxVitesse = 1
        self.VoileMaxVie = 0
        self.VoileMaxVitesse = 1

        self.iconCoque = res.CoqueCommun
        self.iconVoile = res.VoileCommun
        self.iconCanon = res.CanonCommun

        self.AncienneiconCoque = None
        self.AncienneiconVoile = None
        self.AncienneiconCanon = None

        self.DisplayIconNew = None
        self.DisplayIconPast = None

        self.timer_benediction_1 = res.Timer(0)  # Initialiser avec une durée de 0 pour permettre l'utilisation immédiate
        self.timer_benediction_2 = res.Timer(0) # Initialiser avec une durée de 0 pour permettre l'utilisation immédiate
        self.timer_dash = 15
        self.timer_sante = 20
        self.timer_aura = 30
        self.timer_rage = 30
        self.timer_godmode = 40

        self.inraged = False
        self.rage_timer = None
        self.life_before_rage = 0

        self.has_aura = False
        self.aura_timer = None
        self.aura_damage_timer = res.Timer(1)
        self.aura_degat = 1

        self.godmode = False
        self.godmode_timer = None

    # le bateau avance en permanence de la vitesse (donc si la vitesse vaut 0 il avance pas)
    def avancer(self):
        if self.inraged:
            self.x += self.vitesse * 1.5 * math.cos(math.radians(self.angle - 90)) # multiplie la vitesse X par le cosinus de l'angle en fonction de l'incilaison
            self.y += self.vitesse * 1.5 * math.sin(math.radians(self.angle - 90)) # pareil mais avec les Y et le sinus
        else:
            self.x += self.vitesse * math.cos(math.radians(self.angle - 90)) # multiplie la vitesse X par le cosinus de l'angle en fonction de l'incilaison
            self.y += self.vitesse * math.sin(math.radians(self.angle - 90)) # pareil mais avec les Y et le sinus

    # auglente la vitesse
    def accelerer(self):
        # accelere tant que la vitesse max n'est pas atteinte
        if self.vitesse < self.vitesse_max:
            self.vitesse += self.acceleration
        # si la vitesse max est atteinte il revient a la vitesse max
        if self.vitesse > self.vitesse_max:
            self.vitesse = self.vitesse_max
        # je voulais faire progressivement mais pour une raison magique je peux pas utiliser de fonction dans une autre sans que ca affect les classe fille de maniere bizzar

    # si il arrete d'avancer le bateau décelère
    def ralentit(self):
        # ralenti tant qu'il n'est pas a 0
        if self.vitesse > 0:
            self.vitesse -= ( 0.3 - self.vitesse_max/100)
        # revient a 0 si il est en dessous
        if self.vitesse < 0:
            self.vitesse = 0

    def tourne_gauche(self):
        if self.vitesse > 0:
            self.angle -= self.maniabilite
            # si l'angle part en dessous de 0 il lui rajoute 360 pour qu'il reste toujours entre 0 et 360
            if self.angle < 0:
                self.angle += 360

    def tourne_droite(self):
        if self.vitesse > 0:
            self.angle += self.maniabilite
            # si l'angle est superieur a 360 ou lui eneleve 360 pour qu'il reste entre 0 et 360
            if self.angle >= 360:
                self.angle -= 360

    # pour que le bateau ne sorte pas de l'ecran et revienne de l'autre coter
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
        if pygame.time.get_ticks() - self.dernier_tire >= self.cadance_tire:
            self.dernier_tire = pygame.time.get_ticks()

            # argument : x, y, angle, distance_max, image
            # l'angle est ajusté en fonction de la vitesse du bateau. si il avance les boulet continue dans sa direction
            liste_tirs = []

            tir_droite = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
            liste_tirs.append((tir_droite, self.equipement['canons']))

            tir_gauche = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
            liste_tirs.append((tir_gauche, self.equipement['canons']))

            if self.equipement['canons'] == '+1 Canon' or self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_avant = shot.Shot(self.x, self.y, self.angle, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
                liste_tirs.append((tir_avant, self.equipement['canons']))

            if self.equipement['canons'] == '+2 Canons' or self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_arriere = shot.Shot(self.x, self.y, self.angle + 180, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
                liste_tirs.append((tir_arriere, self.equipement['canons']))

            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_diag1 = shot.Shot(self.x, self.y, self.angle + 30, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
                liste_tirs.append((tir_diag1, self.equipement['canons']))

            if self.equipement['canons'] == '+3 Canons' or self.equipement['canons'] == '+4 Canons':
                tir_diag2 = shot.Shot(self.x, self.y, self.angle - 30, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
                liste_tirs.append((tir_diag2, self.equipement['canons']))

            if self.equipement['canons'] == "Canon à tirs doubles":     
                pygame.time.set_timer(tirDouble, 50, loops=1)

            return liste_tirs
        
    def GererEventTir(self, event, liste_tirs):
        if event.type == tirDouble:
            tir_droiteD = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
            liste_tirs.append((tir_droiteD, self.equipement['canons']))

            tir_gaucheD = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID, self.equipement['canons'], self.inraged)
            liste_tirs.append((tir_gaucheD, self.equipement['canons']))

        
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
    
    def getEquipement(self):
        return self.equipement

    def equipInterface(self, recompense, xIle, yIle):
        self.recompense = recompense
        if (self.recompense[0] not in res.liste_benedictions) and (self.recompense[0] not in res.liste_malus):
            
            if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
                self.afficher_items = True
                self.updateIcons()
            else:
                self.afficher_items = False
        else:
            self.afficher_items = False
            if self.recompense[0] in res.liste_malus and res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
                self.equiper()
                self.updateIcons()
                self.verifIleMalus = True


    def equiper(self):
        if self.recompense[0] in res.listeCanons:
            self.equipement['canons'] = self.recompense[0]
        elif self.recompense[0] in res.listeVoiles:
            self.equipement['voile'] = self.recompense[0]
        elif self.recompense[0] in res.listeCoques:
            self.equipement['coque'] = self.recompense[0]
        elif self.recompense[0] in res.liste_malus:
            if self.recompense[0] == res.liste_malus[0]:
                self.equipement['canons'] = self.recompense[0]
            elif self.recompense[0] == res.liste_malus[1]:
                self.equipement['voile'] = self.recompense[0]
            elif self.recompense[0] == res.liste_malus[2]:
                self.equipement['coque'] = self.recompense[0]
        print(self.equipement)
        self.effetItem()

    def effetItem(self):
        self.updateIcons()
        self.maxVie = 50
        self.vitesse_max = 7
        self.maniabilite = 5

        if self.recompense[0] in res.listeCoques:
            self.DisplayIconPast = self.AncienneiconCoque
            self.DisplayIconNew = self.iconCoque
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
            self.DisplayIconPast = self.AncienneiconVoile
            self.DisplayIconNew = self.iconVoile
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
            self.DisplayIconPast = self.AncienneiconCanon
            self.DisplayIconNew = self.iconCanon
            if (self.equipement['canons'] == "Canon en or") or (self.equipement['canons'] == "Canon légendaire"):
                self.cadance_tir = 900

        if self.recompense[0] in res.liste_malus:
            if self.equipement['voile'] == "Voile Trouée":
                self.VoileMaxVitesse = 0.5

        self.maxVie = self.maxVie + self.VoileMaxVie + self.CoqueMaxVie
        self.vitesse_max = self.vitesse_max * self.VoileMaxVitesse * self.CoqueMaxVitesse
        if self.vie > self.maxVie:
                self.vie = self.maxVie

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

            if self.benedictions[1] == "Bénédiction Projectile":
                pass # a faire plus tard. tire une salve de projectile tout autour du joueur

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
                    self.vie = 30
                    self.timer_benediction_1 = res.Timer(50)
                    self.gif_rage = True
                
            if self.timer_benediction_1.timer_ended_special(self.timer_godmode) or self.timer_benediction_1.timer_ended():
                if self.benedictions[0] == "Bénédiction GodMode":
                    self.godmode = True
                    self.godmode_timer = res.Timer(20)
                    self.timer_benediction_1 = res.Timer(50)
            
            if self.benedictions[0] == "Bénédiction Projectile":
                pass # a faire plus tard. tire une salve de projectile tout autour du joueur

    def still_inraged(self):
        if self.inraged:
            if self.rage_timer != None and self.rage_timer.timer_ended():
                self.inraged = False
                self.vie = int(math.floor(self.maxVie * self.life_before_rage))
                self.rage_timer = None
    
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
    
    def aura_activated(self, liste_ennemis):
        if self.has_aura:
            for ennemi in liste_ennemis:
                if self.aura_damage_timer.timer_ended():
                    if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 150:
                        ennemi.get_damaged(self.aura_degat)
                        if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 120:
                            ennemi.get_damaged(self.aura_degat)
                            if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 90:
                                ennemi.get_damaged(self.aura_degat)
                                if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 60:
                                    ennemi.get_damaged(self.aura_degat)
                                    if res.calc_distance(self.x, self.y, ennemi.position_x(), ennemi.position_y()) <= 30:
                                        ennemi.get_damaged(self.aura_degat)
                        print(ennemi.get_vie())
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


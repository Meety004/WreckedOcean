import math
import pygame
import random
import shot
import string
import ressources as res

class Navire:
    def __init__(self, v_max, acceleration, maniabilite, image, screen_width, screen_height):
        # Contrôle du vaisseau
        self.vitesse_max = v_max
        self.acceleration = acceleration
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
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

        self.afficher_items = False  # Variable d'état pour suivre l'affichage de l'image
        self.ItemsUI = pygame.image.load("images/Interfaces/equip_menu_item.png").convert_alpha()
        self.ItemsUI = pygame.transform.scale(self.ItemsUI, (screen_width*0.4, screen_height*0.4)).convert_alpha()

        self.equipement = {
        'canons':    "Canons Rouillés",
        'voile':    "Voile Trouée",
        'coque':    "Coque Trouée"
        }

        self.benedictions = []

        self.recompense = None

    # le bateau avance en permanence de la vitesse (donc si la vitesse vaut 0 il avance pas)
    def avancer(self):
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
            self.vitesse -= 0.07
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

            tir_droite = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID)
            liste_tirs.append(tir_droite)

            tir_gauche = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID)
            liste_tirs.append(tir_gauche)

            if self.equipement['canons'] == '+1 Canon' or self.equipement['canons'] == '+2 Canon' or self.equipement['canons'] == '+3 Canon' or self.equipement['canons'] == '+4 Canon':
                tir_avant = shot.Shot(self.x, self.y, self.angle + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID)
                liste_tirs.append(tir_avant)

                if self.equipement['canons'] == '+2 Canon' or self.equipement['canons'] == '+3 Canon' or self.equipement['canons'] == '+4 Canon':
                    tir_arriere = shot.Shot(self.x, self.y, self.angle + 180 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID)
                    liste_tirs.append(tir_arriere)

                    if self.equipement['canons'] == '+3 Canon' or self.equipement['canons'] == '+4 Canon':
                        tir_diag1 = shot.Shot(self.x, self.y, self.angle + 45 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID)
                        liste_tirs.append(tir_diag1)

                        if self.equipement['canons'] == '+4 Canon':
                            tir_diag2 = shot.Shot(self.x, self.y, self.angle - 45 + self.vitesse*3, 170, "images/Textures/Autres/boulet_canon.png", self.ID)
                            liste_tirs.append(tir_diag2)

            return liste_tirs
        else:
            return None
        
    def get_damaged(self, damage):
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

    def equipInterface(self, recompense, xIle, yIle):
        self.recompense = recompense
        if (recompense not in res.liste_benedictions) and (recompense not in res.liste_malus):
            
            if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
                self.afficher_items = True
            else:
                self.afficher_items = False
        else:
            self.afficher_items = False
            print('Malus/Bene')

    def equiper(self):
        print(self.recompense)
        if self.recompense[0] in res.listeCanons:
            self.equipement['canons'] = self.recompense[0]
        elif self.recompense[0] in res.listeVoiles:
            self.equipement['voile'] = self.recompense[0]
        elif self.recompense[0] in res.listeCoques:
            self.equipement['coque'] = self.recompense[0]
        print(self.equipement)
        self.effetItem()

    def effetItem(self):
        if self.equipement['coque'] == self.recompense[0]:
            if self.equipement['coque'] == "Coque épicéa":
                self.maxVie += 10
            elif self.equipement['coque'] == "Coque en bouleau":
                self.maxVie += 10
                self.vitesse_max = self.vitesse_max * 1.1
            elif self.equipement['coque'] == "Coque en chêne massif":
                self.maxVie += 75
                self.vitesse_max = self.vitesse_max * 0.9
            elif self.equipement['coque'] == "Coque chêne":
                self.vitesse_max = self.vitesse_max * 1.05
            elif self.equipement['coque'] == "Coque en bois magique":
                self.maxVie += 50
                self.vitesse_max = self.vitesse_max * 1.2
            else:
                self.maxVie += 60
                self.vitesse_max = self.vitesse_max * 1.3
        

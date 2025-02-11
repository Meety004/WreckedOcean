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
        self.vie = 50

        self.afficher_items = False  # Variable d'état pour suivre l'affichage de l'image
        self.ItemsUI = pygame.image.load("images/equip_menu_item.png").convert_alpha()
        self.ItemsUI = pygame.transform.scale(self.ItemsUI, (screen_width*0.4, screen_height*0.4)).convert_alpha()

        self.equipement = {
        'canons':    "Canons Rouillés",
        'voile':    "Voile Trouée",
        'coque':    "Coque Trouée"
        }

        self.benedictions = []

        self.recompense = None

        self.liste_benedictions = [
            "Bénédiction Dash", 
            "Bénédiction Santé",
            "Bénédiction d'aura", 
            "Bénédiciton de rage",
            "Bénédiction GodMode", 
            "Bénédiction Projectile"
        ]

        self.liste_malus = [
            "Canons Rouillés",
            "Voile Trouée",
            "Coque Trouée"
        ]

        self.listeCanons = [
            "1 Canon",
            "Canon en bronze",
            "2 Canons", 
            "Canon en argnet", 
            "Canon Ballistique",
            "3 Canons", 
            "Canon en or", 
            "Canon à tirs doubles",
            "4 Canons", 
            "Canon légendaire"
        ]

        self.listeCoques = [
            "Coque épicéa",
            "Coque chêne",
            "Coque en bouleau", 
            "Coque en chêne massif",
            "Coque en bois magique",
            "Coque légendaire"
        ]

        self.listeVoiles = [
            "Voile en toile de jute",
            "Voile Latine",
            "Voile Enchantée", 
            "Voile légendaire"
        ]


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
            tire_droite = shot.Shot(self.x, self.y, self.angle + 90 - self.vitesse*3, 170, "images/boulet_canon.png", self.ID)
            tire_gauche = shot.Shot(self.x, self.y, self.angle - 90 + self.vitesse*3, 170, "images/boulet_canon.png", self.ID)
            return [tire_droite, tire_gauche]
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
        if (recompense not in self.liste_benedictions) and (recompense not in self.liste_malus):
            
            if res.calc_distance(self.x, self.y, xIle, yIle) <= 75:
                self.afficher_items = True
            else:
                self.afficher_items = False
        else:
            self.afficher_items = False
            print('Malus/Bene')

    def equiper(self):
        print(self.recompense)
    
    def getItem(self):
        pass


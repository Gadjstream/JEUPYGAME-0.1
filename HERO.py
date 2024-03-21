import pygame
import random
import math

"""on importe la classe pour avoir accès aux fonctions principale, 
mais on n'a pas accès à l'objet "jeu" initialisé dans le "main" """
from FONCTIONS import Fonctions


class Hero(pygame.sprite.Sprite):

    # Stats et fonctions principales du hero

    def __init__(self):
        super().__init__()

        # Initialisation d'un objet Fonctions pour avoir accès aux fonctions principales du jeu
        self.jeu = Fonctions(self, screen=None, LARGE=1080, HAUT=720)

        # Chargement de la sprite sheet
        self.sprite_sheet = pygame.image.load("SPRITE/HERO.png")
        self.sprites = {
            "hero": self.get_image(0, 0),
            "hero_dmg": self.get_image(320, 0),
            "tp1": self.get_image(640, 0),
            "tp2": self.get_image(960, 0),
            "tp3": self.get_image(1280, 0),
        }

        # Configuration de l'image principale, redimention, transparence.
        self.image = self.sprites["hero"]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([0, 0, 0])

        # Position du héro dans l'espace, variables pour gérer sa direction et son angle de rotation
        self.rect = self.image.get_rect()
        self.rect.x = 540-25
        self.rect.y = 360-25
        self.dirx = 0
        self.diry = 0
        self.angle = 0

        # définis les dimansions du cadre dans lequel il peut se déplacer
        self.marge = 100

        # Coordonnées aléatoires
        self.random_x = random.randint(0, 1080)
        self.random_y = random.randint(0, 720)

        # Gestion des états du héro et des cooldowns
        self.update_hero = True
        self.hero_alive = True
        self.dmg_taken = False
        self.reposition = False
        self.tire = True

        # Stats du héro
        self.hp = 100
        self.hp_max = 100
        self.speed = 2
        self.range = 120
        self.attack_speed = 1000
        self.vision = 300

    def get_image(self, x, y):  # récupère un sprite dans la sprite sheet
        image = pygame.Surface([320, 320])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 320, 320))
        image = pygame.transform.scale(image, (50, 50))
        return image

    def move(self):

        # Gère le mouvement du héro

        # Avance dans une direction donnée
        self.rect.y += self.diry
        self.rect.x += self.dirx

        # si le hero sort du cadre, il se dirige vers le centre
        if (self.rect.x < self.marge or self.rect.x > self.jeu.LARGE - self.marge
                or self.rect.y < self.marge or self.rect.y > self.jeu.HAUT - self.marge
                and not self.reposition):
            self.direction(self.jeu.CENTER[0], self.jeu.CENTER[1])
            self.cd_move_center()

        # le hero change aleatoirement de direction s'il n'a pas d'autre impératif
        if self.update_hero and not self.reposition:
            self.randomise()
            self.direction(self.random_x, self.random_y)
            self.cd_move_random()

    def cd_move_center(self):  # Lance le cooldown avant le prochain changement de direction (à fusionner)
        self.reposition = True
        i = random.randint(400, 3000)
        pygame.time.set_timer(pygame.USEREVENT + 5, i)

    def cd_move_random(self):  # Lance le cooldown avant le prochain changement de direction (à fusionner)
        self.update_hero = False
        i = random.randint(400, 3000)
        pygame.time.set_timer(pygame.USEREVENT+2, i)

    def direction(self, x, y):  # définis la direction du hero vers un point donné
        angle = self.jeu.calculate_angle(self.rect.x, self.rect.y, x, y)
        self.dirx = self.speed * math.cos(angle)
        self.diry = self.speed * math.sin(angle)

    def randomise(self):  # Assigne de nouvelles valeurs random pour le déplacement aléatoire
        self.random_x = random.randint(0, 1080)
        self.random_y = random.randint(0, 720)
        return self.random_x, self.random_y

    def anim_dmg(self, sprite_name):  # Affiche le sprite de dégat du hero
        self.image = self.sprites[sprite_name]
        self.image.set_colorkey([0, 0, 0])
        pygame.time.set_timer(pygame.USEREVENT + 4, 500)




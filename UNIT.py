import pygame
import math
from ANIM_KILL import AnimKillUnit


class Unit(pygame.sprite.Sprite):

    def __init__(self, hero, jeu):
        super().__init__()
        self.hero = hero
        self.jeu = jeu

        self.sprite_sheet = pygame.image.load("SPRITE/UNIT.png")
        self.sprites = {
            "unit": self.get_image(0, 0),
            "kill_1": self.get_image(320, 0),
            "kill_2": self.get_image(640, 0),
            "kill_3": self.get_image(960, 0),
            "kill_4": self.get_image(1280, 0),
        }
        self.image = pygame.image.load("SPRITE/UNIT_BASE.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = 540-25
        self.rect.y = 650
        self.dirx = 0
        self.diry = 0
        self.angle = 0
        
        self.speed = 3
        self.dmg = 10
        self.vision = 200

        # la direction initiale est vers le curseur de la souris au moment du spawn
        x, y = pygame.mouse.get_pos()
        self.direction(x, y)

    def get_image(self, x, y):
        image = pygame.Surface([320, 320])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 320, 320))
        return image

    def direction(self, x, y):
        angle = self.jeu.calculate_angle(self.rect.x, self.rect.y, x, y)
        self.dirx = self.speed * math.cos(angle)
        self.diry = self.speed * math.sin(angle)

    def check_direction(self):
        # l'unité se dirige vers le hero si il est en range de vision
        if self.jeu.calculate_distance(self, self.hero) < self.vision:
            self.direction(self.hero.rect.x, self.hero.rect.y)

    def move(self):

        # verifie si on change de direction
        self.check_direction()
        # si collision avel le hero ou une balle : DED + animation
        if self.jeu.collision(self, self.jeu.grp_bullet):
            self.kill()
            self.jeu.grp_anim_k.add(AnimKillUnit(self, self.jeu))
        if self.jeu.collision(self, self.jeu.grp_hero):
            self.kill()
            self.jeu.grp_anim_k.add(AnimKillUnit(self, self.jeu))
            # si le hero n'est pas déjà en animation de dégat (= frame d'invicibilité) alors dégats + animation
            if not self.hero.dmg_taken:
                self.hero.dmg_taken = True
                self.jeu.damage(self.hero, self.dmg)
                self.hero.anim_dmg("hero_dmg")
        else:
            self.rect.y += self.diry
            self.rect.x += self.dirx
            self.out_screen()
            # self.rotate()

    """def rotate(self): # non fonctionnelle
        self.angle += 0.1
        self.angle = self.jeu.calculate_angle(self.hero.rect.x,
                                              self.hero.rect.y,
                                              self.rect.x,
                                              self.rect.y
                                              )
        self.image = pygame.transform.rotate(self.image, self.angle)"""

    def out_screen(self):
        if self.rect.y < 0 or self.rect.x < 0 or self.rect.x > 1080:
            self.kill()
            print("unit out")


class UnitNest(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("SPRITE/UNIT_NEST.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.center = (540, 650)
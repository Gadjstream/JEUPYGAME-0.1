import pygame
import math


class Bullet(pygame.sprite.Sprite):

    def __init__(self, hero, jeu):
        super().__init__()
        self.hero = hero
        self.jeu = jeu

        self.sprite_sheet = pygame.image.load("SPRITE/BULLET.png")
        self.sprites = {
            "bullet": self.get_image(0, 0),
            "explode": self.get_image(32, 0)
        }
        self.image = self.sprites["bullet"]
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = self.hero.rect.x + 30
        self.rect.y = self.hero.rect.y + 30
        self.dirx = 0
        self.diry = 0
        self.angle = 0
        self.initial_position = []
        self.initial_pos()

        self.speed = 5

        self.direction()

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def direction(self):

        # s'il y a des unités dans l'arène
        if self.jeu.grp_unit.sprites():

            # si une unité est suffisamment proche, le hero tire vers elle
            for unit in self.jeu.grp_unit:
                if self.jeu.calculate_distance(self.hero, unit) < self.hero.vision:

                    x = unit.rect.x
                    y = unit.rect.y
                    angle = self.jeu.calculate_angle(self.rect.x, self.rect.y, x, y)
                    self.dirx = self.speed * math.cos(angle)
                    self.diry = self.speed * math.sin(angle)

                # sinon, il tire en ligne droite
                else:
                    self.dirx = 0
                    self.diry = self.speed
        else:
            self.dirx = 0
            self.diry = self.speed

    def move(self):

        # si collision avec une unit
        if self.jeu.collision(self, self.jeu.grp_unit):
            self.kill()

        # au bout de la range
        if self.jeu.calculate_distance(self.hero, self) > self.hero.range:
            self.kill()
        else:
            # mouvement
            self.rect.x += self.dirx
            self.rect.y += self.diry

    def initial_pos(self):
        self.initial_position = self.rect.x, self.rect.y


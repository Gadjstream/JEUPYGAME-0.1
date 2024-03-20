import pygame


class AnimKillUnit(pygame.sprite.Sprite):

    def __init__(self, unit, jeu):
        super().__init__()
        self.unit = unit
        self.jeu = jeu
        self.image = self.unit.image
        self.image.set_colorkey([0, 0, 0])
        self.rect = unit.rect

        self.update_anim = 1

    def boum(self, nom):
        self.image = self.unit.sprites[nom]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([0, 0, 0])

    def anim_kill(self):
        n = self.update_anim
        if n < 5:
            self.boum("kill_" + str(n))
            self.update_anim += 1
        else:
            self.jeu.grp_anim_k.remove(self)
            self.update_anim = 1


class AnimKillHero(pygame.sprite.Sprite):

    def __init__(self, hero, jeu):
        super().__init__()
        self.hero = hero
        self.jeu = jeu
        self.image = self.hero.image
        self.image.set_colorkey([0, 0, 0])
        self.rect = hero.rect

        self.update_anim = 1

    def boum(self, nom):
        self.image = self.hero.sprites[nom]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([0, 0, 0])

    def anim_kill(self):
        n = self.update_anim
        if n < 4:
            self.boum("tp" + str(n))
            self.update_anim += 1
        else:
            self.jeu.grp_anim_k.remove(self)
            self.update_anim = 1
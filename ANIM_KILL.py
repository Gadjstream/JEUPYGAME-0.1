import pygame


class AnimKillUnit(pygame.sprite.Sprite):

    # Gère l'animation de mort des unités

    def __init__(self, unit, jeu):
        super().__init__()

        # Définition des objets hero et jeu
        self.unit = unit
        self.jeu = jeu

        # Chargement de l'image initiale, transparence, et sa position dans l'espace
        self.image = self.unit.image
        self.image.set_colorkey([0, 0, 0])
        self.rect = unit.rect

        # variable pour parcourir la sprite sheet à partir du 2e sprite
        self.update_anim = 1

    def boum(self, nom):  # Récupère les images dans la sprite sheet
        self.image = self.unit.sprites[nom]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([0, 0, 0])

    def anim_kill(self):  # fait défiler les images de l'animation, puis effece le sprite
        n = self.update_anim
        if n < 5:
            self.boum("kill_" + str(n))
            self.update_anim += 1
        else:
            self.jeu.grp_anim_k.remove(self)
            self.update_anim = 1


class AnimKillHero(pygame.sprite.Sprite):

    # Gère l'animation de mort du hero

    def __init__(self, hero, jeu):
        super().__init__()

        # Définition des objets hero et jeu
        self.hero = hero
        self.jeu = jeu

        # Chargement de l'image initiale, transparence, et sa position dans l'espace
        self.image = self.hero.image
        self.image.set_colorkey([0, 0, 0])
        self.rect = hero.rect

        # variable pour parcourir la sprite sheet à partir du 2e sprite
        self.update_anim = 1

    def boum(self, nom): # Récupère les images dans la sprite sheet
        self.image = self.hero.sprites[nom]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([0, 0, 0])

    def anim_kill(self): # fait défiler les images de l'animation, puis effece le sprite
        n = self.update_anim
        if n < 4:
            self.boum("tp" + str(n))
            self.update_anim += 1
        else:
            self.jeu.grp_anim_k.remove(self)
            self.update_anim = 1
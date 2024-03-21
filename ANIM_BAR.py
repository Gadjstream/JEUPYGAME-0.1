import pygame


class SpawnBar:

    # Gère l'animation de la spawn bar

    def __init__(self):

        # Gestion du temps
        self.start = pygame.time.get_ticks()
        self.time = pygame.time.get_ticks()

        # Dimansion de la barre
        self.haut = 12
        self.large = 100

        # Variable d'animation
        self.anim = 0

        # Couleur de la barre
        self.color = (198, 152, 197)

    def update(self, screen, cd):

        # Gère l'animation

        # tant que l'animation n'est pas terminée
        if self.anim < self.large:

            # chronometre et mesure la taille de la barre
            self.time = pygame.time.get_ticks() - self.start
            self.anim = min(self.time / cd * self.large, self.large)

            # dessine la barre
            pygame.draw.rect(screen, self.color, (540-200, 720-12, self.anim, self.haut))

        else:

            # reset l'animation
            self.anim = 0
            self.start = pygame.time.get_ticks()
            print("reset anim")


class HPBar:

    # Gère la barre de vie du hero

    def __init__(self, hero):

        # Définition du hero
        self.hero = hero

        # Dimansion de la barre
        self.haut = 100
        self.large = 15

        # Couleur de la barre
        self.color = (127, 184, 128)
        self.color_bg = (15, 15, 15)

        # Switch background
        self.bg = False

    def update(self, screen):

        # Dessine le background 1 seule fois
        if not self.bg:
            pygame.draw.rect(screen, self.color_bg, (10 - 1, 10, self.large + 2, self.haut))
        else:
            pass

        # Dessine la barre d'hp
        pygame.draw.rect(screen, self.color, (10, 10 + self.hero.hp_missing, self.large, self.hero.hp))
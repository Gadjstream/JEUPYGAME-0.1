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

    def anim_spawn(self, screen, cd):

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



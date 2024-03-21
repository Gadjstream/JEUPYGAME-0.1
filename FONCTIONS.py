import math
import pygame
from ANIM_KILL import AnimKillHero
from UNIT import Unit
from BULLET import Bullet
from ANIM_BAR import SpawnBar


# Initialisation des événements personnalisés (gestion du temps et cooldowns)
NUM_USEREVENT = 6
custom_events = [pygame.USEREVENT + i + 1 for i in range(NUM_USEREVENT)]
CD, CD_H_MOVE, CD_FIN, FIN_ANIM_DMG, CD_REPOSITION, CD_ATTACK_SPEED = custom_events


class Fonctions():

    # Fonctions principales du jeu
    def __init__(self, hero, screen, LARGE, HAUT):

        # switch entre le gameplay principal et les menus
        self.is_running = False
        self.menu_game = False

        # Création des groupes de sprites
        self.grp_hero = pygame.sprite.Group()
        self.hero = hero
        self.grp_hero.add(self.hero)
        self.grp_unit = pygame.sprite.Group()
        self.grp_anim_k = pygame.sprite.Group()
        self.grp_bullet = pygame.sprite.Group()

        # création de l'animation spawn bar
        self.spawn_bar = SpawnBar()

        # variables principales (écran, dimensions...)
        self.screen = screen
        self.LARGE = LARGE
        self.HAUT = HAUT
        self.CENTER = LARGE/2, HAUT/2

        # variables pour déclencher le début d'un cooldown
        self.cd_anim_k = False
        self.cd_spawn = False

        # vitesse de spawn des unités
        self.cd_spawn_time = 2000

    def run(self, screen):

        # Boucle de gameplay principale

        # tant que le hero est en vie, il est affiché et bouge
        if self.hero.hero_alive:
            screen.blit(self.hero.image, self.hero.rect)
            self.hero.move()

        # Si le hero meurt, il disparait
        elif not self.hero.hero_alive:
            self.hero.kill()

        # les unités sont affichées et bougent
        self.grp_unit.draw(screen)
        for unit in self.grp_unit:
            unit.move()
        self.grp_anim_k.draw(screen)

        # si une entité meurt, une animation est lancée
        for anim in self.grp_anim_k:
            anim.anim_kill()

        # les balles apparaissent à l'écran
        self.grp_bullet.draw(screen)
        for bullet in self.grp_bullet:
            bullet.move()

        # gestion de la fonction pour faire tirer le hero automatiquement
        if self.hero.tire:
            self.tire()
            self.hero.tire = False
            pygame.time.set_timer(CD_ATTACK_SPEED, self.hero.attack_speed)

        # spawn automatique des unités
        if not self.cd_spawn:
            self.grp_unit.add(Unit(self.hero, self))
            self.cd_spawn = True
            pygame.time.set_timer(CD, self.cd_spawn_time)

        # Animation de la barre de spawn
        self.spawn_bar.anim_spawn(self.screen, self.cd_spawn_time)

        # gestion des événements
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()

            # gestions des inputs (voir fonction dédiée)
            elif events.type == pygame.KEYDOWN:
                self.gestion_input()

            # gestion des cooldowns :

            # CD de spawn des entités
            elif events.type == CD:
                if self.cd_spawn:
                    self.cd_spawn = False
                    print("spawn")

            # CD de changement de direction du hero
            elif events.type == CD_H_MOVE:
                if not self.hero.update_hero:
                    self.hero.update_hero = True

            # CD de repositionnement quand le hero s'approche trop du bord de la map
            elif events.type == CD_REPOSITION:
                self.hero.reposition = False

            # délai avant l'apparition du menu à la fin de la boucle de gameplay
            elif events.type == CD_FIN:
                self.is_running = False
                self.menu_game = True

            # durée de l'animation (et frame d'invicibilité) du héro
            elif events.type == FIN_ANIM_DMG:
                self.hero.dmg_taken = False
                self.hero.anim_dmg("hero")

            # Gestion de l'attack speed du hero
            elif events.type == CD_ATTACK_SPEED:
                self.hero.tire = True

    def gestion_input(self):

        # Gestion des inputs
        pressed = pygame.key.get_pressed()

        # La barre espace met pause (toggle)
        if pressed[pygame.K_SPACE]:
            if self.is_running:
                self.is_running = False
            elif not self.is_running: # MARCHE PAS ?
                self.is_running = True

        # La touche "a" affiche la distance entre le hero et l'unita qui a passé le plus de temps à l'écran
        if pressed[pygame.K_a]:
            print(self.calculate_distance(self.hero, self.grp_unit.sprites()[0]))

    def calculate_angle(self, x1, y1, x2, y2): # Calcule une direction ed'un point A vers un point B
        return math.atan2(y2-y1, x2-x1)

    def calculate_distance(self, entity1, entity2):  # calcule la distance entre 2 sprites
        x1, y1 = entity1.rect.x, entity1.rect.y
        x2, y2 = entity2.rect.x, entity2.rect.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def collision(self, sprite, grp_sprite):  # vérifie si un sprite entre en collision avec un groupe de sprite
        return pygame.sprite.spritecollide(sprite, grp_sprite, False, pygame.sprite.collide_mask)

    def damage(self, entity, n):

        # Gère et monitore les dégats infligés
        entity.hp -= n
        print("le hero a perdu " + str(n) + " hp")
        print("hp :", entity.hp)

        # Si les pv du héro sont à O, il meurt
        if entity.hp <= 0:
            entity.hp = 0
            print("le hero est DED")
            self.hero.hero_alive = False

            # Animation de TP du héro
            self.grp_anim_k.add(AnimKillHero(self.hero, self))

            # Fin de la boucle de gameplay dans 1 seconde
            pygame.time.set_timer(CD_FIN, 1000)

    def tire(self):  # Crée une balle dans le groupe de sprites dédié
        self.grp_bullet.add(Bullet(self.hero, self))



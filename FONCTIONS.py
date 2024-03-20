import math
import pygame
from ANIM_KILL import AnimKillHero
from UNIT import Unit
from BULLET import Bullet

NUM_USEREVENT = 6
custom_events = [pygame.USEREVENT + i + 1 for i in range(NUM_USEREVENT)]
CD, CD_H_MOVE, CD_FIN, FIN_ANIM_DMG, CD_REPOSITION, CD_ATTACK_SPEED = custom_events

class Fonctions():
    def __init__(self, hero, LARGE, HAUT):

        self.is_running = False
        self.menu_game = False

        self.grp_hero = pygame.sprite.Group()
        self.hero = hero
        self.grp_hero.add(self.hero)
        self.grp_unit = pygame.sprite.Group()
        self.grp_anim_k = pygame.sprite.Group()
        self.grp_bullet = pygame.sprite.Group()

        self.LARGE = LARGE
        self.HAUT = HAUT
        self.CENTER = LARGE/2, HAUT/2

        self.cd_anim_k = False
        self.cd_spawn = False

        
    def run(self, screen):
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
        if self.hero.tire:
            self.tire()
            self.hero.tire = False
            pygame.time.set_timer(CD_ATTACK_SPEED, self.hero.attack_speed)

        if not self.cd_spawn:
            self.grp_unit.add(Unit(self.hero, self))
            self.cd_spawn = True
            pygame.time.set_timer(CD, 2000)



        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
            elif events.type == pygame.KEYDOWN:
                self.gestion_input()
            elif events.type == CD:
                if self.cd_spawn:
                    self.cd_spawn = False
            elif events.type == CD_H_MOVE:
                if not self.hero.update_hero:
                    self.hero.update_hero = True
            elif events.type == CD_FIN:
                self.is_running = False
                self.menu_game = True
            elif events.type == FIN_ANIM_DMG:
                self.hero.dmg_taken = False
                self.hero.anim_dmg("hero")
            elif events.type == CD_REPOSITION:
                self.hero.reposition = False
            elif events.type == CD_ATTACK_SPEED:
                self.hero.tire = True

    def gestion_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            if self.is_running:
                self.is_running = False
            elif not self.is_running:
                self.is_running = True
        if pressed[pygame.K_a]:
            print(self.calculate_distance(self.hero, self.grp_unit.sprites()[0]))

    def calculate_angle(self, x1, y1, x2, y2):
        return math.atan2(y2-y1, x2-x1)

    def calculate_distance(self, entity1, entity2):
        x1, y1 = entity1.rect.x, entity1.rect.y
        x2, y2 = entity2.rect.x, entity2.rect.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def collision(self, sprite, grp_sprite):
        return pygame.sprite.spritecollide(sprite, grp_sprite, False, pygame.sprite.collide_mask)

    def damage(self, entity, n):
        entity.hp -= n
        print("le hero a perdu " + str(n) + " hp")
        print("hp :", entity.hp)
        if entity.hp <= 0:
            entity.hp = 0
            print("le hero est DED")
            self.hero.hero_alive = False
            self.grp_anim_k.add(AnimKillHero(self.hero, self))
            pygame.time.set_timer(CD_FIN, 1000)

    def tire(self):
        self.grp_bullet.add(Bullet(self.hero, self))



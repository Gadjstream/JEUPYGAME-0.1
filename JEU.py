import pygame
from HERO import Hero
from FONCTIONS import Fonctions
from UNIT import UnitNest
LARGE = 1080
HAUT = 720

DBLUE = (50, 50, 120)


pygame.init()

pygame.display.set_caption("OUI")
screen = pygame.display.set_mode((LARGE, HAUT))
bg = pygame.image.load("SPRITE/MAP.png")

btn_go = pygame.image.load("BTN/BTN_GO.png")
btn_go_i = pygame.image.load("BTN/BTN_GO_I.png")
btn_go_rect = btn_go.get_rect()
btn_go_rect.center = (LARGE/2, HAUT/2)

bg_txt = pygame.image.load("SPRITE/BG_TXT.png")
bg_txt_rect = bg_txt.get_rect()
bg_txt_rect.center = (LARGE/2, HAUT/2)

txt = pygame.font.SysFont("impact", 25)

msg_menu_game = txt.render("Well done ! You spooked it !", False, DBLUE)


hero = Hero()
jeu = Fonctions(hero, LARGE, HAUT)
nest_1 = UnitNest()

running = True

while running:

    screen.blit(bg, (0, 0))

    if jeu.is_running:
        jeu.run(screen)
        screen.blit(nest_1.image, nest_1.rect)
    elif jeu.menu_game:
        screen.blit(bg_txt, bg_txt_rect)
        bg_txt.blit(msg_menu_game,(30,50))
    else:
        if btn_go_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(btn_go_i, btn_go_rect)
        else:
            screen.blit(btn_go, btn_go_rect)

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
            break
        elif events.type == pygame.MOUSEBUTTONDOWN:
            if btn_go_rect.collidepoint(events.pos):
                jeu.is_running = True

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

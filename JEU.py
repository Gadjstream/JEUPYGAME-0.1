import pygame
from HERO import Hero
from FONCTIONS import Fonctions
from UNIT import UnitNest

# dimensions de l'écran
LARGE = 1080
HAUT = 720

# couleur du texte
DBLUE = (50, 50, 120)

# initialisation de pygame et du background
pygame.init()

pygame.display.set_caption("OUI")
screen = pygame.display.set_mode((LARGE, HAUT))
bg = pygame.image.load("SPRITE/MAP.png")

# initialisation du bouton GO
btn_go = pygame.image.load("BTN/BTN_GO.png")
btn_go_i = pygame.image.load("BTN/BTN_GO_I.png")
btn_go_rect = btn_go.get_rect()
btn_go_rect.center = (LARGE/2, HAUT/2)

# initialisation du texte
bg_txt = pygame.image.load("SPRITE/BG_TXT.png")
bg_txt_rect = bg_txt.get_rect()
bg_txt_rect.center = (LARGE/2, HAUT/2)

txt = pygame.font.SysFont("impact", 25)

msg_menu_game = txt.render("Well done ! You spooked it !", False, DBLUE)

# création du héro, du jeu et du 1er nid
hero = Hero()
jeu = Fonctions(hero, screen, LARGE, HAUT)
nest_1 = UnitNest()

# boucle principale
running = True

while running:

    # actualisation du background
    screen.blit(bg, (0, 0))

    # Fonction à exécuter pendant le gameplay principal
    if jeu.is_running:
        jeu.run(screen)
        screen.blit(nest_1.image, nest_1.rect)

    # Fonction à exécuter quand le menu 1 est activé
    elif jeu.menu_game:
        screen.blit(bg_txt, bg_txt_rect)
        bg_txt.blit(msg_menu_game,(30,50))

    # Menu principal
    else:
        if btn_go_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(btn_go_i, btn_go_rect)
        else:
            screen.blit(btn_go, btn_go_rect)

    # gestion des événements pendant le menu principal
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
            break
        elif events.type == pygame.MOUSEBUTTONDOWN:
            if btn_go_rect.collidepoint(events.pos):
                jeu.is_running = True

    # Actualisation de l'écran à 60 fps
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

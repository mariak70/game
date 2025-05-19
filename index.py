import pygame
from pygame.sprite import Group

import controls
from gun import Gun
from scores import Scores
from stats import Stats


def run():
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption('Космические защитники')
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    inos = Group()
    controls.create_army(screen, inos)
    stats = Stats()
    sc = Scores(screen, stats)

    while True:
        controls.events(screen, gun, bullets)
        if stats.run_game:
            gun.update_gun()
            controls.update(bg_color, screen, stats, sc, gun, inos, bullets)
            controls.update_bullets(screen, stats, sc, inos, bullets)
            controls.update_inos(stats, screen, sc, gun, inos, bullets)


run()

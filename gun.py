import pygame
from pygame.sprite import Sprite


class Gun(Sprite):

    def __init__(self, screen: object, speed: float = 1.5) -> object:
        ''' инициализация пушки'''
        super(Gun, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/pixil-frame-0.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.mright = False
        self.mleft = False
        self.speed = speed

    def output(self):
        '''отрисовывать пушку'''
        self.screen.blit(self.image, self.rect)


    def update_gun(self):
        '''обновлеение позиции пушки'''
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += self.speed
        elif self.mleft and self.rect.left > 0:
            self.center -= self.speed

        self.rect.centerx = self.center

    def creaty_gun(self):
        '''размещаем пушку по центру вниз'''
        self.center = self. screen_rect.centerx
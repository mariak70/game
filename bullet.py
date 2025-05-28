import pygame
class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen, gun, speed=4.5):
        '''создаем пулю в позиции пушки'''
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = 255, 242, 0
        self.speed = speed
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update(self):
        '''пермещение пули'''
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        '''рисуем пулю н экране'''
        pygame.draw.rect(self.screen, self.color, self.rect)
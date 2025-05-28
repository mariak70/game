
import pygame
import sys
from bullet import Bullet
from ino import Ino
import time
import random

def events(screen, gun, bullets, bullet_speed=4.5):
    """ обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            #вправо
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                gun.mright = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                gun.mleft = True
            elif event.key == pygame.K_SPACE:
                if len(bullets) < 5:  # Ограничение на количество пуль
                    new_bullet = Bullet(screen, gun, bullet_speed)
                    bullets.add(new_bullet)
            elif event.key == pygame.K_ESCAPE:
                return 'pause'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                gun.mright = False
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                gun.mleft = False
    return None

def update(bg_color, screen, stats, sc, gun, inos, bullets):
    '''обновление экрана с анимациями'''
    # Создаём градиентный фон
    for y in range(600):
        color_intensity = int(y / 600 * 30)
        color = (color_intensity, color_intensity // 2, color_intensity + 10)
        pygame.draw.line(screen, color, (0, y), (700, y))
    
    # Добавляем звёзды на фон
    for _ in range(20):
        x = random.randint(0, 700)
        y = random.randint(0, 600)
        brightness = random.randint(100, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)
    
    sc.show_score()
    
    # Анимация пуль с эффектом следа
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        # Добавляем эффект следа
        for i in range(3):
            trail_y = bullet.rect.y + (i + 1) * 4
            alpha = 255 - (i * 80)
            if trail_y < 600:
                trail_color = (255, 242 - i * 50, 0)
                pygame.draw.circle(screen, trail_color, 
                                 (bullet.rect.centerx, trail_y), 1)
    
    gun.output()
    inos.draw(screen)
    
    # Добавляем эффекты взрыва
    create_explosion_effects(screen)
    
    pygame.display.flip()

# Глобальная переменная для эффектов взрыва
explosion_effects = []

def create_explosion_effects(screen):
    """Создаёт и отображает эффекты взрыва"""
    global explosion_effects
    
    # Обновляем существующие эффекты
    for effect in explosion_effects[:]:
        effect['timer'] -= 1
        if effect['timer'] <= 0:
            explosion_effects.remove(effect)
        else:
            # Рисуем частицы взрыва
            for particle in effect['particles']:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.1  # Гравитация
                alpha = int(255 * (effect['timer'] / 30))
                color = (255, alpha, 0) if alpha > 0 else (255, 0, 0)
                pygame.draw.circle(screen, color, 
                                 (int(particle['x']), int(particle['y'])), 2)

def add_explosion(x, y):
    """Добавляет эффект взрыва в указанной позиции"""
    global explosion_effects
    
    particles = []
    for _ in range(10):
        particles.append({
            'x': x + random.randint(-5, 5),
            'y': y + random.randint(-5, 5),
            'vx': random.uniform(-3, 3),
            'vy': random.uniform(-5, -1)
        })
    
    explosion_effects.append({
        'particles': particles,
        'timer': 30
    })

def update_bullets(screen, stats, sc, inos, bullets, current_level):
    '''обновление позиции пуль с улучшениями'''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for collision_point in collisions:
            # Добавляем эффект взрыва в точке попадания
            add_explosion(collision_point.rect.centerx, collision_point.rect.centery)
            
        for inos_hit in collisions.values():
            stats.score += (10 + current_level * 5) * len(inos_hit)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    
    if len(inos) == 0:
        bullets.empty()
        return 'level_complete'
    
    return None

def gun_kill(stats, screen, sc, gun, inos, bullets):
    '''столкновение пушки и армии'''
    if stats.guns_left > 0:
        stats.guns_left -= 1
        sc.image_guns()
        inos.empty()
        bullets.empty()
        gun.creaty_gun()
        time.sleep(1)
    else:
        stats.run_game = False
        return 'game_over'
    return None

def update_inos(stats, screen, sc, gun, inos, bullets):
    '''обновляет позиции пришельцев'''
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        return gun_kill(stats, screen, sc, gun, inos, bullets)
    return inos_check(stats, screen, sc, gun, inos, bullets)

def inos_check(stats, screen, sc, gun, inos, bullets):
    '''проверка добрались ли до края'''
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            return gun_kill(stats, screen, sc, gun, inos, bullets)
    return None

def create_army(screen, inos, rows=5):
    '''создание армии пришельцев с переменным количеством рядов'''
    ino = Ino(screen)
    ino_width = ino.rect.width
    number_ino_x = int((700 - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height
    
    for row_number in range(rows):
        for ino_number in range(number_ino_x):
            new_ino = Ino(screen)
            new_ino.x = ino_width + ino_width * ino_number
            new_ino.y = ino_height + ino_height * row_number
            new_ino.rect.x = new_ino.x
            new_ino.rect.y = new_ino.rect.height + (new_ino.rect.height * row_number)
            inos.add(new_ino)

def check_high_score(stats, sc):
    '''проверка новых рекордов'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.high_score))


import pygame
import sys
import math
import random

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = (5, 5, 30)
        self.title_color = (255, 255, 100)
        self.button_color = (50, 50, 150)
        self.button_hover_color = (80, 80, 200)
        self.text_color = (255, 255, 255)
        
        # Шрифты
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Анимация звёзд
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, 700),
                'y': random.randint(0, 600),
                'speed': random.uniform(0.5, 2.0),
                'brightness': random.randint(50, 255)
            })
        
        # Анимация заголовка
        self.title_offset = 0
        self.title_direction = 1
        
        # Кнопки
        self.buttons = [
            {'text': 'НОВАЯ ИГРА', 'rect': pygame.Rect(250, 250, 200, 60), 'action': 'new_game'},
            {'text': 'УРОВНИ', 'rect': pygame.Rect(250, 330, 200, 60), 'action': 'levels'},
            {'text': 'РЕКОРДЫ', 'rect': pygame.Rect(250, 410, 200, 60), 'action': 'scores'},
            {'text': 'ВЫХОД', 'rect': pygame.Rect(250, 490, 200, 60), 'action': 'quit'}
        ]
        
        self.selected_button = 0
        self.mouse_pos = (0, 0)

    def update_animation(self):
        # Анимация звёзд
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > 600:
                star['y'] = 0
                star['x'] = random.randint(0, 700)
        
        # Анимация заголовка
        self.title_offset += self.title_direction * 0.5
        if self.title_offset > 10 or self.title_offset < -10:
            self.title_direction *= -1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(self.buttons):
                    if button['rect'].collidepoint(event.pos):
                        return button['action']
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    return self.buttons[self.selected_button]['action']
        return None

    def draw(self):
        # Фон
        self.screen.fill(self.bg_color)
        
        # Звёзды
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), 1)
        
        # Заголовок с анимацией
        title_text = self.title_font.render("КОСМИЧЕСКИЕ ЗАЩИТНИКИ", True, self.title_color)
        title_rect = title_text.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.y = 50 + self.title_offset
        self.screen.blit(title_text, title_rect)
        
        # Кнопки
        for i, button in enumerate(self.buttons):
            is_hovered = button['rect'].collidepoint(self.mouse_pos) or i == self.selected_button
            color = self.button_hover_color if is_hovered else self.button_color
            
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, self.text_color, button['rect'], 2)
            
            text = self.button_font.render(button['text'], True, self.text_color)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

class LevelSelect:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = (5, 5, 30)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        self.levels = [
            {'name': 'ЛЁГКИЙ', 'unlocked': True},
            {'name': 'СРЕДНИЙ', 'unlocked': True},
            {'name': 'СЛОЖНЫЙ', 'unlocked': True},
            {'name': 'ЭКСПЕРТ', 'unlocked': True},
            {'name': 'КОШМАР', 'unlocked': True}
        ]
        
        self.selected_level = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
                elif event.key == pygame.K_UP:
                    self.selected_level = (self.selected_level - 1) % len(self.levels)
                elif event.key == pygame.K_DOWN:
                    self.selected_level = (self.selected_level + 1) % len(self.levels)
                elif event.key == pygame.K_RETURN:
                    if self.levels[self.selected_level]['unlocked']:
                        return f'start_level_{self.selected_level}'
        return None

    def draw(self):
        self.screen.fill(self.bg_color)
        
        title = self.font.render("ВЫБОР УРОВНЯ", True, (255, 255, 100))
        title_rect = title.get_rect(centerx=self.screen_rect.centerx, y=50)
        self.screen.blit(title, title_rect)
        
        for i, level in enumerate(self.levels):
            y = 150 + i * 70
            color = (255, 255, 255) if level['unlocked'] else (100, 100, 100)
            if i == self.selected_level and level['unlocked']:
                color = (255, 255, 100)
            
            text = self.font.render(f"{i+1}. {level['name']}", True, color)
            text_rect = text.get_rect(centerx=self.screen_rect.centerx, y=y)
            self.screen.blit(text, text_rect)
            
            if i == self.selected_level:
                pygame.draw.rect(self.screen, (100, 100, 200), 
                               (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10), 2)

class GameOver:
    def __init__(self, screen, score, level):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_color = (20, 0, 0)
        self.font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 48)
        self.score = score
        self.level = level
        self.alpha = 0
        self.fade_speed = 3

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 'menu'
                elif event.key == pygame.K_r:
                    return f'restart_level_{self.level}'
        return None

    def update(self):
        if self.alpha < 255:
            self.alpha += self.fade_speed

    def draw(self):
        # Затемнение экрана
        overlay = pygame.Surface((700, 600))
        overlay.set_alpha(min(self.alpha, 150))
        overlay.fill(self.bg_color)
        self.screen.blit(overlay, (0, 0))
        
        if self.alpha > 100:
            # Текст Game Over
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, (255, 50, 50))
            game_over_rect = game_over_text.get_rect(centerx=self.screen_rect.centerx, y=200)
            self.screen.blit(game_over_text, game_over_rect)
            
            # Счёт
            score_text = self.small_font.render(f"СЧЁТ: {self.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(centerx=self.screen_rect.centerx, y=280)
            self.screen.blit(score_text, score_rect)
            
            # Инструкции
            restart_text = self.small_font.render("R - ПОВТОР  SPACE - МЕНЮ", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(centerx=self.screen_rect.centerx, y=350)
            self.screen.blit(restart_text, restart_rect)

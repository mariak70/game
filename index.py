
import pygame
import controls
from gun import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores
from menu import Menu, LevelSelect, GameOver
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption('Космические защитники v2.0')
        self.clock = pygame.time.Clock()
        self.bg_color = (0, 0, 0)
        
        # Состояния игры
        self.state = 'menu'
        self.menu = Menu(self.screen)
        self.level_select = LevelSelect(self.screen)
        self.game_over_screen = None
        
        # Игровые объекты
        self.gun = None
        self.bullets = None
        self.inos = None
        self.stats = None
        self.sc = None
        self.current_level = 0
        
        # Настройки уровней
        self.level_configs = [
            {'name': 'ЛЁГКИЙ', 'ino_speed': 0.05, 'bullet_speed': 5.0, 'gun_speed': 2.0, 'ino_rows': 3},
            {'name': 'СРЕДНИЙ', 'ino_speed': 0.08, 'bullet_speed': 4.5, 'gun_speed': 1.8, 'ino_rows': 4},
            {'name': 'СЛОЖНЫЙ', 'ino_speed': 0.12, 'bullet_speed': 4.0, 'gun_speed': 1.5, 'ino_rows': 5},
            {'name': 'ЭКСПЕРТ', 'ino_speed': 0.15, 'bullet_speed': 3.5, 'gun_speed': 1.2, 'ino_rows': 6},
            {'name': 'КОШМАР', 'ino_speed': 0.2, 'bullet_speed': 3.0, 'gun_speed': 1.0, 'ino_rows': 7}
        ]

    def init_game(self, level=0):
        """Инициализация игры для указанного уровня"""
        self.current_level = level
        self.gun = Gun(self.screen, self.level_configs[level]['gun_speed'])
        self.bullets = Group()
        self.inos = Group()
        self.stats = Stats()
        self.sc = Scores(self.screen, self.stats)
        
        # Применяем настройки уровня
        config = self.level_configs[level]
        controls.create_army(self.screen, self.inos, config['ino_rows'])
        
        # Устанавливаем скорости для объектов
        for ino in self.inos:
            ino.speed = config['ino_speed']

    def handle_menu(self):
        """Обработка главного меню"""
        action = self.menu.handle_events()
        
        if action == 'new_game':
            self.init_game(0)
            self.state = 'playing'
        elif action == 'levels':
            self.state = 'level_select'
        elif action == 'scores':
            self.show_high_scores()
        elif action == 'quit':
            return False
        
        self.menu.update_animation()
        self.menu.draw()
        return True

    def handle_level_select(self):
        """Обработка выбора уровня"""
        action = self.level_select.handle_events()
        
        if action == 'menu':
            self.state = 'menu'
        elif action == 'quit':
            return False
        elif action and action.startswith('start_level_'):
            level = int(action.split('_')[-1])
            self.init_game(level)
            self.state = 'playing'
        
        self.level_select.draw()
        return True

    def handle_game_over(self):
        """Обработка экрана окончания игры"""
        action = self.game_over_screen.handle_events()
        
        if action == 'menu':
            self.state = 'menu'
        elif action == 'quit':
            return False
        elif action and action.startswith('restart_level_'):
            level = int(action.split('_')[-1])
            self.init_game(level)
            self.state = 'playing'
        
        self.game_over_screen.update()
        self.game_over_screen.draw()
        return True

    def handle_playing(self):
        """Обработка игрового процесса"""
        controls.events(self.screen, self.gun, self.bullets, self.level_configs[self.current_level]['bullet_speed'])
        
        if self.stats.run_game:
            self.gun.update_gun()
            controls.update(self.bg_color, self.screen, self.stats, self.sc, self.gun, self.inos, self.bullets)
            controls.update_bullets(self.screen, self.stats, self.sc, self.inos, self.bullets, self.current_level)
            result = controls.update_inos(self.stats, self.screen, self.sc, self.gun, self.inos, self.bullets)
            
            if result == 'game_over':
                self.game_over_screen = GameOver(self.screen, self.stats.score, self.current_level)
                self.state = 'game_over'
            elif result == 'level_complete':
                if self.current_level < len(self.level_configs) - 1:
                    self.init_game(self.current_level + 1)
                else:
                    # Игра пройдена полностью
                    self.show_victory_screen()
        else:
            self.game_over_screen = GameOver(self.screen, self.stats.score, self.current_level)
            self.state = 'game_over'
        
        return True

    def show_high_scores(self):
        """Показать таблицу рекордов"""
        # Простая реализация показа рекордов
        self.state = 'menu'

    def show_victory_screen(self):
        """Показать экран победы"""
        self.state = 'menu'

    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            if self.state == 'menu':
                running = self.handle_menu()
            elif self.state == 'level_select':
                running = self.handle_level_select()
            elif self.state == 'playing':
                running = self.handle_playing()
            elif self.state == 'game_over':
                running = self.handle_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()

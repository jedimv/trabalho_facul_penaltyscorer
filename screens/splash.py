import pygame
from screens.main_menu import MainMenu
from constants import BLACK, WHITE


class SplashScreen:
    def __init__(self, game):
        self.game = game
        self.timer = 0
        self.duration = 2000

    def update(self, dt):
        self.timer += dt
        if self.timer > self.duration:
            self.game.current_screen = MainMenu(self.game)

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont(None, 80)
        text = font.render("Helamam", True, WHITE)
        rect = text.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2))
        surface.blit(text, rect)

    def handle_event(self, event):
        pass

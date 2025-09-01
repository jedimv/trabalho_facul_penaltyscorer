# main_menu.py
import pygame
from ui.button import Button
from screens.tournament_selection import TournamentSelection
from constants import BLACK, WHITE
import math

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button((300, 250, 200, 50), "Novo Jogo", self.start_new_game),
            Button((300, 350, 200, 50), "Sair", self.quit_game)
        ]
        self.title_font = pygame.font.Font(None, 80)
        self.bg_color = (20, 20, 40)

    def start_new_game(self):
        self.game.current_screen = TournamentSelection(self.game)

    def quit_game(self):
        pygame.quit()
        exit()

    def update(self, dt):
        pass

    def draw(self, surface):
        for y in range(surface.get_height()):
            color = (self.bg_color[0] + y // 10, self.bg_color[1] + y // 10, self.bg_color[2] + y // 5)
            pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))

        title_text = self.title_font.render("Menu Principal", True, WHITE)
        pulse_y = 150 + int(5 * math.sin(pygame.time.get_ticks() / 300))
        surface.blit(title_text, (surface.get_width() // 2 - title_text.get_width() // 2, pulse_y))

        for btn in self.buttons:
            shadow_rect = btn.rect.move(4, 4)
            pygame.draw.rect(surface, (0,0,0,100), shadow_rect, border_radius=8)
            btn.draw(surface)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

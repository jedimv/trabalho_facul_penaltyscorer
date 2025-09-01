import pygame
from ui.button import Button
from screens.tournament_selection import TournamentSelection
from constants import BLACK, WHITE


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button((300, 250, 200, 50), "Novo Jogo", self.start_new_game),
            Button((300, 350, 200, 50), "Sair", self.quit_game)
        ]

    def start_new_game(self):
        self.game.current_screen = TournamentSelection(self.game)

    def quit_game(self):
        pygame.quit()
        exit()

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont(None, 60)
        text = font.render("Menu Principal", True, WHITE)
        surface.blit(text, (250, 150))
        for btn in self.buttons:
            btn.draw(surface)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

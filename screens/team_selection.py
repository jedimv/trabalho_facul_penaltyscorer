import pygame
from ui.button import Button
from screens.game_screen import GameScreen
from constants import BLACK, WHITE
import random


class TeamSelection:
    def __init__(self, game, tournament):
        self.game = game
        self.tournament = tournament
        self.teams = [f"Time {i + 1}" for i in range(64)]
        self.selected = 0
        self.buttons = [
            Button((300, 500, 200, 50), "Ir para o jogo", self.start_game)
        ]
        self.bracket = self.generate_bracket()

    def generate_bracket(self):
        teams = self.teams.copy()
        random.shuffle(teams)
        return [(teams[i], teams[i + 1]) for i in range(0, 64, 2)]

    def start_game(self):
        self.game.current_screen = GameScreen(self.game, self.teams[self.selected], self.bracket)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        title = font.render(f"Torneio: {self.tournament}", True, WHITE)
        surface.blit(title, (180, 50))

        for idx, t in enumerate(self.teams):
            color = WHITE if idx == self.selected else (180, 180, 180)
            txt = pygame.font.SysFont(None, 35).render(t, True, color)
            surface.blit(txt, (300, 150 + idx * 30))

        for btn in self.buttons:
            btn.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                self.selected = min(len(self.teams) - 1, self.selected + 1)
        for btn in self.buttons:
            btn.handle_event(event)

import pygame
from ui.button import Button
from screens.team_selection import TeamSelection
from constants import BLACK, WHITE


class TournamentSelection:
    def __init__(self, game):
        self.game = game
        self.tournaments = ["Copa dos 64 Times"]
        self.selected = 0
        self.buttons = [
            Button((300, 400, 200, 50), "Selecionar", self.select_tournament)
        ]

    def select_tournament(self):
        self.game.current_screen = TeamSelection(self.game, self.tournaments[self.selected])

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont(None, 60)
        text = font.render("Selecione o Torneio", True, WHITE)
        surface.blit(text, (180, 100))
        for idx, t in enumerate(self.tournaments):
            color = WHITE if idx == self.selected else (180, 180, 180)
            txt = pygame.font.SysFont(None, 50).render(t, True, color)
            surface.blit(txt, (300, 200 + idx * 60))
        for btn in self.buttons:
            btn.draw(surface)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

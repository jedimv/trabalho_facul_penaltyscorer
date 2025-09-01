# team_selection.py
import pygame
from ui.button import Button
from screens.game_screen import GameScreen
from constants import BLACK, WHITE
import random

class TeamSelection:
    def __init__(self, game, tournament="Torneio Local"):
        self.game = game
        self.tournament = tournament
        self.teams = [f"Time {i + 1}" for i in range(64)]
        self.selected = 0
        self.buttons = [
            Button((300, 500, 200, 50), "Ir para o jogo", self.start_game)
        ]
        self.bracket = self.generate_bracket()
        self.title_font = pygame.font.Font(None, 60)
        self.item_font = pygame.font.Font(None, 35)
        self.offset_y = 0

    def update_scroll(self):
        visible_height = 400
        selected_y = self.selected * 30
        if selected_y - self.offset_y > visible_height:
            self.offset_y = selected_y - visible_height
        elif selected_y - self.offset_y < 0:
            self.offset_y = selected_y

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

        title = self.title_font.render(f"Torneio: {self.tournament}", True, WHITE)
        surface.blit(title, (surface.get_width()//2 - title.get_width()//2, 50))

        for idx, t in enumerate(self.teams):
            y_pos = 150 + idx * 30 - self.offset_y
            if idx == self.selected:
                highlight_rect = pygame.Rect(280, y_pos - 2, 240, 32)
                pygame.draw.rect(surface, (0, 150, 255), highlight_rect, border_radius=5)
                color = WHITE
            else:
                color = (180, 180, 180)
            txt = self.item_font.render(t, True, color)
            surface.blit(txt, (300, y_pos))

        # Desenhar botões
        for btn in self.buttons:
            # sombra
            shadow_rect = btn.rect.move(4, 4)
            pygame.draw.rect(surface, (0,0,0,100), shadow_rect, border_radius=8)
            btn.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
                self.update_scroll()
            elif event.key == pygame.K_DOWN:
                self.selected = min(len(self.teams) - 1, self.selected + 1)
                self.update_scroll()
        for btn in self.buttons:
            btn.handle_event(event)
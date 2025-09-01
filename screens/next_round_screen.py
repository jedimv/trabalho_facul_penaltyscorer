import pygame
from constants import BLACK, WHITE

class NextRoundScreen:
    def __init__(self, game, winner, next_opponent):
        self.game = game
        self.winner = winner
        self.next_opponent = next_opponent
        self.timer = 2000
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.timer:
            from screens.game_screen import GameScreen
            self.game.current_screen = GameScreen(self.game, self.winner, self.next_opponent)

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render(f"Vencedor: {self.winner}", True, WHITE)
        surface.blit(text, (200, 300))
        subtext = font.render(f"Próximo adversário: {self.next_opponent}", True, WHITE)
        surface.blit(subtext, (150, 400))

    def handle_event(self, event):
        pass
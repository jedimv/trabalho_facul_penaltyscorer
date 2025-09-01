import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from objects import Goal, Ball

class GameScreen:
    def __init__(self, game, player_team, bracket):
        self.game = game
        self.player_team = player_team
        self.bracket = bracket

        # Cenário
        self.bg = pygame.image.load("assets/gfx/shootout_bg.png").convert()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Objetos do gol
        self.goal = Goal()  # ajustar posição conforme sua tela

        # Bola
        self.ball = Ball(400, 630)

        # Mira
        self.aim_x = 400
        self.aim_y = 300
        self.direction = 1
        self.speed = 3

    def update(self, dt):
        # Movimentação da mira
        self.aim_x += self.speed * self.direction
        if self.aim_x > SCREEN_WIDTH - 200 or self.aim_x < 200:
            self.direction *= -1

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.goal.draw(surface)
        self.ball.draw(surface)
        # Desenhar a mira
        pygame.draw.line(surface, WHITE,
                         (self.aim_x, self.ball.rect.y),
                         (self.aim_x, self.goal.goal_area.top), 5)
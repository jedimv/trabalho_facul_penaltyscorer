import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Goal:
    def __init__(self):
        self.goal_post = pygame.image.load("assets/gfx/goal_post.png").convert_alpha()
        self.goal_net = pygame.image.load("assets/gfx/goal_net.png").convert_alpha()
        self.goal_post = pygame.transform.scale(self.goal_post, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.goal_net = pygame.transform.scale(self.goal_net, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # não redimensiona

        # Rects para colisão: apenas a área real do gol
        # Supondo que o gol esteja centralizado na tela
        goal_width = 200   # largura do gol "real"
        goal_height = 100  # altura do gol "real"
        goal_x = (SCREEN_WIDTH - goal_width) // 2
        goal_y = 100  # altura do gol na tela

        self.goal_area = pygame.Rect(goal_x, goal_y, goal_width, goal_height)
        self.left_post = pygame.Rect(goal_x, goal_y, 10, goal_height)
        self.right_post = pygame.Rect(goal_x + goal_width - 10, goal_y, 10, goal_height)

    def draw(self, surface):
        surface.blit(self.goal_net, (0,0))   # cobre o cenário
        surface.blit(self.goal_post, (0,0))  # sobreposição da trave

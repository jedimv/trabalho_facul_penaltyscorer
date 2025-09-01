import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Goal:
    def __init__(self):
        self.goal_post = pygame.image.load("assets/gfx/goal_post.png").convert_alpha()
        self.goal_net = pygame.image.load("assets/gfx/goal_net.png").convert_alpha()
        self.goal_post = pygame.transform.scale(self.goal_post, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.goal_net = pygame.transform.scale(self.goal_net, (SCREEN_WIDTH, SCREEN_HEIGHT))

        goal_width, goal_height = 360, 120
        goal_x = 220
        goal_y = 240
        self.goal_area = pygame.Rect(goal_x, goal_y, goal_width, goal_height)
        self.top_post = pygame.Rect(215, 235, goal_width + 10, 5)
        self.left_post = pygame.Rect(215, goal_y, 5, goal_height)
        self.right_post = pygame.Rect(580, goal_y, 5, goal_height)

    def draw(self, surface):
        surface.blit(self.goal_net, (0,0))
        surface.blit(self.goal_post, (0,0))

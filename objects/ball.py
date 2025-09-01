import pygame


class Ball:
    def __init__(self, x=400, y=400):
        self.image = pygame.image.load("assets/gfx/ball.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

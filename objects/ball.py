import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.mixer.init()
SOUND_TRAVE = pygame.mixer.Sound("assets/sfx/ball_post.wav")

class Ball:
    def __init__(self, x=400, y=540):
        self.original_image = pygame.image.load("assets/gfx/ball.png").convert_alpha()
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = self.original_image.get_rect(center=(x, y))
        self.on_ground = False
        self.gravity = 500
        self.gol = False
        self.encaixada = False

    def update(self, dt, goal=None):
        if self.on_ground:
            return

        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if goal:
            if self.rect.colliderect(goal.left_post):
                SOUND_TRAVE.play()
                self.velocity.x = abs(self.velocity.x) * 0.5
                self.pos.x = goal.left_post.right + self.rect.width // 2
                self.rect.centerx = int(self.pos.x)
            elif self.rect.colliderect(goal.right_post):
                SOUND_TRAVE.play()
                self.velocity.x = -abs(self.velocity.x) * 0.5
                self.pos.x = goal.right_post.left - self.rect.width // 2
                self.rect.centerx = int(self.pos.x)
            elif self.rect.colliderect(goal.top_post):
                SOUND_TRAVE.play()
                if self.velocity.y < 0:
                    self.velocity.y = -self.velocity.y * 0.5
                self.pos.y = goal.top_post.bottom + self.rect.height / 2
                self.rect.centery = int(self.pos.y)
            elif self.rect.colliderect(goal.goal_area):
                if self.pos.y > 350:
                    self.pos.y = 350
                    self.rect.centery = int(self.pos.y)
                    self.velocity.y *= 0.5
                    self.velocity.x *= 0.5

            if self.rect.colliderect(goal.goal_area):
                if self.pos.y > SCREEN_HEIGHT - 50:
                    self.pos.y = SCREEN_HEIGHT - 50
                    self.velocity = pygame.Vector2(0, 0)
                    self.on_ground = True

        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface):
        scale_factor = 0.5 + 0.5 * (self.pos.y / SCREEN_HEIGHT)
        scaled_width = int(self.original_image.get_width() * scale_factor)
        scaled_height = int(self.original_image.get_height() * scale_factor)
        scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

        rect = scaled_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surface.blit(scaled_image, rect.topleft)

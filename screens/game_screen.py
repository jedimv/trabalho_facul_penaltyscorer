import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from objects import Goal, Ball, Goalkeeper

SOUND_REDE = pygame.mixer.Sound("assets/sfx/ball_net.wav")

class GameScreen:
    def __init__(self, game, player_team, bracket):
        self.game = game
        self.player_team = player_team
        self.bracket = bracket

        self.bg = pygame.image.load("assets/gfx/shootout_bg.png").convert()
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.goal = Goal()
        self.ball = Ball(400, 540)

        self.aim_x = SCREEN_WIDTH // 2
        self.aim_y = 360
        self.direction = 1
        self.speed = 5

        self.power = 0
        self.max_power = 100
        self.final_power = None
        self.power_direction = 1
        self.power_speed = 120

        self.phase = "aim"
        self.click_processed = False
        self.shot_direction = None
        self.last_update = pygame.time.get_ticks()

        self.goalkeeper = Goalkeeper(self.goal)

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_update) / 1000.0

        if self.phase == "aim":
            self.aim_x += self.speed * self.direction
            if self.aim_x > SCREEN_WIDTH - 200 or self.aim_x < 200:
                self.direction *= -1
        elif self.phase == "power":
            self.power += self.power_speed * elapsed_time * self.power_direction
            if self.power >= self.max_power:
                self.power = self.max_power
                self.power_direction = -1
            elif self.power <= 0:
                self.power = 0
                self.power_direction = 1

        if self.phase == "shoot" or self.ball.velocity.length() > 0:
            self.ball.update(dt, goal=self.goal)

        self.ball.update(dt, goal=self.goal)
        self.goalkeeper.update(dt)
        self.last_update = current_time

        if self.ball.rect.colliderect(self.goal.goal_area) and not self.ball.gol:
            if self.ball.pos.y > 350:
                print("Gol!")
                SOUND_REDE.play()
                self.ball.gol = True
            elif self.ball.rect.colliderect(self.goalkeeper.rect):
                print("Bola encaixada pelo goleiro!")
                self.ball.velocity = pygame.Vector2(0, 0)
                self.ball.encaixada = True
                self.ball.pos.x = self.goalkeeper.pos.x
                self.ball.pos.y = self.goalkeeper.pos.y - self.goalkeeper.height // 4
                self.ball.rect.center = (int(self.ball.pos.x), int(self.ball.pos.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.click_processed:
            self.click_processed = True

            mouse_x, mouse_y = event.pos
            if self.phase == "aim":
                ball_center = pygame.Vector2(self.ball.pos.x, self.ball.pos.y)
                aim_point = pygame.Vector2(self.aim_x, self.aim_y)
                self.shot_direction = (aim_point - ball_center).normalize()
                self.phase = "power"
                self.power = 0
                self.power_direction = 1
                self.last_update = pygame.time.get_ticks()
            elif self.phase == "power":
                self.final_power = self.power
                self.phase = "shoot"
                self.shoot_ball()
                self.goalkeeper.jump_to(mouse_x)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.click_processed = False

    def shoot_ball(self):
        force_factor = self.final_power / self.max_power
        base_speed = 0.5
        added_speed = 0.05 * force_factor
        self.ball.velocity = self.shot_direction * (base_speed + added_speed)
        self.ball.velocity.y -= 0.03 * force_factor

    def draw(self, surface):
        bar_y = SCREEN_HEIGHT - 100
        surface.blit(self.bg, (0, 0))
        self.goal.draw(surface)
        self.ball.draw(surface)
        pygame.draw.rect(surface, (255, 255, 0), self.goalkeeper.rect, 2)

        pygame.draw.rect(surface, (255, 0, 0), self.goal.left_post, 2)
        pygame.draw.rect(surface, (0, 0, 255), self.goal.right_post, 2)
        pygame.draw.rect(surface, (0, 255, 0), self.goal.goal_area, 2)
        pygame.draw.rect(surface, (0, 255, 255), self.goal.top_post, 2)

        if self.phase == "aim":
            pygame.draw.line(surface, (255, 255, 0),
                             (int(self.ball.pos.x), int(self.ball.pos.y)),
                             (self.aim_x, self.aim_y), 5)
            font = pygame.font.SysFont(None, 36)
            text = font.render("Clique para definir a direção;", True, (255, 255, 255))
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, bar_y - 40))
        elif self.phase == "power":
            bar_width, bar_height = 300, 30
            bar_x = (SCREEN_WIDTH - bar_width) // 2
            pygame.draw.rect(surface, (50, 50, 50), (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10),
                             border_radius=5)
            pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), border_radius=3)
            fill_width = int((self.power / self.max_power) * bar_width)
            if fill_width > 0:
                pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, fill_width, bar_height), border_radius=3)
            pygame.draw.rect(surface, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=3)
            font = pygame.font.SysFont(None, 36)
            text = font.render("Clique para definir a força;", True, (255, 255, 255))
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, bar_y - 40))

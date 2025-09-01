import pygame, random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from objects import Goal, Ball, Goalkeeper

SOUND_REDE = pygame.mixer.Sound("assets/sfx/ball_net.wav")
SOUND_GOAL = pygame.mixer.Sound("assets/sfx/goal.wav")
SOUND_MISS = pygame.mixer.Sound("assets/sfx/miss.wav")

class GameScreen:
    def __init__(self, game, player_team, bracket):
        self.game = game
        self.player_team = player_team
        self.ai_team = 'Bot'
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
        self.is_ai_keeping = True
        self.is_ai_kicking = False
        self.ta_score = 0
        self.tb_score = 0
        self.turn = 0
        self.max_turns = 10
        self.alternates = 2
        self.alternates_active = False

        self.reason = ''
        self.in_wait = False
        self.delay = 150
        self.ai_decision_time = None
        self.ai_chosen_target = None
        self.ai_chosen_power = 0

        self.goalkeeper = Goalkeeper(self.goal)

        self.bottom_string = ''

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_update) / 1000.0

        if self.is_ai_kicking:
            if self.phase == "aim" and self.ai_decision_time is None:
                self.ai_decision_time = pygame.time.get_ticks() + random.randint(500, 1200)
                self.ai_chosen_target = pygame.Vector2(random.randint(200, SCREEN_WIDTH - 200),
                                                       random.randint(300, 360))
                self.ai_chosen_power = random.randint(30, 100)

            if self.ai_decision_time and pygame.time.get_ticks() >= self.ai_decision_time:
                ball_center = pygame.Vector2(self.ball.pos.x, self.ball.pos.y)
                self.shot_direction = (self.ai_chosen_target - ball_center).normalize()
                self.final_power = self.ai_chosen_power
                self.phase = "shoot"
                self.shoot_ball()  # sem target_x
                self.ai_decision_time = None

        elif not self.is_ai_kicking:
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

        self.ball.update(dt, goal=self.goal)
        self.goalkeeper.update(dt)
        self.last_update = current_time

        if self.ball.rect.colliderect(self.goalkeeper.rect):
            if not self.ball.encaixada and not self.ball.gol:
                SOUND_MISS.play()
                self.ball.velocity = pygame.Vector2(0, 0)
                self.ball.encaixada = True

                if self.is_ai_kicking:
                    self.on_miss(self.ai_team)
                elif not self.is_ai_kicking:
                    self.on_miss(self.player_team)

            if self.ball.encaixada:
                self.ball.pos.x = self.goalkeeper.pos.x
                self.ball.pos.y = self.goalkeeper.pos.y - self.goalkeeper.height // 4
                self.ball.rect.center = (int(self.ball.pos.x), int(self.ball.pos.y))

        if self.ball.rect.colliderect(self.goal.goal_area):
            if self.ball.pos.y > 340:
                if not self.ball.gol:
                    SOUND_REDE.play()
                    SOUND_GOAL.play()
                    self.ball.gol = True

                    if self.is_ai_kicking:
                        self.on_goal(self.ai_team)
                    elif not self.is_ai_kicking:
                        self.on_goal(self.player_team)

        if self.in_wait:
            self.delay -= 1
            if self.delay <= 0:
                self.in_wait = False
                self.turn += 1

                if not self.alternates_active:
                    if self.turn >= self.max_turns:
                        if self.ta_score == self.tb_score:
                            self.alternates_active = True
                            self.turn = 1
                        else:
                            self.end_match()
                else:
                    if self.turn >= self.alternates:
                        if self.ta_score != self.tb_score:
                            self.end_match()
                        else:
                            self.turn = 1  # mesma lógica

                if self.reason == 'player_goal':
                    self.reset_ball()
                    self.is_ai_kicking = True
                    self.ta_score += 1
                elif self.reason == 'player_miss':
                    self.reset_ball()
                    self.is_ai_kicking = True
                elif self.reason == 'ai_goal':
                    self.reset_ball()
                    self.is_ai_kicking = False
                    self.tb_score += 1
                elif self.reason == 'ai_miss':
                    self.reset_ball()
                    self.is_ai_kicking = False

    def reset_ball(self):
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

        self.reason = ''
        self.in_wait = False
        self.delay = 150

        self.goalkeeper.reset_position()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.click_processed:
            self.click_processed = True
            mouse_x, mouse_y = event.pos

            if not self.is_ai_kicking:
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
            elif self.is_ai_kicking and self.phase in ["aim", "power", "shoot"]:
                self.goalkeeper.jump_to(mouse_x)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.click_processed = False

    def shoot_ball(self, target_x=None):
        force_factor = self.final_power / self.max_power
        base_speed = 0.5
        added_speed = 0.05 * force_factor
        self.ball.velocity = self.shot_direction * (base_speed + added_speed)
        self.ball.velocity.y -= 0.03 * force_factor

        if target_x is not None and not self.is_ai_kicking:
            self.goalkeeper.jump_to(target_x)

    def on_goal(self, team):
        if team == self.player_team:
            self.in_wait = True
            self.reason = 'player_goal'
            print("gol do player")
        else:
            self.in_wait = True
            self.reason = 'ai_goal'
            print("gol do bot")

    def on_miss(self, team):
        if team == self.player_team:
            self.in_wait = True
            self.reason = 'player_miss'
            print("player perdeu o penalti")
        else:
            self.in_wait = True
            self.reason = 'ai_miss'
            print("bot perdeu o penalti")

    def end_match(self):
        if self.ta_score > self.tb_score:
            winner = self.player_team
        else:
            winner = self.ai_team
        print(f"Partida encerrada! Vencedor: {winner}")

        self.advance_bracket(winner)

    def advance_bracket(self, winner):
        next_opponent = None
        if hasattr(self.bracket, "opponents") and len(self.bracket.opponents) > 0:
            next_opponent = self.bracket.opponents.pop(0)

        from screens.next_round_screen import NextRoundScreen
        self.game.current_screen = NextRoundScreen(self.game, winner, next_opponent)

    def draw(self, surface):
        bar_y = SCREEN_HEIGHT - 100
        surface.blit(self.bg, (0, 0))
        self.goal.draw(surface)
        self.ball.draw(surface)
        self.goalkeeper.draw(surface)

        pygame.draw.rect(surface, (255, 255, 0), self.goalkeeper.rect, 2)
        pygame.draw.rect(surface, (255, 0, 0), self.goal.left_post, 2)
        pygame.draw.rect(surface, (0, 0, 255), self.goal.right_post, 2)
        pygame.draw.rect(surface, (0, 255, 0), self.goal.goal_area, 2)
        pygame.draw.rect(surface, (0, 255, 255), self.goal.top_post, 2)

        ta = pygame.font.SysFont(None, 36)
        tb = pygame.font.SysFont(None, 36)
        tu = pygame.font.SysFont(None, 36)

        tta = ta.render(f'Time A:{self.ta_score}', True, (255, 255, 255))
        surface.blit(tta, (32, 32))

        ttb = tb.render(f'Time B:{self.tb_score}', True, (255, 255, 255))
        surface.blit(ttb, (32, 64))

        ttu = tu.render(f'Turn:{self.turn}', True, (255, 255, 255))
        surface.blit(ttu, (32, 96))

        font = pygame.font.SysFont(None, 36)

        if self.is_ai_kicking:
            self.bottom_string = "Bot vai chutar!!"

        if self.phase == "aim":
            pygame.draw.line(surface, (255, 255, 0),
                             (int(self.ball.pos.x), int(self.ball.pos.y)),
                             (self.aim_x, self.aim_y), 5)
            self.bottom_string = "Clique para definir a mira!"
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

            self.bottom_string = "Clique para definir a força!"

        text = font.render(self.bottom_string, True, (255, 255, 255))
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, bar_y - 40))
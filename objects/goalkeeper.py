import pygame


class Goalkeeper:
    def __init__(self, goal):
        self.width = 50
        self.height = 100
        self.goal = goal

        self.pos = pygame.Vector2(goal.goal_area.centerx, 360 - self.height / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.pos

        self.gravity = 1000
        self.ground_y = 360 - self.height / 2
        self.on_ground = True
        self.jump_power = 1
        self.friction = 0.9

        self.angle = 0
        self.angular_velocity = 0
        self.rotation_damping = 0.95

        self.sprite = pygame.image.load("assets/gfx/chars/goalie.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def jump_to(self, target_x):
        direction_x = target_x - self.pos.x
        force = min(1.0, abs(direction_x) / 200)

        self.velocity.x = direction_x * 0.00174
        self.velocity.y = -self.jump_power * (0.5 + force * 0.5)

        self.angular_velocity = -direction_x / 15
        self.on_ground = False

    def update(self, dt):
        if not self.on_ground:
            self.velocity.y += self.gravity * dt

            self.pos += self.velocity * dt

            self.angle += self.angular_velocity * dt
            self.angular_velocity *= self.rotation_damping

            if self.pos.y >= self.ground_y:
                self.pos.y = self.ground_y

                if self.velocity.y > 100:
                    self.velocity.y = -self.velocity.y * 0.3
                    self.angular_velocity *= 0.8
                else:
                    self.velocity.y = 0
                    self.on_ground = True

                    self.velocity.x *= self.friction
                    self.angular_velocity *= 0.7

                    if abs(self.velocity.x) < 5:
                        self.velocity.x = 0
        else:
            if abs(self.angle) > 0.5:
                self.angle *= 0.9
            else:
                self.angle = 0

        min_x = self.goal.goal_area.left + self.width / 2
        max_x = self.goal.goal_area.right - self.width / 2
        self.pos.x = max(min_x, min(max_x, self.pos.x))

        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface):
        gk_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        pygame.draw.rect(gk_surface, (70, 130, 180), (0, 0, self.width, self.height), border_radius=10)
        pygame.draw.circle(gk_surface, (240, 200, 160), (self.width // 2, self.height // 4), 15)  # Cabeça

        arm_y = self.height // 2
        pygame.draw.rect(gk_surface, (70, 130, 180), (0, arm_y, self.width // 3, self.height // 4), border_radius=5)
        pygame.draw.rect(gk_surface, (70, 130, 180), (self.width * 2 // 3, arm_y, self.width // 3, self.height // 4),border_radius=5)

        ## tentativa falha de fazer o goleiro 'tombar'
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surface.blit(rotated_sprite, rotated_rect.topleft)

    def reset_position(self):
        self.pos.x = self.goal.goal_area.centerx
        self.pos.y = self.goal.goal_area.top + self.height // 2
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.velocity = pygame.Vector2(0, 0)
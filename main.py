import pygame
import sys
from screens.splash import SplashScreen
from constants import FPS


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Penalty Fever Clone")
        self.clock = pygame.time.Clock()
        self.current_screen = SplashScreen(self)

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if hasattr(self.current_screen, "handle_event"):
                    self.current_screen.handle_event(event)

            if hasattr(self.current_screen, "update"):
                self.current_screen.update(dt)
            if hasattr(self.current_screen, "draw"):
                self.current_screen.draw(self.screen)

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()

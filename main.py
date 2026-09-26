import pygame
import sys
import config
from entities import Boat, Hook, Fish, init_assets

class FishingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("A Fish In My Life")
        
        init_assets()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.boat = Boat(config.WIDTH // 2 - 40, 100)
        self.hook = Hook(self.boat.x + 40, 130)
        self.fishes = [Fish() for _ in range(5)]
        
        self.score = 0
        self.caught_fish = None
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.hook.state == "IDLE":
                    self.hook.state = "DROPPING"

    def update(self):
        keys = pygame.key.get_pressed()
        
        if self.hook.state == "IDLE":
            self.boat.move(left=keys[pygame.K_LEFT], right=keys[pygame.K_RIGHT])

        self.hook.update(self.boat.x)

        if self.hook.state == "RETRACTING":
            if self.caught_fish:
                self.caught_fish.x = self.hook.x - (self.caught_fish.width // 2)
                self.caught_fish.y = self.hook.y

            if self.hook.y <= 130:
                self.hook.state = "IDLE"
                if self.caught_fish:
                    self.score += self.caught_fish.score_value
                    self.caught_fish.reset_position()
                    self.caught_fish = None

        for fish in self.fishes:
            if fish != self.caught_fish:
                fish.move()

                if self.caught_fish is None and self.hook.state != "IDLE":
                    if self.hook.get_rect().colliderect(fish.get_rect()):
                        self.caught_fish = fish
                        self.hook.state = "RETRACTING"

    def draw(self):
        self.screen.fill(config.SKY_BLUE)
        pygame.draw.rect(self.screen, config.OCEAN_BLUE, (0, 140, config.WIDTH, config.HEIGHT - 140))

        self.hook.draw(self.screen, self.boat.x)
        self.boat.draw(self.screen)
        
        for fish in self.fishes:
            fish.draw(self.screen)

        score_text = self.font.render(f"Skor: {self.score}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(config.FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = FishingGame()
    game.run()
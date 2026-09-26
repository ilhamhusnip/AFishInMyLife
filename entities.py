import pygame
import random
import config
from utils import load_and_scale_fish

FISH_CONFIG = {}

def init_assets():
    global FISH_CONFIG
    FISH_CONFIG = {
        "small": {
            "image": load_and_scale_fish("fish_small.png", scale_factor=1.5),
            "score": 10,
            "speed_range": (2, 4),
        },
        "medium": {
            "image": load_and_scale_fish("fish_medium.png", scale_factor=1.8),
            "score": 25,
            "speed_range": (3, 5),
        },
        "rare": {
            "image": load_and_scale_fish("fish_rare.png", scale_factor=1.7),
            "score": 60,
            "speed_range": (5, 7),
        },
    }

class Hook:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = config.HOOK_SPEED
        self.state = "IDLE"

    def update(self, boat_x):
        if self.state == "IDLE":
            self.x = boat_x + 40
            self.y = 130
        elif self.state == "DROPPING":
            self.y += self.speed
            if self.y >= config.HEIGHT - 20:
                self.state = "RETRACTING"
        elif self.state == "RETRACTING":
            self.y -= self.speed

    def draw(self, surface, boat_x):
        pygame.draw.line(surface, config.WHITE, (boat_x + 40, 130), (self.x, self.y), 2)
        pygame.draw.circle(surface, config.HOOK_GRAY, (self.x, self.y), 5)

    def get_rect(self):
        return pygame.Rect(self.x - 5, self.y - 5, 10, 10)

class Boat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = config.BOAT_SPEED
        self.width = 80
        self.height = 40

    def move(self, left=False, right=False):
        if left and self.x > 0:
            self.x -= self.speed
        if right and self.x < config.WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, config.BOAT_BROWN, (self.x, self.y, self.width, self.height))

class Fish:
    def __init__(self):
        self.reset_position()

    def reset_position(self):
        choice = random.choices(["small", "medium", "rare"], weights=config.FISH_SPAWN_WEIGHTS)[0]
        cfg = FISH_CONFIG[choice]

        self.type = choice
        self.base_image = cfg["image"]
        self.score_value = cfg["score"]
        self.width = self.base_image.get_width()
        self.height = self.base_image.get_height()

        self.moving_right = random.choice([True, False])
        if self.moving_right:
            self.x = -self.width - 20
            self.speed = random.randint(*cfg["speed_range"])
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            self.x = config.WIDTH + 20
            self.speed = -random.randint(*cfg["speed_range"])
            self.image = self.base_image

        self.y = random.randint(220, config.HEIGHT - self.height - 20)

    def move(self):
        self.x += self.speed
        if self.speed > 0 and self.x > config.WIDTH + 50:
            self.reset_position()
        elif self.speed < 0 and self.x < -self.width - 50:
            self.reset_position()

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
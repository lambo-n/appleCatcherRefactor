import pygame
import random
import os


class Apple(pygame.sprite.Sprite):
    """A falling apple. Coordinates live in the fixed 500x500 game canvas."""

    _img = None
    SIZE = 40

    def __init__(self, difficulty):
        super().__init__()
        if difficulty == 1:
            self.speed = random.uniform(1.5, 3)
        elif difficulty == 3:
            self.speed = random.uniform(2.5, 5)
        else:
            self.speed = random.uniform(4, 8)

        self.image = pygame.transform.scale(self.get_img(), (self.SIZE, self.SIZE))
        self.rect = self.image.get_rect(topleft=(random.randint(0, 460), -30))
        # rect coords are ints; keep a float for sub-pixel fall speed.
        self._y = float(self.rect.y)

    @classmethod
    def get_img(cls):
        if cls._img is None:
            path = os.path.join("assets", "apple.png")
            cls._img = pygame.image.load(path).convert_alpha()
        return cls._img

    def update(self):
        self._y += self.speed
        self.rect.y = round(self._y)

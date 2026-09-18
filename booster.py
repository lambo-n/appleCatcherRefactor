import pygame
import random


class Booster(pygame.sprite.Sprite):
    """A falling speed booster. Coordinates live in the 500x500 game canvas."""

    SIZE = 40
    _font = None

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 230, 0), self.image.get_rect())
        label = self.get_font().render("S", True, (0, 120, 255))
        self.image.blit(label, label.get_rect(center=(self.SIZE / 2, self.SIZE / 2)))
        self.rect = self.image.get_rect(center=(random.randint(30, 470), -20))
        # rect coords are ints; keep a float for sub-pixel fall speed.
        self._y = float(self.rect.centery)
        self.fallSpeed = 4

    @classmethod
    def get_font(cls):
        if cls._font is None:
            cls._font = pygame.font.Font(None, 25)
        return cls._font

    def update(self):
        self._y += self.fallSpeed
        self.rect.centery = round(self._y)

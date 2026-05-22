import pygame
import random
import os


class Apple:
    _img = None

    def __init__(self, difficulty):
        self.applex = random.randint(0, 460)
        self.appley = -30
        if difficulty == 1:
            self.speed = random.uniform(1.5, 3)
        elif difficulty == 3:
            self.speed = random.uniform(2.5, 5)
        else:
            self.speed = random.uniform(4, 8)
        self.size = 40

    @classmethod
    def get_img(cls):
        if cls._img is None:
            path = os.path.join("assets", "apple.png")
            cls._img = pygame.image.load(path).convert_alpha()
        return cls._img

    def move(self):
        self.appley += self.speed

    def display(self, screen):
        img = pygame.transform.scale(self.get_img(), (self.size, self.size))
        screen.blit(img, (int(self.applex), int(self.appley)))

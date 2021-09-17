import pygame

pygame.init()


class Square:
    def __init__(self, letter, number, screen):
        self.letter = letter
        self.number = number
        self.screen = screen
        self.screenx = screen.get_width()
        self.screeny = screen.get_height()
        self.x = (letter / 8) * self.screenx
        self.y = ((7/8)-(number/8))*self.screeny
        if (letter+number) % 2 == 1:
            self.color = "white"
        else:
            self.color = "brown"
        self.image = pygame.image.load("../Images/" + self.color + ".png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx/8), int(self.screeny/8)))


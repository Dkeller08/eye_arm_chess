import pygame

pygame.init()
import Board

class Square:
    def __init__(self, letter, number, possibleMove):
        self.letter = letter
        self.number = number
        self.screen = Board.screen
        self.w = Board.w
        self.h = Board.h
        self.x = (letter / 8) * self.w
        self.y = ((7/8)-(number/8))*self.h
        if possibleMove:
            self.color = "green"
        elif (letter+number) % 2 == 1:
            self.color = "white"
        else:
            self.color = "brown"
        self.image = pygame.image.load("../Images/" + self.color + ".png")
        self.image = pygame.transform.scale(self.image, (int(self.w / 8), int(self.h / 8)))


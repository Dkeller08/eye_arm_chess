import pygame

pygame.init()


class Square:
    def __init__(self, letter, number, screen, piece, possibleMove):
        self.piece_bool = False
        self.letter = letter
        self.number = number
        self.screen = screen
        self.piece = piece
        self.possibleMove = possibleMove
        self.screenx = 4 * screen.get_height() / 5
        self.screeny = 4 * screen.get_height() / 5
        self.x = (letter / 8) * self.screenx + (screen.get_width() - self.screenx) / 2
        self.y = ((7 / 8) - (number / 8)) * self.screeny
        if possibleMove:
            self.color = "green"
        elif (letter + number) % 2 == 1:
            self.color = "white"
        else:
            self.color = "brown"
        self.image = pygame.image.load("../Images/" + self.color + ".png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx / 8), int(self.screeny / 8)))

    def has_piece(self):
        if self.piece is None:
            self.piece_bool = False
        else:
            self.piece_bool = True

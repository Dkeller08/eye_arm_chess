import Window
import pygame


class Rook:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_rook.png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx / 8), int(self.screeny / 8)))
        for i in range(8):
            for j in range(8):
                if square.number == i or square.letter == j:
                    Window.squares[i][j].possibleMove = True


class Bishop:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_bishop.png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx / 8), int(self.screeny / 8)))
        for i in range(8):
            for j in range(8):
                if square.number - square.letter == i - j or square.number + square.letter == i + j:
                    Window.squares[i][j].possibleMove = True


class Horse:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_horse.png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx / 8), int(self.screeny / 8)))
        for i in range(8):
            for j in range(8):
                if (abs(square.number - i) == 1 and abs(square.letter == 2)) or (
                        abs(square.number - i) == 2 and abs(square.letter == 1)):
                    Window.squares[i][j].possibleMove = True


class King:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_king.png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx / 8), int(self.screeny / 8)))
        for i in range(8):
            for j in range(8):
                if abs(square.number - i) <= 1 and abs(square.letter <= 1):
                    Window.squares[i][j].possibleMove = True


class Queen:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_queen.png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx / 8), int(self.screeny / 8)))
        for i in range(8):
            for j in range(8):
                if square.number == i or square.letter == j or square.number - square.letter == i - j or square.number + square.letter == i + j:
                    Window.squares[i][j].possibleMove = True


class Pawn:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_pawn.png")
        self.image = pygame.transform.scale(self.image, (int(self.screenx / 8), int(self.screeny / 8)))
        for i in range(8):
            for j in range(8):
                if player == "white":
                    if square.letter == i and (j - square.number == 1 or (j - square.number == 2 and j == 3)):
                        Window.squares[i][j].possibleMove = True
                else:
                    if square.letter == i and (j - square.number == -1 or (j - square.number == -2 and j == 4)):
                        Window.squares[i][j].possibleMove = True

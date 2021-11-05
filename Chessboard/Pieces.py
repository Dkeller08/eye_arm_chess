import pygame
import numpy as np


class Rook:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_rook.png")
        self.board = np.full((8, 8), False)
        self.move = 2
        self.update(letter, number)

    def update(self, letter, number):
        self.letter = letter
        self.move -= 1
        self.number = number
        for i in range(8):
            for j in range(8):
                self.board[i][j] = self.number == j or self.letter == i


class Bishop:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_bishop.png")
        self.board = np.full((8, 8), False)
        self.update(letter, number)

    def update(self, letter, number):
        self.letter = letter
        self.number = number
        for i in range(8):
            for j in range(8):
                self.board[i][j] = self.number - self.letter == j - i or self.number + self.letter == i + j


class Horse:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_horse.png")
        self.board = np.full((8, 8), False)
        self.update(letter, number)

    def update(self, letter, number):
        self.letter = letter
        self.number = number
        for i in range(8):
            for j in range(8):
                self.board[i][j] = (abs(self.number - j) == 1 and abs(self.letter - i) == 2) or (
                        abs(self.number - j) == 2 and abs(self.letter - i) == 1)


class King:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_king.png")
        self.board = np.full((8, 8), False)
        self.move = 2
        self.update(letter, number)

    def update(self, letter, number):
        self.letter = letter
        self.move -= 1
        self.number = number
        for i in range(8):
            for j in range(8):
                self.board[i][j] = abs(self.number - j) <= 1 and abs(self.letter - i) <= 1


class Queen:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_queen.png")
        self.board = np.full((8, 8), False)
        self.update(letter, number)

    def update(self, letter, number):
        self.letter = letter
        self.number = number
        for i in range(8):
            for j in range(8):
                self.board[i][
                    j] = self.number == j or self.letter == i or self.number - self.letter == j - i or self.number + self.letter == i + j


class Pawn:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_pawn.png")
        self.board = np.full((8, 8), False)
        self.move = 2
        self.enpessant = True
        self.update(letter, number)

    def update(self, letter, number):
        self.letter = letter
        self.move -= 1
        self.number = number
        for i in range(8):
            for j in range(8):
                self.board[i][j] = False
                if self.player == "white":
                    if self.letter == i and (j - self.number == 1 or (j - self.number == 2 and j == 3)):
                        self.board[i][j] = True
                else:
                    if self.letter == i and (j - self.number == -1 or (j - self.number == -2 and j == 4)):
                        self.board[i][j] = True

    def enpessant_update(self):
        self.enpessant = False


def starting_position(letter, number):
    if number == 1:
        return Pawn(letter, number, "white")
    if letter == 4 and number == 0:
        return King(letter, number, "white")
    if letter == 3 and number == 0:
        return Queen(letter, number, "white")
    if (letter == 7 or letter == 0) and number == 0:
        return Rook(letter, number, "white")
    if (letter == 1 or letter == 6) and number == 0:
        return Horse(letter, number, "white")
    if (letter == 2 or letter == 5) and number == 0:
        return Bishop(letter, number, "white")

    if number == 6:
        return Pawn(letter, number, "black")
    if letter == 4 and number == 7:
        return King(letter, number, "black")
    if letter == 3 and number == 7:
        return Queen(letter, number, "black")
    if (letter == 7 or letter == 0) and number == 7:
        return Rook(letter, number, "black")
    if (letter == 6 or letter == 1) and number == 7:
        return Horse(letter, number, "black")
    if (letter == 5 or letter == 2) and number == 7:
        return Bishop(letter, number, "black")
    else:
        return None

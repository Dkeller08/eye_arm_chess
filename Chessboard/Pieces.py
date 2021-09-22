import pygame
import numpy as np


class Rook:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_rook.png")
        self.board = np.full((8, 8), False)
        for i in range(8):
            for j in range(8):
                if self.number == i or self.letter == j:
                    self.board[i][j] = True


class Bishop:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_bishop.png")
        self.board = np.full((8, 8), False)
        for i in range(8):
            for j in range(8):
                if self.number - self.letter == i - j or self.number + self.letter == i + j:
                    self.board[i][j] = True


class Horse:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_horse.png")
        self.board = np.full((8, 8), False)
        for i in range(8):
            for j in range(8):
                if (abs(self.number - j) == 1 and abs(self.letter - i) == 2) or (
                        abs(self.number - j) == 2 and abs(self.letter - i) == 1):
                    self.board[i][j] = True


class King:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_king.png")
        self.board = np.full((8, 8), False)
        for i in range(8):
            for j in range(8):
                if abs(self.number - i) <= 1 and abs(self.letter <= 1):
                    self.board[i][j] = True


class Queen:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_queen.png")
        self.board = np.full((8, 8), False)
        for i in range(8):
            for j in range(8):
                if self.number == i or self.letter == j or self.number - self.letter == i - j or self.number + self.letter == i + j:
                    self.board[i][j] = True


class Pawn:
    def __init__(self, letter, number, player):
        self.letter = letter
        self.number = number
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_pawn.png")
        self.board = np.full((8, 8), False)
        for i in range(8):
            for j in range(8):
                if player == "white":
                    if self.letter == i and (j - self.number == 1 or (j - self.number == 2 and j == 3)):
                        self.board[i][j] = True
                else:
                    if self.letter == i and (j - self.number == -1 or (j - self.number == -2 and j == 4)):
                        self.board[i][j] = True


def starting_position(letter, number):
    if letter == 1 and number == 5:
        return Horse(letter, number, "black")
    else:
        return None

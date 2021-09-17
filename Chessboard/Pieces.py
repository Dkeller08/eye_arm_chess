import Window
import pygame


class Rook:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/"+player+"_rook.png")
        for i in range(8):
            for j in range(8):
                if square.number == i or square.letter == j:
                    Window.squares[i][j].possibleMove = True


class Bishop:
    def __init__(self, square, player):
        self.square = square
        self.player = player
        self.image = pygame.image.load("../Images/" + player + "_bishop.png")
        for i in range(8):
            for j in range(8):
                if square.number - square.letter == i - j or square.number + square.letter == i + j:
                    Window.squares[i][j].possibleMove = True

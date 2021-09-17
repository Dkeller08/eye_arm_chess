import pygame
import Board
import numpy as np

# initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("EyeChess")
icon = pygame.image.load("../Images/Logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((600, 600))

# Get board
squares = np.full((8, 8), Board.Square(0, 0, screen))
for i in range(8):
    for j in range(8):
        squares[i][j] = Board.Square(i, j, screen)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(8):
        for j in range(8):
            screen.blit(squares[i][j].image, (int(squares[i][j].x), int(squares[i][j].y)))

    pygame.display.update()

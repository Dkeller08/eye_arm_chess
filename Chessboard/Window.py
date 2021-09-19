import pygame
import Board
import Pieces
import numpy as np

# initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("EyeChess")
icon = pygame.image.load("../Images/Logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((600, 600))

# Get board
squares = np.full((8, 8), Board.Square(0, 0, screen, None, None, False))
for i in range(8):
    for j in range(8):
        piece, color = Pieces.starting_position(i, j)
        squares[i][j] = Board.Square(i, j, screen, piece, color, False)
# Set some constants
mousex, mousey = 20, 20
h, w = screen.get_height(), screen.get_width()

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            squares[int(8 * mousex / w)][int(8 * (h - mousey) / h)] = Board.Square(int(8 * mousex / w),
                                                                                   int(8 * (h - mousey) / h),
                                                                                   screen, squares[int(8 * mousex / w)][
                                                                                       int(8 * (h - mousey) / h)].piece,squares[int(8 * mousex / w)][
                                                                                       int(8 * (h - mousey) / h)].color,
                                                                                   False)
            mousex, mousey = pygame.mouse.get_pos()
            squares[int(8 * mousex / w)][int(8 * (h - mousey) / h)] = Board.Square(int(8 * mousex / w),
                                                                                   int(8 * (h - mousey) / h),
                                                                                   screen, squares[int(8 * mousex / w)][
                                                                                       int(8 * (h - mousey) / h)].piece, squares[int(8 * mousex / w)][
                                                                                       int(8 * (h - mousey) / h)].color,
                                                                                   True)
        if event.type == pygame.QUIT:
            running = False

    for i in range(8):
        for j in range(8):
            screen.blit(squares[i][j].image, (int(squares[i][j].x), int(squares[i][j].y)))
            piece = squares[i][j].piece
            if piece is not None:
                image_piece = pygame.transform.scale(eval("Pieces." + piece)(squares[i][j], squares[i][j].player).image,
                                                     (int(w / 8), int(h / 8)))
                screen.blit(image_piece, (int(squares[i][j].x), int(squares[i][j].y)))

    pygame.display.update()

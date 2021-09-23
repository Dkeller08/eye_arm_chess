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
squares = np.full((8, 8), Board.Square(0, 0, screen, None, False))
for i in range(8):
    for j in range(8):
        piece = Pieces.starting_position(i, j)
        squares[i][j] = Board.Square(i, j, screen, piece, False)
# Set some constants
squarex, squarey = 0, 0
h, w = screen.get_height(), screen.get_width()

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse2x, mouse2y = pygame.mouse.get_pos()
            movex = int(8 * mouse2x / w)
            movey = int(8 * (h - mouse2y) / h)
            if squares[movex][movey].possibleMove:
                squares[movex][movey] = Board.Square(movex, movey, screen, squares[squarex][squarey].piece, False)
                squares[movex][movey].piece.update(movex, movey)
                squares[squarex][squarey] = Board.Square(squarex, squarey, screen, None, False)
            squares[squarex][squarey] = Board.Square(squarex, squarey, screen, squares[squarex][squarey].piece, False)
            mousex, mousey = pygame.mouse.get_pos()
            squarex = int(8 * mousex / w)
            squarey = int(8 * (h - mousey) / h)
            for i in range(8):
                for j in range(8):
                    if squares[squarex][squarey].piece is not None:
                        squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)
                        if squares[squarex][squarey].piece.board[i][j]:
                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)
                    else:
                        squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)
            squares[squarex][squarey] = Board.Square(squarex, squarey, screen, squares[squarex][squarey].piece, True)

        if event.type == pygame.QUIT:
            running = False

    for i in range(8):
        for j in range(8):
            screen.blit(squares[i][j].image, (int(squares[i][j].x), int(squares[i][j].y)))
            piece = squares[i][j].piece
            if piece is not None:
                image_piece = pygame.transform.scale(piece.image, (int(w / 8), int(h / 8)))
                screen.blit(image_piece, (int(squares[i][j].x), int(squares[i][j].y)))

    pygame.display.update()

import pygame
import Board
import Pieces
import numpy as np


def endTurn():
    global turner
    global playerTurn
    global pawns_moved
    global pieces
    turner = turner ^ 1
    playerTurn = players[turner]
    for square in pawns_moved:
        if square.piece.player is playerTurn:
            if isinstance(squares[square.letter][square.number].piece, Pieces.Pawn):
                squares[square.letter][square.number].piece.enpessant_update()
            pawns_moved.pop(0)
    pieces = []
    for ii in range(8):
        for jj in range(8):
            if squares[ii][jj].piece is not None:
                pieces.append(squares[ii][jj])
    return


# initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("EyeChess")
icon = pygame.image.load("../Images/Logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Get board
squares = np.full((8, 8), Board.Square(0, 0, screen, None, False))
for i in range(8):
    for j in range(8):
        piece = Pieces.starting_position(i, j)
        squares[i][j] = Board.Square(i, j, screen, piece, False)
# Set some constants
squarex, squarey = 0, 0
h, w = screen.get_height(), screen.get_width()
Castle = False
players = ["white", "black"]
playerTurn = players[0]
turner = 0
pieces_block = []
pawns_moved = []
pieces = []
width_board = 4 * screen.get_height() / 5

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            if mousey <= width_board and mousex >= (w-width_board)/2 and mousex <= width_board + (w-width_board)/2:
                movex = int(8 * (mousex-(w-width_board)/2) / width_board)
                movey = int(8 * (width_board - mousey) / width_board)
                print(movey, " + ", movex)
                # if statement to move pieces
                if squares[squarex][squarey].piece is not None and squares[squarex][squarey].piece.player is playerTurn and \
                        squares[movex][movey].possibleMove and squares[movex][movey] is not squares[squarex][squarey] \
                        and ((isinstance(squares[squarex][squarey].piece, Pieces.Pawn) and (squares[movex][
                                                                                                movey].piece is None or (
                                                                                                    abs(movex - squarex) == 1 and abs(
                                                                                                movey - squarey) == 1))) or not isinstance(
                    squares[squarex][squarey].piece, Pieces.Pawn)):
                    squares[movex][movey] = Board.Square(movex, movey, screen, squares[squarex][squarey].piece, False)
                    squares[movex][movey].piece.update(movex, movey)
                    squares[squarex][squarey] = Board.Square(squarex, squarey, screen, None, False)
                    # Castleing
                    if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 6 and movey == 0 and Castle:
                        squares[5][0] = Board.Square(5, 0, screen, squares[7][0].piece, False)
                        squares[5][0].piece.update(5, 0)
                        squares[7][0] = Board.Square(7, 0, screen, None, False)
                    if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 2 and movey == 0 and Castle:
                        squares[3][0] = Board.Square(5, 0, screen, squares[0][0].piece, False)
                        squares[3][0].piece.update(3, 0)
                        squares[0][0] = Board.Square(0, 0, screen, None, False)
                    if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 2 and movey == 7 and Castle:
                        squares[3][7] = Board.Square(5, 7, screen, squares[0][7].piece, False)
                        squares[3][7].piece.update(3, 7)
                        squares[0][7] = Board.Square(0, 7, screen, None, False)
                    if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 6 and movey == 7 and Castle:
                        squares[5][7] = Board.Square(5, 7, screen, squares[7][7].piece, False)
                        squares[5][7].piece.update(5, 7)
                        squares[7][7] = Board.Square(7, 7, screen, None, False)
                    # en passant
                    if isinstance(squares[movex][movey].piece, Pieces.Pawn) and squares[movex][
                        movey].piece.player == "white" \
                            and abs(movex - squarex) == 1 and squarey == 4 and movey == 5 and isinstance(
                        squares[movex][4].piece, Pieces.Pawn):
                        squares[movex][4] = Board.Square(movex, 4, screen, None, False)
                    if isinstance(squares[movex][movey].piece, Pieces.Pawn) and squares[movex][
                        movey].piece.player == "black" \
                            and abs(movex - squarex) == 1 and squarey == 3 and movey == 2 and isinstance(
                        squares[movex][3].piece, Pieces.Pawn):
                        squares[movex][3] = Board.Square(movex, 3, screen, None, False)
                    if isinstance(squares[movex][movey].piece, Pieces.Pawn) and (movey == 0 or movey == 7):
                        squares[movex][movey].piece = Pieces.Queen(movex, movey, squares[movex][movey].piece.player)
                    if isinstance(squares[movex][movey].piece, Pieces.Pawn):
                        pawns_moved.append(squares[movex][movey])
                    endTurn()

                # setting new veriables
                squares[squarex][squarey] = Board.Square(squarex, squarey, screen, squares[squarex][squarey].piece, False)
                squarex = movex
                squarey = movey
                Castle = False

                # selecting tiles
                for i in range(8):
                    for j in range(8):
                        if squares[squarex][squarey].piece is not None and squares[squarex][
                            squarey].piece.player is playerTurn:
                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)

                            # Castleing
                            if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                                squarey].piece.player == "white" \
                                    and squares[5][0].piece is None and squares[6][0].piece is None and isinstance(
                                squares[7][0].piece, Pieces.Rook) \
                                    and squares[squarex][squarey].piece.move > 0 and squares[7][0].piece.move > 0:
                                squares[6][0] = Board.Square(6, 0, screen, None, True)
                                Castle = True
                            if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                                squarey].piece.player == "white" \
                                    and squares[3][0].piece is None and squares[2][0].piece is None and squares[1][
                                0].piece is None and isinstance(
                                squares[0][0].piece, Pieces.Rook) \
                                    and squares[squarex][squarey].piece.move > 0 and squares[0][0].piece.move > 0:
                                squares[2][0] = Board.Square(2, 0, screen, None, True)
                                Castle = True
                            if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                                squarey].piece.player == "black" \
                                    and squares[3][7].piece is None and squares[2][7].piece is None and squares[1][
                                7].piece is None and isinstance(
                                squares[0][7].piece, Pieces.Rook) \
                                    and squares[squarex][squarey].piece.move > 0 and squares[0][7].piece.move > 0:
                                squares[2][7] = Board.Square(2, 7, screen, None, True)
                                Castle = True
                            if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                                squarey].piece.player == "black" \
                                    and squares[5][7].piece is None and squares[6][7].piece is None and isinstance(
                                squares[7][7].piece, Pieces.Rook) \
                                    and squares[squarex][squarey].piece.move > 0 and squares[7][7].piece.move > 0:
                                squares[6][7] = Board.Square(6, 7, screen, None, True)
                                Castle = True

                            # Pawn attack
                            if isinstance(squares[squarex][squarey].piece, Pieces.Pawn) and squares[squarex][
                                squarey].piece.player == "white" \
                                    and abs(i - squarex) == 1 and (
                                    (j - squarey == 1 and squares[i][j].piece is not None) or (
                                    squarey == 4 and j == 5 and isinstance(
                                squares[i][4].piece, Pieces.Pawn) and squares[i][
                                        4].piece.move >= 0) and squares[i][4].piece.enpessant):
                                squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)
                            if isinstance(squares[squarex][squarey].piece, Pieces.Pawn) and squares[squarex][
                                squarey].piece.player == "black" \
                                    and abs(i - squarex) == 1 and ((j - squarey == -1 \
                                                                    and squares[i][j].piece is not None) or (
                                                                           squarey == 3 and j == 2 and isinstance(
                                                                       squares[i][3].piece, Pieces.Pawn) and squares[i][
                                                                               3].piece.move >= 0 and squares[i][
                                                                               3].piece.enpessant)):
                                squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)

                            # select possible moves
                            if squares[squarex][squarey].piece.board[i][j]:
                                squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)

                                # Add pieces that are in the way to pieces_block list
                                if squares[i][j].piece is not None and not isinstance(squares[squarex][squarey],
                                                                                      Pieces.Horse) and squares[i][j] is not \
                                        squares[squarex][squarey]:
                                    pieces_block.append(squares[i][j])
                        else:
                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)

                # making sure pieces cannot go over other pieces
                for square in pieces_block:

                    # rules for the rook-lines
                    if square.letter == squarex and square.number > squarey:
                        for i in range(square.number + 1, 8):
                            squares[squarex][i] = Board.Square(squarex, i, screen, squares[squarex][i].piece, False)
                    if square.letter == squarex and square.number < squarey:
                        for i in range(square.number):
                            squares[squarex][i] = Board.Square(squarex, i, screen, squares[squarex][i].piece, False)
                    if square.letter > squarex and square.number == squarey:
                        for i in range(square.letter + 1, 8):
                            squares[i][squarey] = Board.Square(i, squarey, screen, squares[i][squarey].piece, False)
                    if square.letter < squarex and square.number == squarey:
                        for i in range(square.letter):
                            squares[i][squarey] = Board.Square(i, squarey, screen, squares[i][squarey].piece, False)

                    # rules for the bishop-lines
                    if square.letter + square.number == squarex + squarey and square.letter > squarex:
                        for i in range(square.letter + 1, 8):
                            squares[i][i - squarex + squarey] = Board.Square(i, i - squarex + squarey, screen,
                                                                             squares[i][i - squarex + squarey].piece, False)
                    if square.letter + square.number == squarex + squarey and square.letter < squarex:
                        for i in range(square.letter):
                            squares[i][i - squarex + squarey] = Board.Square(i, i - squarex + squarey, screen,
                                                                             squares[i][i - squarex + squarey].piece, False)
                    if square.letter - square.number == squarex - squarey and square.letter > squarex:
                        for i in range(square.letter + 1, 8):
                            if i - (squarex - squarey) < 8:
                                squares[i][i - (squarex - squarey)] = Board.Square(i, i - (squarex - squarey), screen,
                                                                                   squares[i][
                                                                                       i - (squarex - squarey)].piece,
                                                                                   False)
                    if square.letter - square.number == squarex - squarey and square.letter < squarex:
                        for i in range(square.letter + 1):
                            if i - (squarex - squarey) < 8:
                                squares[i][i - (squarex - squarey)] = Board.Square(i, i - (squarex - squarey), screen,
                                                                                   squares[i][
                                                                                       i - (squarex - squarey)].piece,
                                                                                   False)

                    # deselecting the pieces of the own player
                    if square.piece.player is playerTurn:
                        squares[square.letter][square.number] = Board.Square(square.letter, square.number, screen,
                                                                             squares[square.letter][square.number].piece,
                                                                             False)
                pieces_block = []

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    for i in range(8):
        for j in range(8):
            screen.blit(squares[i][j].image, (int(squares[i][j].x), int(squares[i][j].y)))
            piece = squares[i][j].piece
            if piece is not None:
                image_piece = pygame.transform.scale(piece.image, (int(width_board / 8), int(width_board / 8)))
                screen.blit(image_piece, (int(squares[i][j].x), int(squares[i][j].y)))
    pygame.display.update()

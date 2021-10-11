import pygame
import Board
import Pieces
import numpy as np
import rules


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
white = (255, 255, 255)
black = (0, 0, 0)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            if mousey <= width_board and (w - width_board) / 2 <= mousex <= width_board + (w - width_board) / 2:
                movex = int(8 * (mousex - (w - width_board) / 2) / width_board)
                movey = int(8 * (width_board - mousey) / width_board)
                # if statement to move pieces
                if squares[squarex][squarey].piece is not None and squares[squarex][
                    squarey].piece.player is playerTurn and \
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
                    rook_new, rook_old, row = rules.castle(squares, movex, movey, Pieces.King, Castle)
                    if rook_new != 0:
                        squares[rook_new][row] = Board.Square(rook_new, row, screen, squares[7][7].piece, False)
                        squares[rook_new][row].piece.update(rook_old, row)
                        squares[rook_old][row] = Board.Square(rook_old, row, screen, None, False)
                    # en passant
                    passant_row = rules.en_passant(squares, movex, movey, squarex, squarey, Pieces.Pawn)
                    if passant_row != 0:
                        squares[movex][passant_row] = Board.Square(movex, passant_row, screen, None, False)
                    # Queening
                    if isinstance(squares[movex][movey].piece, Pieces.Pawn) and (movey == 0 or movey == 7):
                        squares[movex][movey].piece = Pieces.Queen(movex, movey, squares[movex][movey].piece.player)
                    if isinstance(squares[movex][movey].piece, Pieces.Pawn):
                        pawns_moved.append(squares[movex][movey])
                    endTurn()

                # setting new veriables
                squares[squarex][squarey] = Board.Square(squarex, squarey, screen, squares[squarex][squarey].piece,
                                                         False)
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
                            castle_x, castle_y, castle_possible = rules.castle_possible(squares, squarex, squarey,
                                                                                        Pieces.King, Pieces.Rook)
                            if castle_possible:
                                squares[castle_x][castle_y] = Board.Square(castle_x, castle_y, screen, None, True)
                                Castle = True

                            # Pawn attack
                            pawn_attack = rules.pawn_attack(squares, squarex, squarey, Pieces.Pawn, i, j, playerTurn)
                            if pawn_attack:
                                squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)

                            # select possible moves
                            if squares[squarex][squarey].piece.board[i][j]:
                                squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)
                                # Add pieces that are in the way to pieces_block list
                                if squares[i][j].piece is not None and not isinstance(squares[squarex][squarey],
                                                                                      Pieces.Horse) and squares[i][
                                    j] is not \
                                        squares[squarex][squarey]:
                                    pieces_block.append(squares[i][j])
                        else:
                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)

                # making sure pieces cannot go over other pieces
                blocked_moves = rules.pieces_block(squarex, squarey, pieces_block, playerTurn)
                for i in range(len(blocked_moves)):
                    blocked_x, blocked_y = blocked_moves[i][0], blocked_moves[i][1]
                    squares[blocked_x][blocked_y] = Board.Square(blocked_x, blocked_y, screen,
                                                                 squares[blocked_x][blocked_y].piece, False)
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
    image_white = pygame.transform.scale(pygame.image.load("../Images/white.png"), (w, int(h / 5)))
    screen.blit(image_white, (0, int(4 * h / 5 - 1)))
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render('Look here if you are ready to input a move', True, black, white)
    textRect = text.get_rect()
    textRect.center = (w // 2, 9 * h // 10)
    screen.blit(text, textRect)
    pygame.display.update()

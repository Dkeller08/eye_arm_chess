def castle_possible(squares, squarex, squarey, king, rook):
    pos = []
    if isinstance(squares[squarex][squarey].piece, king) and squares[squarex][
        squarey].piece.player == "white" \
            and squares[5][0].piece is None and squares[6][0].piece is None and isinstance(
        squares[7][0].piece, rook) \
            and squares[squarex][squarey].piece.move > 0 and squares[7][0].piece.move > 0:
        pos.append([6, 0, True])
    if isinstance(squares[squarex][squarey].piece, king) and squares[squarex][
        squarey].piece.player == "white" \
            and squares[3][0].piece is None and squares[2][0].piece is None and squares[1][
        0].piece is None and isinstance(
        squares[0][0].piece, rook) \
            and squares[squarex][squarey].piece.move > 0 and squares[0][0].piece.move > 0:
        pos.append([2, 0, True])
    if isinstance(squares[squarex][squarey].piece, king) and squares[squarex][
        squarey].piece.player == "black" \
            and squares[3][7].piece is None and squares[2][7].piece is None and squares[1][
        7].piece is None and isinstance(
        squares[0][7].piece, rook) \
            and squares[squarex][squarey].piece.move > 0 and squares[0][7].piece.move > 0:
        pos.append([2, 7, True])
    if isinstance(squares[squarex][squarey].piece, king) and squares[squarex][
        squarey].piece.player == "black" \
            and squares[5][7].piece is None and squares[6][7].piece is None and isinstance(
        squares[7][7].piece, rook) \
            and squares[squarex][squarey].piece.move > 0 and squares[7][7].piece.move > 0:
        pos.append([6, 7, True])
    return pos


def pawn_attack(squares, squarex, squarey, pawn, i, j, player_turn):
    if isinstance(squares[squarex][squarey].piece, pawn) and squares[squarex][
        squarey].piece.player == "white" \
            and abs(i - squarex) == 1 and (
            (j - squarey == 1 and squares[i][j].piece is not None and squares[i][
                j].piece.player is not player_turn) or (
                    squarey == 4 and j == 5 and isinstance(
                squares[i][4].piece, pawn) and squares[i][
                        4].piece.move >= 0) and squares[i][4].piece.enpessant):
        return True
    if isinstance(squares[squarex][squarey].piece, pawn) and squares[squarex][
        squarey].piece.player == "black" \
            and abs(i - squarex) == 1 and (
            (j - squarey == -1 and squares[i][j].piece is not None and squares[i][
                j].piece.player is not player_turn) or (
                    squarey == 3 and j == 2 and isinstance(
                squares[i][3].piece, pawn) and squares[i][
                        3].piece.move >= 0 and squares[i][
                        3].piece.enpessant)):
        return True
    else:
        return False


def pieces_block(squarex, squarey, pieces_block, playerTurn):
    blocked_moves = []
    for square in pieces_block:

        # rules for the rook-lines
        if square.letter == squarex and square.number > squarey:
            for i in range(square.number + 1, 8):
                blocked_moves.append([squarex, i])
        if square.letter == squarex and square.number < squarey:
            for i in range(square.number):
                blocked_moves.append([squarex, i])
        if square.letter > squarex and square.number == squarey:
            for i in range(square.letter + 1, 8):
                blocked_moves.append([i, squarey])
        if square.letter < squarex and square.number == squarey:
            for i in range(square.letter):
                blocked_moves.append([i, squarey])

        # rules for the bishop-lines
        if square.letter + square.number == squarex + squarey and square.letter > squarex:
            for i in range(square.letter + 1, 8):
                if i - squarex + squarey < 8:
                    blocked_moves.append([i, i - squarex + squarey])
        if square.letter + square.number == squarex + squarey and square.letter < squarex:
            for i in range(square.letter):
                if i - squarex + squarey < 8:
                    blocked_moves.append([i, i - squarex + squarey])
        if square.letter - square.number == squarex - squarey and square.letter > squarex:
            for i in range(square.letter + 1, 8):
                if i - (squarex - squarey) < 8:
                    blocked_moves.append([i, i - (squarex - squarey)])
        if square.letter - square.number == squarex - squarey and square.letter < squarex:
            for i in range(square.letter + 1):
                if i - (squarex - squarey) < 8:
                    blocked_moves.append([i, i - (squarex - squarey)])

        # deselecting the pieces of the own player
        if square.piece.player is playerTurn:
            blocked_moves.append([square.letter, square.number])
    return blocked_moves


def castle(squares, move_x, move_y, king, Castle):
    if isinstance(squares[move_x][move_y].piece, king) and move_x == 6 and move_y == 0 and Castle:
        return 5, 7, 0
    if isinstance(squares[move_x][move_y].piece, king) and move_x == 2 and move_y == 0 and Castle:
        return 3, 0, 0
    if isinstance(squares[move_x][move_y].piece, king) and move_x == 2 and move_y == 7 and Castle:
        return 3, 0, 7
    if isinstance(squares[move_x][move_y].piece, king) and move_x == 6 and move_y == 7 and Castle:
        return 5, 7, 7
    else:
        return 0, 0, 0


def en_passant(squares, move_x, move_y, square_x, square_y, pawn):
    if isinstance(squares[move_x][move_y].piece, pawn) and squares[move_x][
        move_y].piece.player == "white" \
            and abs(move_x - square_x) == 1 and square_y == 4 and move_y == 5 and isinstance(
        squares[move_x][4].piece, pawn):
        return 4
    if isinstance(squares[move_x][move_y].piece, pawn) and squares[move_x][
        move_y].piece.player == "black" \
            and abs(move_x - square_x) == 1 and square_y == 3 and move_y == 2 and isinstance(
        squares[move_x][3].piece, pawn):
        return 3
    else:
        return 0


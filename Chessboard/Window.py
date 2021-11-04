import pygame
import Board
import Pieces
import numpy as np
import rules
import pylink
import os


def board(screen):
    def endTurn(def_turner, def_pawns_moved):
        def_turner = def_turner ^ 1
        def_playerTurn = players[def_turner]
        for square in def_pawns_moved:
            if square.piece.player is def_playerTurn:
                if isinstance(squares[square.letter][square.number].piece, Pieces.Pawn):
                    squares[square.letter][square.number].piece.enpessant_update()
                def_pawns_moved.pop(0)
        def_pieces = []
        for ii in range(8):
            for jj in range(8):
                if squares[ii][jj].piece is not None:
                    def_pieces.append(squares[ii][jj])
        return def_turner, def_playerTurn, def_pawns_moved, def_pieces

    def abort_trial():
        """Ends recording

        We add 100 msec to catch final events
        """

        # get the currently active tracker object (connection)
        el_tracker = pylink.getEYELINK()

        # Stop recording
        if el_tracker.isRecording():
            # add 100 ms to catch final trial events
            pylink.pumpDelay(100)
            el_tracker.stopRecording()

        # clear the screen
        surf = pygame.display.get_surface()
        surf.fill((128, 128, 128))
        pygame.display.flip()
        # Send a message to clear the Data Viewer screen
        el_tracker.sendMessage('!V CLEAR 128 128 128')

        # send a message to mark trial end
        el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)

    el_tracker = pylink.getEYELINK()
    el_tracker.setOfflineMode()
    el_tracker.sendCommand('clear_screen 0')
    try:
        el_tracker.startRecording(1, 1, 1, 1)
    except RuntimeError as error:
        print("ERROR:", error)
        return pylink.TRIAL_ERROR
    pylink.pumpDelay(100)

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
    minimum_duration = 3000
    new_sample = None
    old_sample = None
    in_hit_region = False
    gaze_start = -1
    trigger_fired = False
    move_x_2 = 0
    move_y_2 = 0
    move_start = None

    # Game Loop
    running = True
    while running:
        new_sample = el_tracker.getNewestSample()
        if new_sample is not None:
            if old_sample is not None:
                if new_sample.getTime() != old_sample.getTime():
                    # check if the new sample has data for the eye
                    # currently being tracked; if so, we retrieve the current
                    # gaze position and PPD (how many pixels correspond to 1
                    # deg of visual angle, at the current gaze position)

                    r_x, r_y = new_sample.getRightEye().getGaze()

                    l_x, l_y = new_sample.getLeftEye().getGaze()

                    # break the while loop if the current gaze position is
                    # in a 120 x 120 pixels region around the screen centered
                    if min(l_y, r_y) >= width_board:
                        # record gaze start time
                        if not in_hit_region:
                            if gaze_start == -1:
                                gaze_start = pygame.time.get_ticks()
                                in_hit_region = True
                        # check the gaze duration and fire
                        if in_hit_region:
                            gaze_dur = pygame.time.get_ticks() - gaze_start
                            if gaze_dur > minimum_duration:
                                trigger_fired = True
                    elif max(l_y, r_y) <= width_board and (w - width_board) / 2 <= (l_x + r_x) / 2 <= width_board + (
                            w - width_board) / 2 and trigger_fired:
                        move_x_1 = int(8 * ((l_x + r_x) / 2 - (w - width_board) / 2) / width_board)
                        move_y_1 = int(8 * (width_board - (l_y + r_y) / 2) / width_board)
                        if move_x_1 == move_x_2 and move_y_1 == move_y_2:
                            if move_start is None:
                                move_start = pygame.time.get_ticks()
                            elif pygame.time.get_ticks() - move_start > minimum_duration:
                                movex = move_x_1
                                movey = move_y_1
                                # if statement to move pieces
                                if squares[squarex][squarey].piece is not None and squares[squarex][
                                    squarey].piece.player is playerTurn and \
                                        squares[movex][movey].possibleMove and squares[movex][movey] is not \
                                        squares[squarex][squarey] \
                                        and (
                                        (isinstance(squares[squarex][squarey].piece, Pieces.Pawn) and (squares[movex][
                                                                                                           movey].piece is None or (
                                                                                                               abs(movex - squarex) == 1 and abs(
                                                                                                           movey - squarey) == 1))) or not isinstance(
                                    squares[squarex][squarey].piece, Pieces.Pawn)):
                                    squares[movex][movey] = Board.Square(movex, movey, screen,
                                                                         squares[squarex][squarey].piece, False)
                                    squares[movex][movey].piece.update(movex, movey)
                                    squares[squarex][squarey] = Board.Square(squarex, squarey, screen, None, False)
                                    # Castleing
                                    rook_new, rook_old, row = rules.castle(squares, movex, movey, Pieces.King, Castle)
                                    if rook_new != 0:
                                        squares[rook_new][row] = Board.Square(rook_new, row, screen,
                                                                              squares[rook_old][row].piece,
                                                                              False)
                                        squares[rook_new][row].piece.update(rook_new, row)
                                        squares[rook_old][row] = Board.Square(rook_old, row, screen, None, False)
                                    # en passant
                                    passant_row = rules.en_passant(squares, movex, movey, squarex, squarey, Pieces.Pawn)
                                    if passant_row != 0:
                                        squares[movex][passant_row] = Board.Square(movex, passant_row, screen, None,
                                                                                   False)
                                    # Queening
                                    if isinstance(squares[movex][movey].piece, Pieces.Pawn) and (
                                            movey == 0 or movey == 7):
                                        squares[movex][movey].piece = Pieces.Queen(movex, movey,
                                                                                   squares[movex][movey].piece.player)
                                    if isinstance(squares[movex][movey].piece, Pieces.Pawn):
                                        pawns_moved.append(squares[movex][movey])
                                    turner, playerTurn, pawns_moved, pieces = endTurn(turner, pawns_moved)

                                # setting new veriables
                                squares[squarex][squarey] = Board.Square(squarex, squarey, screen,
                                                                         squares[squarex][squarey].piece,
                                                                         False)
                                squarex = movex
                                squarey = movey
                                Castle = False

                                # selecting tiles
                                for i in range(8):
                                    for j in range(8):
                                        if squares[squarex][squarey].piece is not None and squares[squarex][
                                            squarey].piece.player \
                                                is playerTurn:
                                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)
                                            # Castleing
                                            pos_list = rules.castle_possible(squares, squarex, squarey,
                                                                             Pieces.King, Pieces.Rook)
                                            for pos in pos_list:
                                                castle_x, castle_y, castle_possible = pos
                                                if castle_possible:
                                                    squares[castle_x][castle_y] = Board.Square(castle_x, castle_y,
                                                                                               screen, None, True)
                                                    Castle = True

                                            # Pawn attack
                                            pawn_attack = rules.pawn_attack(squares, squarex, squarey, Pieces.Pawn, i,
                                                                            j, playerTurn)
                                            if pawn_attack:
                                                squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)

                                            # select possible moves
                                            if squares[squarex][squarey].piece.board[i][j]:
                                                squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)
                                                # Add pieces that are in the way to pieces_block list
                                                if squares[i][j].piece is not None and not isinstance(
                                                        squares[squarex][squarey],
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
                                                                                 squares[blocked_x][blocked_y].piece,
                                                                                 False)
                                pieces_block = []

                        move_x_2 = move_x_1
                        move_y_2 = move_y_1
                    else:  # gaze outside the hit region, reset variables
                        in_hit_region = False
                        gaze_start = -1

            # update the "old_sample"
            old_sample = new_sample

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    abort_trial()

        for i in range(8):
            for j in range(8):
                screen.blit(squares[i][j].image, (int(squares[i][j].x), int(squares[i][j].y)))
                piece = squares[i][j].piece
                if piece is not None:
                    image_piece = pygame.transform.scale(piece.image, (int(width_board / 8), int(width_board / 8)))
                    screen.blit(image_piece, (int(squares[i][j].x), int(squares[i][j].y)))
        image_white = pygame.transform.scale(pygame.image.load("../Images/white.png"), (w, int(h / 5)))
        screen.blit(image_white, (0, int(4 * h / 5 - 1)))
        if in_hit_region:
            image_green = pygame.transform.scale(pygame.image.load("../Images/green.png"),
                                                 (w * min(gaze_dur / minimum_duration, 1), int(h / 5)))
            screen.blit(image_green, (0, int(4 * h / 5 - 1)))
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render('Look here if you are ready to input a move', True, black, white)
        textRect = text.get_rect()
        textRect.center = (w // 2, 9 * h // 10)
        screen.blit(text, textRect)
        pygame.display.update()

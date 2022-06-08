import pygame
import Board
import Pieces
import numpy as np
import rules
import pylink
import cv2
import board_recognition

debug = False

try:
    import move_cartesian

    robot_connected = True
except:
    robot_connected = False


def board(screen, Dummy):
    def undistort(img):
        cv2.imshow("undistorted", img)
        cv2.waitKey(0)
        DIM = (1920, 1440)
        K = np.array([[1141.0682579839233, 0.0, 986.5923008101605], [0.0, 1141.588261433595, 747.2232727434749],
                      [0.0, 0.0, 1.0]])
        D = np.array([[-0.07684126395433953], [0.22851365143861682], [-0.4987877748120961], [0.3869384335287188]])
        h, w = img.shape[:2]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        cv2.imshow("undistorted", undistorted_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return undistorted_img

    def check_board():
        try:
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)  # auto mode
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
            cap.set(cv2.CAP_PROP_EXPOSURE, 15)  # 0-5000
            cap.set(cv2.CAP_PROP_CONTRAST, 13)  # 0-30
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)  # -64-64

            camera_used = True
        except:
            print("Camera cannot be accesed")
            camera_used = False
        ret, frame_dim = cap.read()
        # frame_dim = cv2.imread('dim.jpg')
        # frame_dim = undistort(frame_dim)
        if debug is True:
            cv2.imshow('frame', frame_dim)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        cap.release()

        try:
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)  # auto mode
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
            cap.set(cv2.CAP_PROP_EXPOSURE, 20)  # 0-5000
            cap.set(cv2.CAP_PROP_CONTRAST, 13)  # 0-30
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)  # -64-64
            camera_used = True
        except:
            print("Camera cannot be accesed")
            camera_used = False
        ret, frame_bright = cap.read()
        # frame_bright = cv2.imread('bright.jpg')
        # frame_bright = undistort(frame_bright)
        if debug is True:
            cv2.imshow('frame', frame_bright)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        cap.release()

        square = board_recognition.board_recognition(frame_dim, frame_bright)
        return square

    def check_initial_position(board):
        correct_squares = 0
        false_squares = 0
        not_recognized = 0
        falsely_recognized = 0
        square = check_board()
        for i in range(8):
            for j in range(8):
                board[i][j].has_piece()

                if board[i][j].piece_bool == square[i][j].has_piece:
                    correct_squares += 1
                else:
                    false_squares += 1
                    if board[i][j].piece_bool:
                        not_recognized += 1
                    else:
                        print(square[i][j].position)
                        falsely_recognized += 1

        return correct_squares, false_squares, not_recognized, falsely_recognized

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

    def check_moves(def_squares, def_movex, def_movey, def_squarex, def_squarey, def_playerTurn, def_turner,
                    def_pawns_moved, def_Castle, def_selected_string):
        def_move_string = ""
        if def_squares[def_squarex][def_squarey].piece is not None and def_squares[def_squarex][
            def_squarey].piece.player is def_playerTurn and \
                def_squares[def_movex][def_movey].possibleMove and def_squares[def_movex][def_movey] is not \
                def_squares[def_squarex][def_squarey] \
                and (
                (isinstance(def_squares[def_squarex][def_squarey].piece, Pieces.Pawn) and (def_squares[def_movex][
                                                                                               def_movey].piece is None or (
                                                                                                   abs(def_movex - def_squarex) == 1 and abs(
                                                                                               def_movey - def_squarey) == 1))) or not isinstance(
            def_squares[def_squarex][def_squarey].piece, Pieces.Pawn)):
            if def_squares[def_movex][def_movey].piece is None:
                def_move_string = def_selected_string + str(def_movex) + str(def_movey)
            else:
                def_move_string = def_selected_string + "x" + type(def_squares[def_movex][def_movey].piece).__name__[
                    0] + str(def_movex) + str(def_movey)
            def_squares[def_movex][def_movey] = Board.Square(def_movex, def_movey, screen,
                                                             def_squares[def_squarex][def_squarey].piece, False)
            def_squares[def_movex][def_movey].piece.update(def_movex, def_movey)
            def_squares[def_squarex][def_squarey] = Board.Square(def_squarex, def_squarey, screen, None, False)
            # Castleing
            rook_new, rook_old, row = rules.castle(def_squares, def_movex, def_movey, Pieces.King, def_Castle)
            if rook_new != 0:
                def_squares[rook_new][row] = Board.Square(rook_new, row, screen,
                                                          def_squares[rook_old][row].piece,
                                                          False)
                def_squares[rook_new][row].piece.update(rook_new, row)
                def_squares[rook_old][row] = Board.Square(rook_old, row, screen, None, False)
                def_move_string = "O" + def_selected_string + "R" + str(rook_old) + str(row)
            # en passant
            passant_row = rules.en_passant(def_squares, def_movex, def_movey, def_squarex, def_squarey, Pieces.Pawn)
            if passant_row != 0:
                def_move_string = def_selected_string + "e.p." + str(def_movex) + str(def_movey)
                def_squares[def_movex][passant_row] = Board.Square(def_movex, passant_row, screen, None,
                                                                   False)
            # Queening
            if isinstance(def_squares[def_movex][def_movey].piece, Pieces.Pawn) and (
                    def_movey == 0 or def_movey == 7):
                def_move_string = def_move_string + "=Q"
                def_squares[def_movex][def_movey].piece = Pieces.Queen(def_movex, def_movey,
                                                                       def_squares[def_movex][def_movey].piece.player)
            if isinstance(def_squares[def_movex][def_movey].piece, Pieces.Pawn):
                def_pawns_moved.append(def_squares[def_movex][def_movey])
            def_turner, def_playerTurn, def_pawns_moved, pieces = endTurn(def_turner, def_pawns_moved)
            trigger_fired = False

        # setting new veriables
        def_squares[def_squarex][def_squarey] = Board.Square(def_squarex, def_squarey, screen,
                                                             def_squares[def_squarex][def_squarey].piece,
                                                             False)
        def_squarex = def_movex
        def_squarey = def_movey
        def_Castle = False

        # selecting tiles
        for i in range(8):
            for j in range(8):
                if def_squares[def_squarex][def_squarey].piece is not None and def_squares[def_squarex][
                    def_squarey].piece.player \
                        is def_playerTurn:
                    def_selected_string = type(def_squares[def_squarex][def_squarey].piece).__name__[0] + playerTurn[
                        0] + str(
                        def_squarex) + str(def_squarey)
                    def_squares[i][j] = Board.Square(i, j, screen, def_squares[i][j].piece, False)
                    # Castleing
                    pos_list = rules.castle_possible(def_squares, def_squarex, def_squarey,
                                                     Pieces.King, Pieces.Rook)
                    for pos in pos_list:
                        castle_x, castle_y, castle_possible = pos
                        if castle_possible:
                            def_squares[castle_x][castle_y] = Board.Square(castle_x, castle_y,
                                                                           screen, None, True)
                            def_Castle = True

                    # Pawn attack
                    pawn_attack = rules.pawn_attack(def_squares, def_squarex, def_squarey, Pieces.Pawn, i,
                                                    j, def_playerTurn)
                    if pawn_attack:
                        def_squares[i][j] = Board.Square(i, j, screen, def_squares[i][j].piece, True)

                    # select possible moves
                    if def_squares[def_squarex][def_squarey].piece.board[i][j]:
                        def_squares[i][j] = Board.Square(i, j, screen, def_squares[i][j].piece, True)
                        # Add pieces that are in the way to pieces_block list
                        if def_squares[i][j].piece is not None and not isinstance(
                                def_squares[def_squarex][def_squarey],
                                Pieces.Horse) and def_squares[i][
                            j] is not \
                                def_squares[def_squarex][def_squarey]:
                            pieces_block.append(def_squares[i][j])
                else:
                    def_squares[i][j] = Board.Square(i, j, screen, def_squares[i][j].piece, False)

        # making sure pieces cannot go over other pieces
        blocked_moves = rules.pieces_block(def_squarex, def_squarey, pieces_block, def_playerTurn)
        for i in range(len(blocked_moves)):
            blocked_x, blocked_y = blocked_moves[i][0], blocked_moves[i][1]
            def_squares[blocked_x][blocked_y] = Board.Square(blocked_x, blocked_y, screen,
                                                             def_squares[blocked_x][blocked_y].piece,
                                                             False)
        return def_squares, def_squarex, def_squarey, def_playerTurn, def_turner, def_pawns_moved, def_Castle, def_selected_string, def_move_string

    def compare_boards(board, playerTurn, turner, pawns_moved, Castle, selected_string):
        square = check_board()
        move_string = []
        now_empty = []
        now_full = []
        for i in range(8):
            for j in range(8):
                board[i][j].has_piece()
                print(board[i][j].piece_bool, square[i][j].has_piece)
                if board[i][j].piece_bool != square[i][j].has_piece:
                    if board[i][j].piece_bool:
                        now_empty.append([i, j])
                    else:
                        now_full.append([i, j])

        print(now_empty, now_full)
        if len(now_empty) == 1 and len(now_full) == 1:
            print("move detected")
            board, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                board,
                now_empty[0][0],
                now_empty[0][1],
                now_full[0][0],
                now_full[0][1],
                playerTurn,
                turner,
                pawns_moved,
                Castle,
                selected_string)
            board, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                board,
                now_full[0][0],
                now_full[0][1],
                now_empty[0][0],
                now_empty[0][1],
                playerTurn,
                turner,
                pawns_moved,
                Castle,
                selected_string)
        elif len(now_empty) == 1 and len(now_full) == 0:
            hit_piece = []
            for i in range(8):
                for j in range(8):
                    if board[i][j].piece is not None and square[i][j].color is not None and board[i][j].piece.player != \
                            square[i][j].color:
                        hit_piece.append([i, j])
                        print(board[i][j].piece.player, square[i][j].color)
            if len(hit_piece) == 1:
                board, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                    board,
                    now_empty[0][0],
                    now_empty[0][1],
                    hit_piece[0][0],
                    hit_piece[0][1],
                    playerTurn,
                    turner,
                    pawns_moved,
                    Castle,
                    selected_string)
                board, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                    board,
                    hit_piece[0][0],
                    hit_piece[0][1],
                    now_empty[0][0],
                    now_empty[0][1],
                    playerTurn,
                    turner,
                    pawns_moved,
                    Castle,
                    selected_string)
            else:
                print("no hit found")
                print(hit_piece)
        elif len(now_empty) == 2 and len(now_full) == 2:
            for empty in now_empty:
                if empty[0] == 4:
                    for full in now_full:
                        print("one last if statement")
                        print(full[0])
                        if abs(full[0] - 4) == 2:
                            print("casteling")
                            board, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                                board,
                                empty[0],
                                empty[1],
                                full[0],
                                full[1],
                                playerTurn,
                                turner,
                                pawns_moved,
                                Castle,
                                selected_string)
                            board, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                                board,
                                full[0],
                                full[1],
                                empty[0],
                                empty[1],
                                playerTurn,
                                turner,
                                pawns_moved,
                                Castle,
                                selected_string)

        return board, playerTurn, turner, pawns_moved, Castle, selected_string, move_string

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

    if not Dummy:
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
    correct, faulty, not_recog, false_recog = check_initial_position(squares)
    if faulty != 0:
        raise Exception(
            f'Board not found correctly! Number of detections: {32 - not_recog + false_recog}, Correctsquares: {correct}, faulty squares: {faulty}. Not '
            f'recognized: {not_recog}, falsely recognized: {false_recog}')
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
    minimum_move_duration = 750
    new_sample = None
    old_sample = None
    in_hit_region = False
    gaze_start = -1
    trigger_fired = False
    move_x_2 = 0
    move_y_2 = 0
    move_start = None
    selected_string = ""

    # Game Loop
    running = True
    while running:
        if not Dummy:
            new_sample = el_tracker.getNewestSample()
            if new_sample is not None and old_sample is not None and new_sample.getTime() != old_sample.getTime():
                # check if the new sample has data for the eye
                # currently being tracked; if so, we retrieve the current
                # gaze position and PPD (how many pixels correspond to 1
                # deg of visual angle, at the current gaze position)

                r_x, r_y = new_sample.getRightEye().getGaze()

                l_x, l_y = new_sample.getLeftEye().getGaze()

                if min(l_y, r_y) >= width_board:
                    # record gaze start time
                    if not in_hit_region:
                        if gaze_start == -1:
                            gaze_start = pygame.time.get_ticks()
                            in_hit_region = True
                    # check the gaze duration and fire
                    if in_hit_region and not trigger_fired:
                        gaze_dur = pygame.time.get_ticks() - gaze_start
                        if gaze_dur > minimum_duration:
                            trigger_fired = True
                elif max(l_y, r_y) <= width_board and (w - width_board) / 2 <= (l_x + r_x) / 2 <= width_board + (
                        w - width_board) / 2 and trigger_fired:
                    move_x_1 = int(8 * ((l_x + r_x) / 2 - (w - width_board) / 2) / width_board)
                    move_y_1 = int(8 * (width_board - (l_y + r_y) / 2) / width_board)
                    if move_x_1 == move_x_2 and move_y_1 == move_y_2 and move_x_1 < 8 and move_y_1 < 8:
                        if move_start is None:
                            move_start = pygame.time.get_ticks()
                        elif pygame.time.get_ticks() - move_start > minimum_move_duration:
                            movex = move_x_1
                            movey = move_y_1
                            # if statement to move pieces
                            squares, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                                squares,
                                movex,
                                movey,
                                squarex,
                                squarey,
                                playerTurn,
                                turner,
                                pawns_moved,
                                Castle, selected_string)
                            pieces_block = []
                            if move_string != "":
                                # os.system("python2.7 ../../move_cartesian.py " + move_string)
                                # subprocess.Popen(["python2.7", "../../move_cartesian.py", move_string])
                                move_cartesian.input_move(move_string)


                    else:
                        move_start = None
                    move_x_2 = move_x_1
                    move_y_2 = move_y_1
                else:  # gaze outside the hit region, reset variables
                    in_hit_region = False
                    gaze_start = -1

                # update the "old_sample"
            old_sample = new_sample

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                if mousey <= width_board and (w - width_board) / 2 <= mousex <= width_board + (w - width_board) / 2:
                    movex = int(8 * (mousex - (w - width_board) / 2) / width_board)
                    movey = int(8 * (width_board - mousey) / width_board)
                    # if statement to move pieces
                    squares, squarex, squarey, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = check_moves(
                        squares, movex,
                        movey, squarex,
                        squarey,
                        playerTurn, turner,
                        pawns_moved,
                        Castle, selected_string)
                    pieces_block = []
                    if move_string != "" and robot_connected:
                        # os.system("python2.7 ../../move_cartesian.py " + move_string)
                        # subprocess.Popen(["python2.7", "../../move_cartesian.py", move_string])
                        move_cartesian.input_move(move_string)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    squares, playerTurn, turner, pawns_moved, Castle, selected_string, move_string = compare_boards(
                        squares, playerTurn, turner, pawns_moved, Castle, selected_string)
                    pieces_block = []
                    print(move_string)
                if event.key == pygame.K_q:
                    running = False
                    if not Dummy:
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
        if in_hit_region or trigger_fired:
            image_green = pygame.transform.scale(pygame.image.load("../Images/green.png"),
                                                 (w * min(gaze_dur / minimum_duration, 1), int(h / 5)))
            screen.blit(image_green, (0, int(4 * h / 5 - 1)))
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render('Look here if you are ready to input a move', True, black, white)
        textRect = text.get_rect()
        textRect.center = (w // 2, 9 * h // 10)
        screen.blit(text, textRect)
        pygame.display.update()
        if new_sample is not None and old_sample is not None and new_sample.getTime() != old_sample.getTime():
            image_black = pygame.transform.scale(pygame.image.load("../Images/black.png"), (30, 30))
            screen.blit(image_black, ((r_x + l_x) / 2, (l_y + r_y) / 2))

# eye_arm_chess
Welcome to de README of the eye_arm_chess repository! First an introduction on what the program does will be provided, next the installation steps will be given and last the code-structure will be explained.

The goal of the program is to connect a Eyelink 100+ eyetracker to a robotic arm of Franka Emica Panda. This is done via a chess program that first lets you input a move via the eyetracker. Than it sends the move to the robotic arm to be executed. A camera-recognition has also been implemented that is able to recognize legal moves on the chess board and show them to the person behind the eyetracker.

The chessprogram is implemented in four files. First there are two files for the board and the pieces, called board.py and pieces.py. The special rules of the chessgame are in rules.py. Finally Window.py arranges the gameflow and sends and gets messages from the different instruments.

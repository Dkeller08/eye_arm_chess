import pylink
import pygame
import os
import Window

from pygame import FULLSCREEN, DOUBLEBUF

from CalibrationGraphicsPygame import CalibrationGraphics

""" A short script showing how to use this library.

We connect to the tracker, open a Pygame window, and then configure the
graphics environment for calibration. Then, perform a calibration and
disconnect from the tracker.

The doTrackerSetup() command will bring up a gray calibration screen.
When the gray screen comes up, press Enter to show the camera image,
press C to calibrate, V to validate, and O to quit calibration"""
Dummy = False

# initialize Pygame
pygame.init()
os.environ['SDL_VIDEODRIVER'] = 'windows'
pygame.display.set_caption("EyeChess")
icon = pygame.image.load("../Images/Logo.png")
pygame.display.set_icon(icon)

# get the screen resolution natively supported by the monitor
disp = pylink.getDisplayInformation()
scn_w = disp.width
scn_h = disp.height

# connect to the tracker
try:
    el_tracker = pylink.EyeLink("100.1.1.1")
except:
    Dummy = True
# open an EDF data file on the Host PC

# open a Pygame window
win = pygame.display.set_mode((scn_w, scn_h), FULLSCREEN | DOUBLEBUF)
if not Dummy:
    el_tracker.openDataFile('test.edf')
    # send over a command to let the tracker know the correct screen resolution
    scn_coords = "screen_pixel_coords = 0 0 %d %d" % (scn_w - 1, scn_h - 1)
    el_tracker.sendCommand(scn_coords)

    # Instantiate a graphics environment (genv) for calibration
    genv = CalibrationGraphics(el_tracker, win)

    # Set background and foreground colors for calibration
    foreground_color = (0, 0, 0)
    background_color = (128, 128, 128)
    genv.setCalibrationColors(foreground_color, background_color)

    # The calibration target could be a "circle" (default) or a "picture",
    genv.setTargetType('circle')
    # Configure the size of the calibration target (in pixels)
    genv.setTargetSize(24)

    # Beeps to play during calibration, validation, and drift correction
    # parameters: target, good, error
    # Each parameter could be ''--default sound, 'off'--no sound, or a wav file
    genv.setCalibrationSounds('', '', '')

    # Request Pylink to use the graphics environment (genv) we customized above
    pylink.openGraphicsEx(genv)

    # calibrate the tracker
    el_tracker.doTrackerSetup()

Window.board(win, Dummy)

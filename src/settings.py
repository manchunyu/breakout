from pyray import *
from raylib import *
from random import randint, uniform
from os.path import join

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT) = (1280, 800)
PATH_TO_IMAGES = ["..", "assets", "images"]


BALL_SPEED = 500
BALL_INIT_POS = Vector2(WINDOW_WIDTH / 2 - 11, WINDOW_HEIGHT - 100 - 22)

PLAYER_SPEED = 300
PLAYER_INIT_POS = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100)




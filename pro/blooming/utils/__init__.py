"""Shared game constants"""

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

BASE_DIR = None  # set at runtime


def set_base_dir(path):
    global BASE_DIR
    BASE_DIR = path


COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'green': (0, 128, 0),
    'dark_green': (0, 64, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'pink': (255, 192, 203),
    'brown': (139, 69, 19),
    'dark_purple': (40, 0, 60),
    'fog': (180, 190, 200),
    'dark_fog': (100, 110, 120),
}

IMAGE_DIR = None  # set at runtime


def set_image_dir(path):
    global IMAGE_DIR
    IMAGE_DIR = path

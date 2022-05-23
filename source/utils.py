import math
import random

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def random_color():
    return (
        random.randrange(0, 255),
        random.randrange(0, 255),
        random.randrange(0, 255),
    )


def random_position():
    padding = 50
    return (
        random.randrange(padding, SCREEN_WIDTH - padding),
        random.randrange(padding * 4, SCREEN_HEIGHT - padding),
    )


def colors_match(color1, color2):
    return math.dist(color1, color2) < 80

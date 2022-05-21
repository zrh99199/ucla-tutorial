import arcade
from constants import *
from game_view import GameView


def main():
    """Start the game"""

    # Load fonts

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(GameView())
    arcade.run()


if __name__ == "__main__":
    main()

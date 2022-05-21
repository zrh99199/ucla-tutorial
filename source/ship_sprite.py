import arcade

from constants import *


class ShipSprite(arcade.Sprite):
    """
    Sprite that represents our space ship.

    Derives from arcade.Sprite.
    """

    MIN_ANGLE = -90
    MAX_ANGLE = 90

    def __init__(self, filename, scale):
        """Set up the space ship."""

        # Call the parent Sprite constructor
        super().__init__(filename, scale)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = self.height + 10
        self.angle = 0

    def update(self):
        """
        Update our position and other particulars.
        """
        if self.angle < ShipSprite.MIN_ANGLE:
            self.angle = ShipSprite.MIN_ANGLE
        elif self.angle > ShipSprite.MAX_ANGLE:
            self.angle = ShipSprite.MAX_ANGLE

        """ Call the parent class. """
        super().update()

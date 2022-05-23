import arcade

from arcade.experimental.shadertoy import Shadertoy


class ExplosionMaker:
    """Class to create and draw explosions."""

    def __init__(self, size, position, color=arcade.csscolor.WHITE):

        self.shadertoy: Shadertoy = Shadertoy.create_from_file(size, "explosion.glsl")
        self.shadertoy.program["explosionPos"] = position
        self.shadertoy.program["color"] = arcade.get_three_float_color(color)
        self.time = 0.0
        self.position = position

    def update(self, time):
        self.time += time

    def render(self):
        self.shadertoy.render(time=self.time)

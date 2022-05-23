import arcade
import math

from projectile import Projectile


class GlowLine(Projectile):
    def __init__(self, shadertoy, glowcolor, length=10):
        super().__init__(shadertoy=shadertoy)
        self.type = None
        self.shadertoy = shadertoy
        self.glowcolor = glowcolor
        self.length = length
        self.texture = arcade.make_circle_texture(4, glowcolor)

    def get_color(self):
        return self.glowcolor

    def draw(self):
        self.shadertoy.program["pos"] = self.position
        self.shadertoy.program["lineColor"] = arcade.get_four_float_color(
            self.glowcolor
        )
        self.shadertoy.program["angle"] = math.radians(self.angle)
        self.shadertoy.program["laserLength"] = self.length
        self.shadertoy.render()

    def update(self):
        """Move the sprite"""
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

import arcade
import math

from bullet import Bullet


class GlowLine(Bullet):
    def __init__(self, shadertoy, glowcolor):
        super().__init__(shadertoy=shadertoy)
        self.type = None
        self.shadertoy = shadertoy
        self.glowcolor = glowcolor
        self.texture = arcade.make_circle_texture(4, glowcolor)
        self._points = self.texture.hit_box_points

    def draw(self):
        self.shadertoy.program["pos"] = self.position
        self.shadertoy.program["lineColor"] = arcade.get_four_float_color(
            self.glowcolor
        )
        self.shadertoy.program["angle"] = math.radians(self.angle)

        self.shadertoy.program["laserLength"] = 100
        self.shadertoy.render()

    def update(self):
        """Move the sprite"""
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

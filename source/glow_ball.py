import arcade
from projectile import Projectile


class GlowBall(Projectile):
    def __init__(self, shadertoy, glowcolor, radius):
        super().__init__(shadertoy=shadertoy)
        self.type = None
        self.shadertoy = shadertoy
        self.glowcolor = glowcolor
        self.radius = radius
        self.texture = arcade.make_circle_texture(radius * 2, glowcolor)

    def get_color(self):
        return self.glowcolor

    def draw(self):
        self.shadertoy.program["pos"] = self.position
        self.shadertoy.program["color"] = arcade.get_three_float_color(self.glowcolor)
        self.shadertoy.program["size"] = 15
        self.shadertoy.render()

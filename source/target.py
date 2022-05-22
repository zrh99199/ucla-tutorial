import arcade


class Target(arcade.Sprite):
    def __init__(self, shadertoy, glowcolor, radius, position):
        super().__init__(None, 1.0)
        self.type = None
        self.shadertoy = shadertoy
        self.glowcolor = glowcolor
        self.radius = radius
        self.texture = arcade.make_circle_texture(radius * 2, glowcolor)
        self.position = position

    def get_color(self):
        return self.glowcolor

    def draw(self):
        self.shadertoy.program["pos"] = self.position
        self.shadertoy.program["color"] = arcade.get_three_float_color(self.glowcolor)
        self.shadertoy.program["size"] = 20
        self.shadertoy.render()

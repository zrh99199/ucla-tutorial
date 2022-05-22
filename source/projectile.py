import arcade


class Projectile(arcade.Sprite):
    """Base class for fireable objects"""

    def __init__(self, image_file=None, scale=1.0, shadertoy=None):
        super().__init__(image_file, scale)
        self.type = None
        self.shadertoy = shadertoy

    def get_color(self):
        pass

    def draw(self):
        pass

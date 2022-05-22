import arcade


class Swatch(arcade.Sprite):
    def __init__(self, position, image_file=None, scale=1.0):
        super().__init__(image_file, scale)
        self.type = None
        self.position = position
        self.color = (255, 255, 255)
        self.width = 100
        self.height = 100
        self.border_width = 10

    def set_color(self, color):
        self.color = color

    def draw(self):
        arcade.draw_rectangle_outline(
            self.center_x,
            self.center_y,
            width=self.width,
            height=self.height,
            color=(255, 255, 255),
            border_width=self.border_width,
        )
        arcade.draw_rectangle_filled(self.center_x, self.center_y, 100, 100, self.color)
        arcade.draw_text(
            text=str(self.color),
            start_x=self.center_x,
            start_y=self.center_y - self.height / 2 - self.border_width - 20,
            width=self.width + self.border_width * 2,
            font_name="Arial",
            font_size=11,
            anchor_x="center",
        )

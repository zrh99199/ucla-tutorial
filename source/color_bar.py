import arcade

MAX_VALUE = 255


class ColorBar(arcade.Sprite):
    def __init__(self, position, initial_value, color, image_file=None, scale=1.0):
        super().__init__(image_file, scale)
        assert color in ["red", "green", "blue"]
        self.position = position
        self.value = initial_value
        self.color = (
            arcade.csscolor.RED
            if color == "red"
            else arcade.csscolor.GREEN
            if color == "green"
            else arcade.csscolor.BLUE
        )
        self.width = 30
        self.height = 100

    def set_value(self, value):
        self.value = value

    def draw(self):
        fill_height = self.height * self.value / MAX_VALUE
        arcade.draw_rectangle_filled(
            center_x=self.position[0],
            center_y=self.height / 2 + fill_height / 2,
            width=self.width,
            height=fill_height,
            color=self.color,
        )
        arcade.draw_rectangle_outline(
            center_x=self.position[0],
            center_y=self.position[1],
            width=self.width,
            height=self.height,
            border_width=5,
            color=(255, 255, 255),
        )

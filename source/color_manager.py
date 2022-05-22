from dataclasses import dataclass


@dataclass
class ColorManager:
    """Class for keeping track of the current color and how fast it's changing."""

    color_names = ["red", "green", "blue"]
    red: int = 255 / 2
    green: int = 255 / 2
    blue: int = 255 / 2
    delta_red: int = 0
    delta_green: int = 0
    delta_blue: int = 0

    @property
    def colors(self) -> tuple:
        return (self.red, self.green, self.blue)

    def _clamp_color(self, color_value):
        return int(max(min(color_value, 255), 0))

    def update_colors(self):
        self.red = self._clamp_color(self.red + self.delta_red)
        self.green = self._clamp_color(self.green + self.delta_green)
        self.blue = self._clamp_color(self.blue + self.delta_blue)

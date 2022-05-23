import arcade

from target import Target
from utils import random_color, random_position


class TargetManager:
    """Class to create and display targets to shoot at"""

    def __init__(self, shadertoy, max_targets=3):
        self.targets = arcade.SpriteList()
        self.shadertoy = shadertoy
        self.max_targets = max_targets

    def get_targets(self):
        return self.targets

    def remove_target(self, target):
        self.targets.remove(target)

    def is_match(self, color):
        return False

    def update(self):
        if len(self.targets) < self.max_targets:
            self.targets.append(
                Target(
                    shadertoy=self.shadertoy,
                    glowcolor=random_color(),
                    radius=40,
                    position=random_position(),
                )
            )

    def draw(self):
        for target in self.targets:
            target.draw()

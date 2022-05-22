import math

import arcade
from arcade.experimental.shadertoy import Shadertoy

from constants import *
from ship_sprite import ShipSprite

# from projectile import Projectile
from color_bar import ColorBar
from color_manager import ColorManager
from glow_ball import GlowBall
from explosion import ExplosionMaker
from target_spawner import TargetSpawner
from swatch import Swatch
from utils import colors_match


class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        super().__init__()

        # Sprite lists
        self.laser_list = arcade.SpriteList()
        self.glowball_shadertoy = Shadertoy.create_from_file(
            self.window.get_size(), "glow_ball.glsl"
        )

        self.explosion_list = []
        self.target_spawner = TargetSpawner(shadertoy=self.glowball_shadertoy)
        self.color_manager = ColorManager()
        self.swatch = Swatch((100, 100))
        self.color_bars = [
            ColorBar(
                position=(200 + 50 * index, 100),
                initial_value=self.color_manager.colors[index],
                color=color,
            )
            for index, color in enumerate(self.color_manager.color_names)
        ]
        self.score = 0

        self.start_new_game()

    def start_new_game(self):
        """Set up the game and initialize the variables."""

        arcade.set_background_color(arcade.csscolor.BLACK)
        self.laser_list = arcade.SpriteList()

        self.player_sprite = ShipSprite(
            ":resources:images/space_shooter/playerShip1_orange.png",
            SCALE,
        )

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        for laser in self.laser_list:
            laser.draw()

        self.laser_list.draw()
        for explosion in self.explosion_list:
            explosion.render()

        for bar in self.color_bars:
            bar.draw()

        self.player_sprite.draw()
        self.target_spawner.draw()
        self.swatch.draw()

        # arcade.draw_text("Score", start_x=SCREEN_WIDTH / 2, start_y=SCREEN_HEIGHT / 2)

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif symbol == arcade.key.Q:
            self.color_manager.delta_red = 1
        elif symbol == arcade.key.A:
            self.color_manager.delta_red = -1
        elif symbol == arcade.key.W:
            self.color_manager.delta_green = 1
        elif symbol == arcade.key.S:
            self.color_manager.delta_green = -1
        elif symbol == arcade.key.E:
            self.color_manager.delta_blue = 1
        elif symbol == arcade.key.D:
            self.color_manager.delta_blue = -1
        elif symbol == arcade.key.SPACE:
            color = self.color_manager.colors
            self.fire_circle(color)

    def fire_circle(self, laser_color):
        """Shoot a glowy ball in the specified color in the direction the ship is pointing."""

        laser_sprite = GlowBall(
            glowcolor=laser_color,
            radius=10,
            shadertoy=self.glowball_shadertoy,
        )
        self.set_laser_vector(laser_sprite, 5)  # change laser speed here

    def set_laser_vector(self, laser_sprite, laser_speed):
        """Calculate the direction the ship is currently firing lasers"""
        laser_sprite.change_y = (
            math.cos(math.radians(self.player_sprite.angle)) * laser_speed
        )
        laser_sprite.change_x = (
            -math.sin(math.radians(self.player_sprite.angle)) * laser_speed
        )

        laser_sprite.center_x = self.player_sprite.center_x
        laser_sprite.center_y = self.player_sprite.center_y

        self.laser_list.append(laser_sprite)

    def on_key_release(self, symbol, modifiers):
        """Called whenever a key is released."""
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.Q or symbol == arcade.key.A:
            self.color_manager.delta_red = 0
        elif symbol == arcade.key.W or symbol == arcade.key.S:
            self.color_manager.delta_green = 0
        elif symbol == arcade.key.E or symbol == arcade.key.D:
            self.color_manager.delta_blue = 0

    def on_update(self, delta_t):
        """Move everything"""

        self.laser_list.update()
        self.player_sprite.update()
        self.target_spawner.update()
        explosion_list_copy = self.explosion_list.copy()

        self.color_manager.update_colors()
        self.color_bars[0].set_value(self.color_manager.red)
        self.color_bars[1].set_value(self.color_manager.green)
        self.color_bars[2].set_value(self.color_manager.blue)
        self.swatch.set_color(self.color_manager.colors)

        for explosion in explosion_list_copy:
            explosion.update(delta_t)
            if explosion.time > 0.9:
                self.explosion_list.remove(explosion)

        for laser in self.laser_list:
            targets_hit = arcade.check_for_collision_with_list(
                laser, self.target_spawner.get_targets()
            )

            for target in targets_hit:
                if colors_match(laser.get_color(), target.get_color()):
                    self.target_spawner.remove_target(target)
                    explosion = ExplosionMaker(
                        self.window.get_size(),
                        target.position,
                        target.get_color(),
                    )
                    self.explosion_list.append(explosion)

            if len(targets_hit) > 0:
                laser.remove_from_sprite_lists()
            else:
                # Remove laser if it goes off-screen
                size = max(laser.width, laser.height)
                if laser.center_x < 0 - size:
                    laser.remove_from_sprite_lists()
                if laser.center_x > SCREEN_WIDTH + size:
                    laser.remove_from_sprite_lists()
                if laser.center_y < 0 - size:
                    laser.remove_from_sprite_lists()
                if laser.center_y > SCREEN_HEIGHT + size:
                    laser.remove_from_sprite_lists()

import math

import arcade
from arcade.experimental.shadertoy import Shadertoy

from constants import *
from ship_sprite import ShipSprite
from bullet import Bullet
from color_bar import ColorBar
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
        self.bullet_list = arcade.SpriteList()
        self.glowball_shadertoy = Shadertoy.create_from_file(
            self.window.get_size(), "glow_ball.glsl"
        )

        self.explosion_list = []
        self.target_spawner = TargetSpawner(shadertoy=self.glowball_shadertoy)
        self.red = int(255 / 2)
        self.green = int(255 / 2)
        self.blue = int(255 / 2)
        self.colors = [self.red, self.green, self.blue]
        self.delta_red = 0
        self.delta_green = 0
        self.delta_blue = 0
        self.swatch = Swatch((100, 100))
        self.color_bars = [
            ColorBar(
                position=(200 + 50 * index, 100),
                initial_value=self.colors[index],
                color=color,
            )
            for index, color in enumerate(["red", "green", "blue"])
        ]

        self.start_new_game()

    def start_new_game(self):
        """Set up the game and initialize the variables."""

        arcade.set_background_color(arcade.csscolor.BLACK)

        # Sprite lists
        self.bullet_list = arcade.SpriteList()

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

        for bullet in self.bullet_list:
            bullet.draw()

        self.bullet_list.draw()
        for explosion in self.explosion_list:
            explosion.render()

        for bar in self.color_bars:
            bar.draw()

        self.player_sprite.draw()
        self.target_spawner.draw()
        self.swatch.draw()

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""
        # Shoot if the player hit the space bar and we aren't respawning.
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif symbol == arcade.key.Q:
            self.delta_red = 1
        elif symbol == arcade.key.A:
            self.delta_red = -1
        elif symbol == arcade.key.W:
            self.delta_green = 1
        elif symbol == arcade.key.S:
            self.delta_green = -1
        elif symbol == arcade.key.E:
            self.delta_blue = 1
        elif symbol == arcade.key.D:
            self.delta_blue = -1
        elif symbol == arcade.key.SPACE:
            color = (self.red, self.green, self.blue)
            self.fire_circle(color)

    def fire_circle(self, bullet_color):
        bullet_sprite = GlowBall(
            glowcolor=bullet_color,
            radius=10,
            shadertoy=self.glowball_shadertoy,
        )
        self.set_bullet_vector(bullet_sprite, 5)  # change bullet speed here

    def set_bullet_vector(self, bullet_sprite, bullet_speed):
        bullet_sprite.change_y = (
            math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
        )
        bullet_sprite.change_x = (
            -math.sin(math.radians(self.player_sprite.angle)) * bullet_speed
        )

        bullet_sprite.center_x = self.player_sprite.center_x
        bullet_sprite.center_y = self.player_sprite.center_y

        self.bullet_list.append(bullet_sprite)

    def on_key_release(self, symbol, modifiers):
        """Called whenever a key is released."""
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.Q or symbol == arcade.key.A:
            self.delta_red = 0
        elif symbol == arcade.key.W or symbol == arcade.key.S:
            self.delta_green = 0
        elif symbol == arcade.key.E or symbol == arcade.key.D:
            self.delta_blue = 0

    def clamp_color(self, color_value):
        return max(min(color_value, 255), 0)

    def on_update(self, delta_t):
        """Move everything"""

        self.bullet_list.update()
        self.player_sprite.update()
        self.target_spawner.update()
        explosion_list_copy = self.explosion_list.copy()

        # TODO: clean this up
        self.red = self.clamp_color(self.red + self.delta_red)
        self.green = self.clamp_color(self.green + self.delta_green)
        self.blue = self.clamp_color(self.blue + self.delta_blue)
        self.color_bars[0].set_value(self.red)
        self.color_bars[1].set_value(self.green)
        self.color_bars[2].set_value(self.blue)
        self.swatch.set_color((self.red, self.green, self.blue))

        for explosion in explosion_list_copy:
            explosion.update(delta_t)
            if explosion.time > 0.9:
                self.explosion_list.remove(explosion)

        for bullet in self.bullet_list:
            assert isinstance(bullet, Bullet)
            targets_hit = arcade.check_for_collision_with_list(
                bullet, self.target_spawner.get_targets()
            )

            for target in targets_hit:
                if colors_match(bullet.get_color(), target.get_color()):
                    self.target_spawner.remove_target(target)
                    explosion = ExplosionMaker(
                        self.window.get_size(),
                        target.position,
                        target.get_color(),
                    )
                    self.explosion_list.append(explosion)

            if len(targets_hit) > 0:
                bullet.remove_from_sprite_lists()
            else:
                # Remove bullet if it goes off-screen
                size = max(bullet.width, bullet.height)
                if bullet.center_x < 0 - size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_x > SCREEN_WIDTH + size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y < 0 - size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y > SCREEN_HEIGHT + size:
                    bullet.remove_from_sprite_lists()

import random
import math
import arcade


from typing import cast
from arcade.experimental.shadertoy import Shadertoy

from constants import *

from ship_sprite import ShipSprite
from bullet import Bullet
from glow_line import GlowLine
from glow_ball import GlowBall
from explosion import ExplosionMaker
from glow_image_sprite import GlowImageSprite


class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        super().__init__()

        # Sprite lists
        self.bullet_list = arcade.SpriteList()

        self.glowball_shadertoy = Shadertoy.create_from_file(
            self.window.get_size(), "glow_ball.glsl"
        )
        self.glowline_shadertoy = Shadertoy.create_from_file(
            self.window.get_size(), "glow_line.glsl"
        )

        self.explosion_list = []

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

        self.player_sprite.draw()

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""
        # Shoot if the player hit the space bar and we aren't respawning.
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif symbol == arcade.key.KEY_1:
            color = (255, 128, 128)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_2:
            color = (128, 255, 128)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_3:
            color = (128, 128, 255)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_4:
            color = (255, 128, 255)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_5:
            color = (255, 255, 255)
            self.fire_line(color)
        elif symbol == arcade.key.KEY_6:
            color = (64, 255, 64)
            self.fire_line(color)
        elif symbol == arcade.key.KEY_7:
            bullet_sprite = GlowImageSprite(
                ":resources:images/space_shooter/laserBlue01.png",
                SCALE,
                glowcolor=arcade.color.WHITE,
                shadertoy=self.glowball_shadertoy,
            )
            self.set_bullet_vector(bullet_sprite, 13, self.player_sprite)

    def fire_circle(self, bullet_color):
        bullet_sprite = GlowBall(
            glowcolor=bullet_color,
            radius=5,
            shadertoy=self.glowball_shadertoy,
        )
        self.set_bullet_vector(bullet_sprite, 5)

    def fire_line(self, bullet_color):
        bullet_sprite = GlowLine(
            glowcolor=bullet_color,
            shadertoy=self.glowline_shadertoy,
        )
        self.set_bullet_vector(bullet_sprite, 13, self.player_sprite)

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

    def on_update(self, x):
        """Move everything"""

        self.bullet_list.update()
        self.player_sprite.update()
        explosion_list_copy = self.explosion_list.copy()
        for explosion in explosion_list_copy:
            explosion.update(x)
            if explosion.time > 0.9:
                self.explosion_list.remove(explosion)

        for bullet in self.bullet_list:
            assert isinstance(bullet, Bullet)
            # asteroids = arcade.check_for_collision_with_list(bullet, self.asteroid_list)

            # if len(asteroids) > 0:
            #     explosion = ExplosionMaker(self.window.get_size(), bullet.position)
            #     self.explosion_list.append(explosion)

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

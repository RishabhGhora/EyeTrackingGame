import math
import pygame
import time

from ConstantVars import Colors, Constants
from Utilities.EyeGazeInstance import EyeGazeInstance
from main_objects import ship_blueprint


class Spaceship(ship_blueprint.Ship):
    def __init__(self):
        # main_objects characteristics
        SPACESHIP_MAX_HEALTH = 10000
        SPACESHIP_HEIGHT = 80
        SPACESHIP_ICON = r'main_objects\\spaceship\\spaceship_icon.png'
        #SPACESHIP_ICON = r'main_objects/spaceship/spaceship_icon.png'
        TOP_LEFT = [
            int(Constants.CENTER[0] - SPACESHIP_HEIGHT / 2),
            int(Constants.CENTER[1] - SPACESHIP_HEIGHT / 2)
        ]
        super().__init__(SPACESHIP_MAX_HEALTH, TOP_LEFT, SPACESHIP_HEIGHT,
                         SPACESHIP_ICON, SPACESHIP_ICON)

        self.is_spaceship = True

        self.BULLET_SPEED = 10
        self.SHIELD_THICKNESS = 10
        self.SHIELD_LIFE = 6  # in seconds
        self.BASE_BULLET_DAMAGE = 5

        self.bullet_damage = self.BASE_BULLET_DAMAGE
        self.shield_start_time = 0
        self.time_begin_paused = 0
        self.duration_paused = 0
        self.rotated_image = None
        self.spaceship_bullet_color = Colors.RED

        self.last_angle_from_center = self.angle_from_center

        self.current_inventory = {"Bullet Power": 1}
        self.wallet = 0

        self.SHIELD_RADIUS = math.sqrt(
            (Constants.CENTER[0] - self.edges["top_left"][0]) ** 2 +
            (Constants.CENTER[1] - self.edges["top_left"][1]) ** 2
        )

        self.health_bar_pos = [
            int((self.edges["top_left"][0] + self.edges["bottom_right"][0])
                / 2),
            self.edges["top_left"][1]
        ]

    def update_ship(self, screen, mouse_instance: EyeGazeInstance, main):
        if self.has_shield:
            pygame.draw.circle(screen, Colors.WHITE, tuple(Constants.CENTER),
                               self.SHIELD_RADIUS)
            pygame.draw.circle(screen, Colors.BLACK, tuple(Constants.CENTER),
                               self.SHIELD_RADIUS - self.SHIELD_THICKNESS)
            if time.time() - self.shield_start_time \
                    - self.duration_paused > self.SHIELD_LIFE:
                self.remove_shield()

        self.update_spaceship_rotation(mouse_instance)
        if main.in_first_view:
            health_bar_pos_1st_view = [
                Constants.CENTER[0] - Constants.HEALTH_BAR_LEN / 2,
                Constants.CENTER[1] + 300
            ]
            self.update_health_bar(screen, health_bar_pos_1st_view)
        else:
            self.update_health_bar(screen, self.health_bar_pos)
            screen.blit(self.rotated_image, self.edges["top_left"])

        bullet_velocity = self.generate_bullet_velocity(mouse_instance,
                                                        main.in_first_view)
        self.fire_bullets(screen, self.bullet_damage,
                          bullet_velocity[0], bullet_velocity[1], main,
                          self.spaceship_bullet_color,
                          is_spaceship=self.is_spaceship)

    def generate_bullet_velocity(self, mouse_instance, in_first_view=False) \
            -> list:
        if in_first_view:
            BULLET_X_DEVIATION = 2
            if self.last_angle_from_center == self.angle_from_center:
                bullet_velocity = [0, -self.BULLET_SPEED]
            elif self.last_angle_from_center > self.angle_from_center:
                # turning left, means bullets go to the right
                bullet_velocity = [
                    BULLET_X_DEVIATION, -self.BULLET_SPEED
                ]
            else:
                # turning right, means bullets go to the left
                bullet_velocity = [
                    -BULLET_X_DEVIATION, -self.BULLET_SPEED
                ]
            self.last_angle_from_center = self.angle_from_center
        else:
            bullet_velocity = [
                self.BULLET_SPEED * mouse_instance.unit_x_displacement,
                self.BULLET_SPEED * mouse_instance.unit_y_displacement
            ]
        return bullet_velocity

    def update_spaceship_rotation(self, mouse_instance):
        if not self.ship_paused:
            self.angle_from_center = mouse_instance.angle_from_center
            self.rotated_image = pygame.transform.rotate(self.scaled_ship_image,
                                                         self.angle_from_center)

    def set_bullet_damage(self, new_damage: int):
        self.bullet_damage = new_damage

    def add_shield(self):
        shields_left = self.current_inventory.get("Shield", 0)
        if shields_left > 0:
            self.current_inventory["Shield"] = shields_left - 1
            self.has_shield = True
            self.shield_start_time = time.time()

    def remove_shield(self):
        self.has_shield = False
        self.time_begin_paused = 0
        self.duration_paused = 0

    def pause_ship(self):
        self.ship_paused = True
        if self.has_shield:
            self.time_begin_paused = time.time()

    def resume_ship(self):
        self.ship_paused = False
        if self.has_shield:
            self.duration_paused = time.time() - self.time_begin_paused

    def change_bullet_color(self, color: tuple):
        self.spaceship_bullet_color = color

    def update_inventory(self, order_cart: dict):
        for item, item_count in order_cart.items():
            self.current_inventory[item] = self.current_inventory.get(item, 0) \
                                           + item_count
            if item == "Bullet Power":
                if item_count <= 1:
                    self.set_bullet_damage(self.BASE_BULLET_DAMAGE)
                else:
                    self.set_bullet_damage(item_count * self.BASE_BULLET_DAMAGE)

    def update_wallet(self, change_in_cash: int):
        self.wallet += change_in_cash

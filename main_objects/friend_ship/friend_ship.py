from main_objects import ship_blueprint
from ConstantVars import GenFunctions, Constants, Colors
from Utilities import EyeGazeInstance
import random
import pygame
import time


class FriendShip(ship_blueprint.Ship):
    def __init__(self, friend_name):
        FRIEND_MAX_HEALTH = 100
        TOP_LEFT_INITIAL = GenFunctions.rand_coord()
        FRIEND_HEIGHT = 50
        FRIEND_SHIP_ICON = r'main_objects\\friend_ship\\friend_ship_icon.png'
        #FRIEND_SHIP_ICON = r'main_objects/friend_ship/friend_ship_icon.png'
        FIRST_VIEW_ICON = r'main_objects\\friend_ship\\friend_ship_3rd_icon.png'
        #FIRST_VIEW_ICON = r'main_objects/friend_ship/friend_ship_3rd_icon.png'

        super().__init__(FRIEND_MAX_HEALTH, TOP_LEFT_INITIAL, FRIEND_HEIGHT,
                         FRIEND_SHIP_ICON, FIRST_VIEW_ICON)
        self.SPEED = 8
        self.friend_name = friend_name
        self.time_initiated = time.time()
        self.TIME_LIMIT = 3  # in seconds
        self.time_begin_paused = 0  # in seconds
        self.duration_paused = 0

    def update_ship(self, screen, mouse_instance: EyeGazeInstance, main):
        health_bar_pos = [
            int((self.edges["top_left"][0] + self.edges["bottom_right"][0])
                / 2),
            self.edges["top_left"][1]
        ]
        self.update_health_bar(screen, health_bar_pos)

        # fire bullets
        x_unit_velocity = random.random() * 2 - 1  # [-1, 1]
        y_unit_velocity = random.random() * 2 - 1  # [-1, 1]
        bullet_velocity = [
            self.BULLET_SPEED * x_unit_velocity,
            self.BULLET_SPEED * y_unit_velocity
        ]
        self.fire_bullets(screen, Constants.BULLET_DAMAGE, bullet_velocity[0],
                          bullet_velocity[1], main)

        # rotate and move main_objects
        if not self.ship_paused:
            self.angle_from_center = random.randint(0, 359)
            self.update_coords(mouse_instance)
        rotated_image = pygame.transform. \
            rotate(self.scaled_ship_image, self.angle_from_center)
        screen.blit(rotated_image, self.edges["top_left"])

        # put name of friend
        name_label = Constants.FONTS["TEXT_FONT"].render(
            self.friend_name, True, Colors.WHITE)
        name_pos = [
            self.edges["top_left"][0] + self.scaled_ship_image.get_width() // 2
            - name_label.get_width() // 2,
            self.edges["top_left"][1] + self.scaled_ship_image.get_height()
            * 3 // 4
        ]
        screen.blit(name_label, tuple(name_pos))

        # kill the main_objects after a period of time
        # if not self.ship_paused \
        #         and time.time() - self.time_initiated - self.duration_paused \
        #         > self.TIME_LIMIT:
        #     self.out_of_range = False

    def update_coords(self, mouse_instance: EyeGazeInstance):
        self.edges["top_left"][0] = self.edges["top_left"][0] \
                                    - mouse_instance.unit_x_displacement \
                                    * self.SPEED
        self.edges["top_left"][1] = self.edges["top_left"][1] \
                                    - mouse_instance.unit_y_displacement \
                                    * self.SPEED
        self.update_edges(self.edges["top_left"])

        if GenFunctions.out_of_range(self.edges["top_left"][0],
                                     self.edges["top_left"][1]):
            self.out_of_range = True

    def pause_ship(self):
        self.ship_paused = True
        self.time_begin_paused = time.time()

    def resume_ship(self):
        self.ship_paused = False
        self.duration_paused = time.time() - self.time_begin_paused

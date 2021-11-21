import pygame
from Utilities import EyeGazeInstance
import math

from ConstantVars import Constants, GenFunctions
from main_objects import ship_blueprint


class EvilShip(ship_blueprint.Ship):
    def __init__(self):
        # main_objects characteristics
        SPACESHIP_MAX_HEALTH = 100
        SPACESHIP_HEIGHT = 50
        SPACESHIP_ICON = r'main_objects\\evil_ship\\evil_ship_icon.png'
        #SPACESHIP_ICON = r'main_objects/evil_ship/evil_ship_icon.png'
        FIRST_VIEW_ICON = r'main_objects\\evil_ship\\evil_ship_3rd_icon.png'
        #FIRST_VIEW_ICON = r'main_objects/evil_ship/evil_ship_3rd_icon.png'
        top_left_init = GenFunctions.rand_coord_padded()
        super().__init__(SPACESHIP_MAX_HEALTH, top_left_init, SPACESHIP_HEIGHT,
                         SPACESHIP_ICON, FIRST_VIEW_ICON)
        self.rotated_image = self.scaled_ship_image
        self.SPEED = 8
        self.BULLET_SPEED = 10
        self.out_of_range = False
        self.health = SPACESHIP_MAX_HEALTH

    def update_ship(self, screen, mouse_instance: EyeGazeInstance, main):
        if not self.ship_paused:
            self.update_coords(mouse_instance)
            self.update_rotation()

        if not self.is_alive():
            self.out_of_range = True

        bullet_velocity = self.generate_bullet_velocity(main.in_first_view)
        self.fire_bullets(screen, Constants.BULLET_DAMAGE,
                          bullet_velocity[0],
                          bullet_velocity[1], main)
        if main.in_first_view:
            if 0 <= self.first_view["angle_from_self_center"] <= 180:
                self.update_3rd_view_vars(main.spaceship.angle_from_center)
                screen.blit(self.first_view["final_rotated_image"],
                            self.first_view["final_screen_pos"])
            else:
                # if not viewable, don't project the ship on the screen but
                # don't remove it either
                return
        else:
            health_bar_pos = [
                int((self.edges["top_left"][0] + self.edges["bottom_right"][0])
                    / 2),
                self.edges["top_left"][1]
            ]
            self.update_health_bar(screen, health_bar_pos)
            screen.blit(self.rotated_image, self.edges["top_left"])

    def generate_bullet_velocity(self, in_first_view=False) -> list:
        bullet_velocity = [0, 0]
        if in_first_view:
            angle = self.first_view["angle_from_self_center"]
            bullet_velocity = [
                GenFunctions.abs_cos(angle) * self.BULLET_SPEED,
                GenFunctions.abs_sin(angle) * self.BULLET_SPEED,
            ]
            return bullet_velocity

        ship_quadrant = GenFunctions \
            .get_quadrant(0, 0, angle_from_center=self.angle_from_center)
        sine_angle_abs = math.fabs(math.sin(math.radians(
            self.angle_from_center)))
        cosine_angle_abs = math.fabs(math.cos(math.radians(
            self.angle_from_center)))

        if ship_quadrant == 1:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs * -1
        elif ship_quadrant == 2:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs * -1
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs * -1
        elif ship_quadrant == 3:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs * -1
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs
        else:
            bullet_velocity[0] = self.BULLET_SPEED * sine_angle_abs
            bullet_velocity[1] = self.BULLET_SPEED * cosine_angle_abs

        return bullet_velocity

    def update_3rd_view_vars(self, angle_of_spaceship):
        # update angle, distance, and height
        self.first_view["angle_from_mid_btm"] = \
            90 + self.angle_from_center - angle_of_spaceship
        self.first_view["angle_from_self_center"] = \
            270 - self.first_view["angle_from_mid_btm"]
        self.first_view["distance_to_mid_btm"] = \
            GenFunctions.dist(Constants.CENTER, self.get_center())
        self.first_view["current_height"] = \
            (Constants.MAX_CENTER_EDGE_DISTANCE
             - self.first_view["distance_to_mid_btm"]) \
            * self.first_view["HEIGHT_INC"] + self.first_view["BASE_HEIGHT"]

        # update the image itself
        self.first_view["scaled_image"] = pygame.transform.scale(
            self.first_view["raw_image"],
            (self.first_view["current_height"],
             self.first_view["current_height"])
        )
        self.first_view["final_rotated_image"] = pygame.transform. \
            rotate(self.first_view["scaled_image"],
                   self.first_view["angle_from_self_center"])
        self.first_view["final_screen_pos"] = [
            Constants.MID_BTM[0] - self.first_view["distance_to_mid_btm"]
            * math.fabs(math.cos(math.radians(
                self.first_view["angle_from_mid_btm"]))),
            Constants.MID_BTM[1] - self.first_view["distance_to_mid_btm"]
            * math.fabs(math.sin(math.radians(
                self.first_view["angle_from_mid_btm"]))),
        ]

    def update_rotation(self):
        ship_center = self.get_center()
        y_delta_from_center = ship_center[1] - Constants.CENTER[1]
        x_delta_from_center = ship_center[0] - Constants.CENTER[0]
        try:
            base_angle_from_center = math.degrees(
                math.atan(abs(y_delta_from_center) / abs(x_delta_from_center)))
        except ZeroDivisionError:
            # keep last rotation
            return
        quadrant = GenFunctions.get_quadrant(ship_center[0], ship_center[1])
        if quadrant == 1:
            self.angle_from_center = 90 + base_angle_from_center
        elif quadrant == 2:
            self.angle_from_center = 270 - base_angle_from_center
        elif quadrant == 3:
            self.angle_from_center = 270 + base_angle_from_center
        elif quadrant == 4:
            self.angle_from_center = 90 - base_angle_from_center
        self.rotated_image = pygame.transform. \
            rotate(self.scaled_ship_image, self.angle_from_center)

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

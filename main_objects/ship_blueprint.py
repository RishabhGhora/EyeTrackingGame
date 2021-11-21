import random
import pygame
from Utilities import EyeGazeInstance
from ConstantVars import Constants, Colors, GenFunctions


class Ship:
    def __init__(self, max_health: int, top_left: list, height: int, icon: str,
                 first_view_icon: str):
        # main_objects characteristics
        self.id = random.randint(0, 10_000)
        self.angle_from_center = 0  # counterclockwise, in deg
        self.MAX_HEALTH = max_health
        self.health = self.MAX_HEALTH
        self.bullets = []
        self.has_shield = False
        self.out_of_range = False
        self.ship_paused = False
        self.BULLET_SPEED = 10
        self.is_spaceship = False

        # loading main_objects image
        self.raw_spaceship_image = pygame.image.load(icon)
        self.ship_height = height
        self.scaled_ship_image = pygame.transform.scale(
            self.raw_spaceship_image, (self.ship_height, self.ship_height))
        self.ship_image_width = self.scaled_ship_image.get_width()
        self.ship_image_height = self.scaled_ship_image.get_height()
        self.edges = dict()
        self.update_edges(top_left)

        self.first_view = {
            "BASE_HEIGHT": 50.0,
            "HEIGHT_INC": 0.25,
            "current_height": 50.0,  # range = [50, 356.86]
            "raw_image": pygame.image.load(first_view_icon),
            "scaled_image": None,
            "final_rotated_image": None,
            "angle_from_mid_btm": 0.0,  # counterclockwise, deg, range=[0, 180]
            "angle_from_self_center": 0.0,  # counterclockwise, deg, [0, 360)
            "distance_to_mid_btm": 0.0,
            "health_bar_pos": [0, 0],
            "final_screen_pos": [0, 0]
        }
        self.first_view["scaled_image"] = pygame.transform.scale(
            self.first_view["raw_image"],
            (self.first_view["current_height"],
             self.first_view["current_height"])
        )

    def rescale_ship(self, new_height):
        self.ship_height = new_height
        self.scaled_ship_image = pygame.transform.scale(
            self.raw_spaceship_image, (self.ship_height, self.ship_height))

    def update_ship(self, screen, mouse_instance: EyeGazeInstance, main):
        raise NotImplementedError

    def update_edges(self, top_left: list):
        bottom_right = [
            top_left[0] + self.ship_image_width,
            top_left[1] + self.ship_image_height]
        self.edges = {
            "top_left": top_left,
            "bottom_right": bottom_right
        }

    def update_3rd_view_vars(self, angle_of_spaceship):
        raise NotImplementedError

    def get_rect(self):
        return pygame.Rect(tuple(self.edges["top_left"]),
                           (self.ship_image_width, self.ship_image_height))

    def update_health_bar(self, screen, health_bar_pos: list):
        pygame.draw.rect(screen, Colors.WHITE, (health_bar_pos[0],
                                                health_bar_pos[1],
                                                Constants.HEALTH_BAR_LEN,
                                                Constants.HEALTH_BAR_HEIGHT))
        current_bar_len = self.health / self.MAX_HEALTH \
                          * Constants.HEALTH_BAR_LEN
        pygame.draw.rect(screen, Colors.RED, (health_bar_pos[0],
                                              health_bar_pos[1],
                                              current_bar_len,
                                              Constants.HEALTH_BAR_HEIGHT))

    def fire_bullets(self, screen, damage: int, x_velocity, y_velocity, main,
                     bullet_color: tuple = Colors.RED, is_spaceship=False):
        if main.in_first_view:
            if is_spaceship:
                ship_center = Constants.MID_BTM
            else:
                ship_center = self.first_view["final_screen_pos"]
        else:
            ship_center = self.get_center()
        new_bullet = ShipBullet(ship_center, damage, x_velocity, y_velocity,
                                bullet_color)
        self.bullets.append(new_bullet)

        bullets_to_remove = set()
        for bullet_i, bullet in enumerate(self.bullets):
            bullet.update_screen_pos(screen, self.ship_paused)
            if bullet.out_of_range:
                bullets_to_remove.add(bullet_i)

        while len(self.bullets) > 100:
            self.bullets.pop(0)

        if not self.ship_paused:
            for other_ship in main.all_ships:
                if other_ship.id != self.id:
                    for bullet_i, bullet in enumerate(self.bullets):
                        if other_ship.analyze_hit(bullet.get_coord(),
                                                  bullet.get_damage()):
                            bullets_to_remove.add(bullet_i)

            for bullet_to_remove in bullets_to_remove:
                try:
                    self.bullets.pop(bullet_to_remove)
                except IndexError:
                    self.bullets.pop()

        bullets_to_remove.clear()

    def analyze_hit(self, bullet_coord: list, damage: int) -> bool:
        if self.edges["top_left"][0] <= bullet_coord[0] <= \
                self.edges["bottom_right"][0] \
                and self.edges["top_left"][1] <= bullet_coord[1] <= \
                self.edges["bottom_right"][1]:
            if self.has_shield or not self.is_alive():
                return True
            else:
                self.reduce_health(damage)
                return True
        return False

    def reduce_health(self, damage: int):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self) -> bool:
        return self.health > 0

    def get_center(self) -> list:
        return [
            int((self.edges["top_left"][0]
                 + self.edges["bottom_right"][0]) / 2),
            int((self.edges["top_left"][1]
                 + self.edges["bottom_right"][1]) / 2),
        ]

    def pause_ship(self):
        self.ship_paused = True

    def resume_ship(self):
        self.ship_paused = False

    def clear_all_bullets(self):
        self.bullets.clear()


class ShipBullet:
    def __init__(self, ship_center: list, damage: int, x_velocity, y_velocity,
                 color=Colors.RED, height: int = 3):
        self.coord = [ship_center[0], ship_center[1]]
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.out_of_range = False
        self.damage = damage
        self.color = color
        self.height = height

    def update_screen_pos(self, screen, ship_paused):
        if not ship_paused:
            self.coord = [
                self.coord[0] + self.x_velocity,
                self.coord[1] + self.y_velocity
            ]
            if self.coord[0] > Constants.WINDOW_WIDTH \
                    or self.coord[1] > Constants.WINDOW_HEIGHT:
                self.out_of_range = True
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.coord[0], self.coord[1],
                                     self.height, self.height))

    def get_damage(self) -> int:
        return self.damage

    def get_coord(self) -> list:
        return self.coord

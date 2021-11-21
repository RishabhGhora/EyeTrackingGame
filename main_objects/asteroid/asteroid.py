import pygame
import math
from ConstantVars import GenFunctions, Constants, Colors


class Asteroid:
    def __init__(self):
        self.is_paused = False
        self.top_left = GenFunctions.rand_coord_padded()
        self.ASTEROID_HEIGHT = 50
        self.ASTEROID_SPEED = 15
        self.DAMAGE = 100
        #SPACESHIP_ICON = r'main_objects\\asteroid\\asteroid_icon.jpg'
        SPACESHIP_ICON = r'main_objects/asteroid/asteroid_icon.jpg'

        raw_asteroid_image = pygame.image.load(SPACESHIP_ICON)
        self.scaled_asteroid_image = pygame.transform \
            .scale(raw_asteroid_image,
                   (self.ASTEROID_HEIGHT, self.ASTEROID_HEIGHT))

        self.asteroid_velocity = self.generate_asteroid_velocity()
        self.angle_from_center = 0

    def update_asteroid(self, screen, game_is_paused=False):
        self.update_rotation()
        if not game_is_paused:
            self.update_coords()
        rotated_asteroid = pygame.transform. \
            rotate(self.scaled_asteroid_image, self.angle_from_center)
        screen.blit(rotated_asteroid, self.top_left)

    def analyze_strike(self, strike_x_coords: list = None,
                       strike_y_coords: list = None) -> bool:
        """
        Analyzes the finger strike against the asteroid's position.
        :param strike_x_coords: list of all x-coordinates of given finger
        gesture
        :param strike_y_coords: list of all y-coordinates of given finger
        gesture
        :return: True if the finger gesture hits the asteroid. Else, False.
        """
        if strike_x_coords is None or strike_y_coords is None:
            return False
        asteroid_rect = pygame.Rect(tuple(self.top_left),
                                    (self.ASTEROID_HEIGHT,
                                     self.ASTEROID_HEIGHT))
        for x, y in zip(strike_x_coords, strike_y_coords):
            if asteroid_rect.collidepoint(x, y):
                return True
        return False

    def analyze_hit(self, spaceship) -> bool:
        asteroid_rect = pygame.Rect(tuple(self.top_left),
                                    (self.ASTEROID_HEIGHT,
                                     self.ASTEROID_HEIGHT))
        if asteroid_rect.colliderect(spaceship.get_rect()):
            if spaceship.has_shield is False:
                spaceship.reduce_health(self.DAMAGE)
            return True
        else:
            return False

    def get_center(self) -> list:
        return [
            self.top_left[0] + self.ASTEROID_HEIGHT / 2,
            self.top_left[1] + self.ASTEROID_HEIGHT / 2
        ]

    def update_coords(self):
        self.top_left[0] += self.asteroid_velocity[0]
        self.top_left[1] += self.asteroid_velocity[1]

    def update_rotation(self):
        self.angle_from_center = (self.angle_from_center + 1 % 360)

    def generate_asteroid_velocity(self) -> list:
        asteroid_center = self.get_center()
        x_delta_from_center = asteroid_center[0] - Constants.CENTER[0]
        y_delta_from_center = asteroid_center[1] - Constants.CENTER[1]
        try:
            base_angle_from_center = math.degrees(
                math.atan(abs(y_delta_from_center) / abs(x_delta_from_center)))
        except ZeroDivisionError:
            if y_delta_from_center >= 0:
                base_angle_from_center = 180
            else:
                base_angle_from_center = 0
        quadrant = GenFunctions.get_quadrant(asteroid_center[0],
                                             asteroid_center[1])
        if quadrant == 1:
            angle_from_center = 90 + base_angle_from_center
        elif quadrant == 2:
            angle_from_center = 270 - base_angle_from_center
        elif quadrant == 3:
            angle_from_center = 270 + base_angle_from_center
        else:
            angle_from_center = 90 - base_angle_from_center

        # possibly unnecessary if asteroid_quadrant == quadrant
        asteroid_velocity = [0, 0]
        asteroid_quadrant = GenFunctions \
            .get_quadrant(0, 0, angle_from_center=angle_from_center)
        sine_angle_abs = math.fabs(math.sin(math.radians(
            angle_from_center)))
        cosine_angle_abs = math.fabs(math.cos(math.radians(
            angle_from_center)))

        if asteroid_quadrant == 1:
            asteroid_velocity[0] = self.ASTEROID_SPEED * sine_angle_abs
            asteroid_velocity[1] = self.ASTEROID_SPEED * cosine_angle_abs * -1
        elif asteroid_quadrant == 2:
            asteroid_velocity[0] = self.ASTEROID_SPEED * sine_angle_abs * -1
            asteroid_velocity[1] = self.ASTEROID_SPEED * cosine_angle_abs * -1
        elif asteroid_quadrant == 3:
            asteroid_velocity[0] = self.ASTEROID_SPEED * sine_angle_abs * -1
            asteroid_velocity[1] = self.ASTEROID_SPEED * cosine_angle_abs
        else:
            asteroid_velocity[0] = self.ASTEROID_SPEED * sine_angle_abs
            asteroid_velocity[1] = self.ASTEROID_SPEED * cosine_angle_abs

        return asteroid_velocity

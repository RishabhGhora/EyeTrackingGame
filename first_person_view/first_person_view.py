from ConstantVars import Constants, Colors
import pygame


class FirstPersonView:
    def __init__(self):
        self.angle_of_spaceship = 180
        self.ANGLE_VIEWABLE_EACH_SIDE = 90
        self.triangle_sides = []
        self.draw_triangle_base()

    def update_view(self, screen, spaceship_angle):
        self.update_triangle_base(screen)
        self.angle_of_spaceship = spaceship_angle

    def draw_triangle_base(self):
        btm_mid = [Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT]
        self.triangle_sides = [
            [btm_mid[0] - 300, btm_mid[1]],
            [btm_mid[0] + 300, btm_mid[1]],
            [btm_mid[0], btm_mid[1] - 150],
        ]

    def update_triangle_base(self, screen):
        pygame.draw.polygon(screen, Colors.WHITE, self.triangle_sides)

    def within_view(self, other_object_angle: float) -> bool:
        """
        Returns True if the other ship's or asteroid's angle is within the
        180 degree view of the ship from the cockpit.
        Citation: https://stackoverflow.com/a/12234633/11031425
        :param other_object_angle: ship or asteroid's angle counterclockwise
        from vertical axis
        :return: True if the other ship's or asteroid's angle is within the
        180 degree view of the ship from the cockpit. False otherwise.
        """
        angle_diff = (self.angle_of_spaceship - other_object_angle + 180
                      + 360) % 360 - 180
        in_view = self.ANGLE_VIEWABLE_EACH_SIDE >= \
                  angle_diff >= -self.ANGLE_VIEWABLE_EACH_SIDE
        return in_view


if __name__ == "__main__":
    pass

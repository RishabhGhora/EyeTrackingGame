import math
from ConstantVars import Constants, GenFunctions


class EyeGazeInstance:
    def __init__(self, scaled_pupil_right_coords: list):
        # self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_x, self.mouse_y = scaled_pupil_right_coords
        x_delta = self.mouse_x - Constants.CENTER[0]
        y_delta = self.mouse_y - Constants.CENTER[1]
        self.quadrant = GenFunctions.get_quadrant(self.mouse_x, self.mouse_y)

        self.base_mouse_angle = 0  # in radians, from x-axis
        self.angle_from_center = 0  # counterclockwise, in deg
        """
        The unit displacement from the center, where the hypotenuse formed by 
        the unit_x_displacement and unit_y_displacement is 1
        """
        self.unit_x_displacement = 0  # from center
        self.unit_y_displacement = 0  # from center
        try:
            self.base_mouse_angle = math.atan(abs(y_delta) / abs(x_delta))
        except ZeroDivisionError:
            # don't change base_mouse_angle
            pass
        self.unit_x_displacement = math.cos(self.base_mouse_angle)
        self.unit_y_displacement = math.sin(self.base_mouse_angle)
        if self.quadrant == 1:
            self.angle_from_center = 270 + math.degrees(self.base_mouse_angle)
            self.unit_y_displacement = -self.unit_y_displacement
        elif self.quadrant == 2:
            self.angle_from_center = 90 - math.degrees(self.base_mouse_angle)
            self.unit_x_displacement = -self.unit_x_displacement
            self.unit_y_displacement = -self.unit_y_displacement
        elif self.quadrant == 3:
            self.angle_from_center = 90 + math.degrees(self.base_mouse_angle)
            self.unit_x_displacement = -self.unit_x_displacement
        elif self.quadrant == 4:
            self.angle_from_center = 270 - math.degrees(self.base_mouse_angle)


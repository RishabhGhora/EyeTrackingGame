import pygame.draw
from ConstantVars import Constants, Colors
import random, math


def out_of_range(x: int, y: int) -> bool:
    return (x < 0 or x > Constants.WINDOW_WIDTH
            or y < 0 or y > Constants.WINDOW_HEIGHT)


def rand_coord() -> list:
    x = random.randint(0, Constants.WINDOW_WIDTH)
    y = random.randint(0, Constants.WINDOW_HEIGHT)
    return [x, y]


def rand_coord_padded(CENTER_PADDING: int = 40) -> list:
    """
    :return: a random coordinate not located near center of screen
    """
    if random.random() >= 0.5:
        x = random.randint(Constants.CENTER[0] + CENTER_PADDING,
                           Constants.WINDOW_WIDTH)
    else:
        x = random.randint(0, Constants.CENTER[0] - CENTER_PADDING)
    if random.random() >= 0.5:
        y = random.randint(Constants.CENTER[1] + CENTER_PADDING,
                           Constants.WINDOW_HEIGHT)
    else:
        y = random.randint(0, Constants.CENTER[1] - CENTER_PADDING)
    return [x, y]


def get_quadrant(x_pos: int, y_pos: int,
                 angle_from_center: float = None) -> int:
    if angle_from_center is not None:
        if angle_from_center <= 90:
            return 2
        elif angle_from_center <= 180:
            return 3
        elif angle_from_center <= 270:
            return 4
        else:
            return 1

    # with respect to center of screen
    x_center = Constants.CENTER[0]
    y_center = Constants.CENTER[1]
    if x_pos >= x_center and y_pos < y_center:
        return 1
    elif x_pos < x_center and y_pos < y_center:
        return 2
    elif x_pos < x_center and y_pos >= y_center:
        return 3
    elif x_pos >= x_center and y_pos >= y_center:
        return 4


def draw_point(screen, coords: list):
    pygame.draw.rect(screen, Colors.WHITE, (coords[0], coords[1], 3, 3))


def draw_circle_alpha(surface, color, center: tuple, radius):
    """
    Draws a semi-transparent circle.
    Citation: https://stackoverflow.com/a/64630102/11031425
    :param surface: surface to draw circle on
    :param color: color in RGBA e.g. (255, 255, 0, 127)
    :param center: center coord of circle
    :param radius: radius of circle
    :return: None
    """
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def dist(p: list, q: list) -> float:
    """
    Returns the Euclidean distance between points p and q. Tries to emulate
    Python 3.8's math.dist(p, q) function.
    Citation: https://docs.python.org/3/library/math.html
    :param p: A multi-dimensional (dimension >= 1) point in the form of a list
    :param q: A multi-dimensional (dimension >= 1) point in the form of a list
    :return: Euclidean distance between points p and q
    """
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def abs_sin(deg: float) -> float:
    return math.fabs(math.sin(math.radians(deg)))


def abs_cos(deg: float) -> float:
    return math.fabs(math.cos(math.radians(deg)))

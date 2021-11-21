import math

WINDOW_WIDTH = 1244
WINDOW_HEIGHT = 700
CENTER = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]  # [622, 350]
FPS = 10
HEALTH_BAR_LEN = 20
HEALTH_BAR_HEIGHT = 2
FONTS = {}
BULLET_DAMAGE = 5
POSSIBLE_PLANETS = \
    ["Banronope", "Tenkanides", "Todruna", "Kegnerth", "Marus", "Iunus",
     "Phimoter", "Mithuhiri", "Gars 9R1K", "Soth LPO"]
CHANGE_PLANET_THRESHOLD = 0.3
ASTEROID_PROBABILITY = 0.3
MAX_CENTER_EDGE_DISTANCE = \
    math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip([0, 0], CENTER)))
MID_BTM = [WINDOW_WIDTH / 2, WINDOW_HEIGHT]


def initiate_constants(pygame):
    generate_fonts(pygame)


def generate_fonts(pygame):
    FONTS["HEADING_1_FONT"] = pygame.font.SysFont("arial", 18)
    FONTS["HEADING_2_FONT"] = pygame.font.SysFont("arial", 15)
    FONTS["TEXT_FONT"] = pygame.font.SysFont("arial", 11)

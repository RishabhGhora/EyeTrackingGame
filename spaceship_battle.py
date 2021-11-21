import pygame
import random
from main_objects.spaceship import Spaceship
from main_objects.evil_ship import EvilShip
from main_objects.friend_ship import friend_ship
from main_objects.asteroid.asteroid import Asteroid
from ConstantVars import Colors, Constants, GenFunctions
from Utilities import EyeGazeInstance
from Utilities.nine_sq_recognizer import NineSquareRecognizer
from AltScreens.request_support import RequestSupport
from AltScreens.settings import Settings
from AltScreens.market import Market
import cv2
from Utilities.gaze_tracking import GazeTracking
from first_person_view.first_person_view import FirstPersonView


class SpaceshipBattle:
    def __init__(self):
        self.run = True
        self.clock = pygame.time.Clock()

        self.spaceship = None
        self.all_ships = []
        self.finger_x_array = []
        self.finger_y_array = []
        self.asteroids = []
        self.finger_id = set()
        self.MINIMUM_SHIPS = 5
        self.MAXIMUM_SHIPS = 25

        self.game_is_paused = False
        self.current_planet = random.choice(Constants.POSSIBLE_PLANETS)
        self.in_first_view = False
        self.first_view = None

        # alt screens
        self.req_support = None
        self.settings_panel = None
        self.market = None

        self.webcam = None
        self.gaze = None
        self.scaled_pupil_right_coords = [0, 0]  # based on min and max recorded
        self.min_pupil_right_coords = [10000, 10000]
        self.max_pupil_right_coords = [0, 0]
        # when min and max pupil coords are no longer equal
        self.eye_coords_able_to_scale = False

        screen = self.initiate_game()
        self.run_game(screen)

    def initiate_game(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

        self.first_view = FirstPersonView()

        pygame.init()
        Constants.initiate_constants(pygame)

        screen = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                          Constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Spaceship Battle")

        # make ships
        self.spaceship = Spaceship.Spaceship()
        self.all_ships.append(self.spaceship)
        for _ in range(random.randint(3, 10)):
            evil_ship = EvilShip.EvilShip()
            self.all_ships.append(evil_ship)

        return screen

    def run_game(self, screen):
        while self.run:
            pygame.time.delay(100)

            self.collect_eye_data()
            self.update_components(screen)

            pygame.display.update()

        self.exit_game()

    def collect_eye_data(self):
        _, frame = self.webcam.read()
        self.gaze.refresh(frame)

        new_frame = self.gaze.annotated_frame()
        text = ""

        if self.gaze.is_right():
            text = "Looking right"
        elif self.gaze.is_left():
            text = "Looking left"
        elif self.gaze.is_center():
            text = "Looking center"

        # calculating eye position scaled
        # as we have more data, the scale gets better
        coord = self.gaze.pupil_right_coords()
        if coord is not None:
            self.min_pupil_right_coords = [
                min(self.min_pupil_right_coords[0], coord[0]),
                min(self.min_pupil_right_coords[1], coord[1])
            ]
            self.max_pupil_right_coords = [
                max(self.max_pupil_right_coords[0], coord[0]),
                max(self.max_pupil_right_coords[1], coord[1])
            ]
            if not self.eye_coords_able_to_scale:
                if self.min_pupil_right_coords[0] \
                        != self.max_pupil_right_coords[0] \
                        and self.min_pupil_right_coords[1] \
                        != self.max_pupil_right_coords[1]:
                    self.eye_coords_able_to_scale = True
            else:
                x_scaled = (coord[0] - self.min_pupil_right_coords[0]) / \
                           (self.max_pupil_right_coords[0]
                            - self.min_pupil_right_coords[0]) \
                           * Constants.WINDOW_WIDTH
                y_scaled = (coord[1] - self.min_pupil_right_coords[1]) / \
                           (self.max_pupil_right_coords[1]
                            - self.min_pupil_right_coords[1]) \
                           * Constants.WINDOW_HEIGHT
                self.scaled_pupil_right_coords = [x_scaled, y_scaled]

        # blinking is disabled until better implementation is procured
        # if self.gaze.is_blinking():
        #     print(f'True {time.time()}')

        cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2,
                    (255, 0, 0), 2)
        cv2.imshow("Eye Tracker", new_frame)

        # if Esc or 'X' close key clicked
        if cv2.waitKey(1) == 27 \
                or cv2.getWindowProperty("Eye Tracker",
                                         cv2.WND_PROP_VISIBLE) == 0:
            self.run = False

    def update_components(self, screen):
        for event in pygame.event.get():
            # reset screen
            screen.fill(Colors.BLACK)

            # update ships and bullets
            self.update_ships_and_bullets(screen)

            # check for any inputs
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                self.run = False
                break
            elif event.type == pygame.FINGERDOWN:
                # Citation: https://www.patreon.com/posts/
                # finger-painting-43786073?l=fr
                if not self.game_is_paused:
                    self.finger_id.add(event.finger_id)
            elif event.type == pygame.FINGERMOTION:
                if not self.game_is_paused:
                    self.finger_x_array.append(event.x
                                               * Constants.WINDOW_WIDTH)
                    self.finger_y_array.append(event.y
                                               * Constants.WINDOW_HEIGHT)
            elif event.type == pygame.FINGERUP:
                if not self.game_is_paused:
                    if len(self.finger_id) == 1 \
                            and len(self.finger_x_array) > 1:
                        drawing_candidate = \
                            NineSquareRecognizer(self.finger_x_array,
                                                 self.finger_y_array) \
                                .get_template_answer()
                        print(f"drawing_candidate = {drawing_candidate}")
                        if drawing_candidate == ">":
                            self.request_support()
                        elif drawing_candidate == "<":
                            self.open_settings()
                        elif drawing_candidate == "^":
                            self.open_market()
                        elif drawing_candidate == "O":
                            self.spaceship.add_shield()
                        elif drawing_candidate == "/":
                            asteroid_to_remove = None
                            for asteroid in self.asteroids:
                                if asteroid.analyze_strike(self.finger_x_array,
                                                           self.finger_y_array):
                                    asteroid_to_remove = asteroid
                                    break
                            if asteroid_to_remove is not None:
                                try:
                                    self.asteroids.remove(asteroid_to_remove)
                                except ValueError:
                                    pass
                    elif len(self.finger_id) == 4 \
                            and len(self.finger_x_array) > 1:
                        self.in_first_view = not self.in_first_view
                    self.finger_x_array.clear()
                    self.finger_y_array.clear()
                    self.finger_id.clear()

            # update all alternative screens
            alt_screen_returns = self.update_alt_screens(screen, event)
            if alt_screen_returns is not None:
                if self.req_support is not None:
                    friends_requested = alt_screen_returns
                    self.add_allies(friends_requested)
                    self.req_support = None
                    self.resume_game()
                elif self.settings_panel is not None:
                    new_bullet_color = alt_screen_returns["bullet_color"]
                    self.settings_panel = None
                    self.change_spaceship_bullet_color(new_bullet_color)
                    self.resume_game()
                elif self.market is not None:
                    self.market = None
                    self.resume_game()

        screen.fill(Colors.BLACK)
        if self.in_first_view:
            self.first_view.update_view(screen,
                                        self.spaceship.angle_from_center)
        self.update_finger_trace(screen)
        self.update_stars(screen)
        self.update_asteroids(screen)
        self.update_ships_and_bullets(screen)
        self.update_alt_screens(screen, None)
        if random.random() < Constants.CHANGE_PLANET_THRESHOLD:
            self.randomly_change_planet()
        if len(self.asteroids) == 0 and not self.in_first_view:
            self.asteroids.append(Asteroid())

        self.clock.tick(Constants.FPS)

    def update_asteroids(self, screen):
        asteroids_to_remove = []
        for asteroid in self.asteroids:
            asteroid.update_asteroid(screen, self.game_is_paused)

            if asteroid.analyze_hit(self.spaceship):
                # if got hit, remove the spaceship
                asteroids_to_remove.append(asteroid)
        for asteroid_to_remove in asteroids_to_remove:
            try:
                self.asteroids.remove(asteroid_to_remove)
            except ValueError:
                pass

    def randomly_change_planet(self):
        self.current_planet = random.choice(Constants.POSSIBLE_PLANETS)

    def open_market(self):
        self.pause_game()
        self.market = Market(self.spaceship, self.current_planet)

    def change_spaceship_bullet_color(self, color):
        self.spaceship.change_bullet_color(color)

    def update_alt_screens(self, screen, event=None):
        if self.game_is_paused:
            if self.req_support is not None:
                friends_requested = self.req_support.update_gui(screen, event)
                return friends_requested
            elif self.settings_panel is not None:
                new_bullet_color = self.settings_panel.update_gui(screen, event)
                return new_bullet_color
            elif self.market is not None:
                return self.market.update_gui(screen, event)
        return None

    def pause_game(self):
        print("GAME IS PAUSED")
        self.game_is_paused = True
        for ship in self.all_ships:
            ship.pause_ship()

    def resume_game(self):
        print("GAME IS RESUMED")
        self.game_is_paused = False
        for ship in self.all_ships:
            ship.resume_ship()

    def add_allies(self, friends_requested):
        for friend in friends_requested:
            self.all_ships.append(friend_ship.FriendShip(friend))

    def update_finger_trace(self, screen):
        for x, y in zip(self.finger_x_array, self.finger_y_array):
            GenFunctions.draw_circle_alpha(screen,
                                           tuple(Colors.HALF_TRANSPARENT_WHITE),
                                           (x, y),
                                           5)

    def update_stars(self, screen):
        NUMBER_OF_STARS = 10
        for _ in range(NUMBER_OF_STARS):
            GenFunctions.draw_point(screen, GenFunctions.rand_coord())

    def request_support(self):
        self.pause_game()
        self.req_support = RequestSupport()

    def open_settings(self):
        self.pause_game()
        self.settings_panel = Settings(self.spaceship.spaceship_bullet_color)

    def update_ships_and_bullets(self, screen):
        mouse_instance = EyeGazeInstance.EyeGazeInstance(
            self.scaled_pupil_right_coords)
        ships_to_remove = set()
        for ship_i, ship in enumerate(self.all_ships):
            ship.update_ship(screen, mouse_instance, self)
            if ship.out_of_range:
                ships_to_remove.add(ship_i)

        # remove ships out of range
        for ship_to_remove in ships_to_remove:
            try:
                self.all_ships.pop(ship_to_remove)
            except IndexError:
                print(f"Unable to remove ship #{ship_to_remove}")
        ships_to_remove.clear()

        if len(self.all_ships) < self.MINIMUM_SHIPS:
            self.all_ships.append(EvilShip.EvilShip())

        while len(self.all_ships) > self.MAXIMUM_SHIPS:
            # if too many ships, remove a random ship that is not the main
            # spaceship
            if self.all_ships[0].is_spaceship:
                self.all_ships.pop(1)
            else:
                self.all_ships.pop(0)

    def exit_game(self):
        print("EXITING...")
        pygame.quit()
        self.webcam.release()
        cv2.destroyAllWindows()


def main():
    SpaceshipBattle()


if __name__ == "__main__":
    main()

import random
from ConstantVars import Constants, Colors
import pygame.draw
from Utilities.button import Button


class RequestSupport:
    def __init__(self):
        self.available_friends = []
        self.friends_requested = set()
        self.FRIEND_PIC_HEIGHT = 50
        self.GENERAL_MARGIN = 10
        self.LEFT_MARGIN = 20
        self.reset_friends()
        self.buttons = []
        self.draw_apply_button()

    def draw_background(self, screen):
        # citation for translucent: https://stackoverflow.com/questions/
        # 6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
        translucent_surface = pygame.Surface((Constants.WINDOW_WIDTH,
                                              Constants.WINDOW_HEIGHT))
        translucent_surface.set_alpha(128)  # alpha level
        translucent_surface.fill(Colors.WHITE)  # this fills the entire surface
        screen.blit(translucent_surface, (0, 0))

        background = pygame.Surface((Constants.WINDOW_WIDTH / 2,
                                     Constants.WINDOW_HEIGHT))
        background.fill(Colors.WHITE)  # this fills the entire surface
        screen.blit(background, (int(Constants.WINDOW_WIDTH / 2), 0))

    def draw_friends_pictures(self, screen, friend_i, friend):
        # draw profile pic
        friend_pic_pos = [
            Constants.WINDOW_WIDTH // 2 + self.LEFT_MARGIN,
            self.GENERAL_MARGIN + (self.GENERAL_MARGIN + self.FRIEND_PIC_HEIGHT)
            * friend_i
        ]
        friend_pic_color = Colors.BLACK
        if friend in self.friends_requested:
            friend_pic_color = Colors.INDIGO
        pygame.draw.rect(screen, friend_pic_color,
                         (friend_pic_pos[0], friend_pic_pos[1],
                          self.FRIEND_PIC_HEIGHT, self.FRIEND_PIC_HEIGHT))

        # draw names
        # make Request Support text
        friend_name_color = Colors.WHITE
        friend_name_label = Constants.FONTS["TEXT_FONT"].render(
            friend, True, friend_name_color)
        friend_name_pos = [
            Constants.WINDOW_WIDTH / 2 + self.LEFT_MARGIN
            + self.FRIEND_PIC_HEIGHT / 2 - friend_name_label.get_width() / 2,
            self.GENERAL_MARGIN + (self.GENERAL_MARGIN + self.FRIEND_PIC_HEIGHT)
            * friend_i + self.FRIEND_PIC_HEIGHT * 3 / 4
        ]
        screen.blit(friend_name_label, tuple(friend_name_pos))

    def draw_support_buttons(self, screen, friend_i, friend, event=None):
        # make button
        request_button_pos = [
            Constants.WINDOW_WIDTH // 2 + self.LEFT_MARGIN
            + self.FRIEND_PIC_HEIGHT + self.GENERAL_MARGIN,
            self.GENERAL_MARGIN + (self.GENERAL_MARGIN + self.FRIEND_PIC_HEIGHT)
            * friend_i
        ]
        REQ_BUTTON_WIDTH = Constants.WINDOW_WIDTH // 2 - \
                           self.LEFT_MARGIN * 2 - self.GENERAL_MARGIN \
                           - self.FRIEND_PIC_HEIGHT
        REQ_BUTTON_HEIGHT = self.FRIEND_PIC_HEIGHT
        request_button_color = Colors.LIGHT_GRAY
        if friend in self.friends_requested:
            request_button_color = Colors.SILVER
        request_button = pygame.draw.rect(screen, request_button_color,
                                          (request_button_pos[0],
                                           request_button_pos[1],
                                           REQ_BUTTON_WIDTH,
                                           REQ_BUTTON_HEIGHT))
        if request_button.collidepoint(pygame.mouse.get_pos()):
            # if mouse hovers over button, turn color to white
            request_button_color = Colors.WHITE
            request_button = pygame.draw.rect(screen, request_button_color,
                                              (request_button_pos[0],
                                               request_button_pos[1],
                                               REQ_BUTTON_WIDTH,
                                               REQ_BUTTON_HEIGHT))

        # if click on button, remove or add ally
        if event is not None \
                and event.type == pygame.MOUSEBUTTONUP \
                and request_button.collidepoint(pygame.mouse.get_pos()):
            if friend in self.friends_requested:
                self.friends_requested.remove(friend)
            else:
                self.friends_requested.add(friend)

        # make Request Support text
        req_support_label_color = Colors.BLACK
        if friend in self.friends_requested:
            req_support_label_color = Colors.BLUE
        req_support_label = Constants.FONTS["HEADING_1_FONT"].render(
            "Request Support", True, req_support_label_color)
        req_support_label_pos = [
            request_button_pos[0] + REQ_BUTTON_WIDTH // 2
            - req_support_label.get_width() // 2,
            request_button_pos[1] + REQ_BUTTON_HEIGHT // 2
            - req_support_label.get_height() // 2,
            ]
        screen.blit(req_support_label, tuple(req_support_label_pos))

    def update_gui(self, screen, event=None):
        self.draw_background(screen)

        for button in self.buttons:
            # if click on Apply button, return all friends requested and
            # close window
            button.update_button(screen, event)
            if button.btn_type == "APPLY" and button.is_enabled():
                return self.friends_requested

        for friend_i, friend in enumerate(self.available_friends):
            # draw friends pictures
            self.draw_friends_pictures(screen, friend_i, friend)

            # draw boxes for Request Support button
            self.draw_support_buttons(screen, friend_i, friend, event)

        return None

    def draw_apply_button(self):
        APPLY_BUTTON_DIM = [
            150, 40
        ]
        APPLY_BUTTON_TOP_LEFT = [
            Constants.WINDOW_WIDTH * 3 / 4 - APPLY_BUTTON_DIM[0] / 2,
            Constants.WINDOW_HEIGHT * 0.9
        ]
        apply_button = Button("Apply", Constants.FONTS["HEADING_1_FONT"],
                              APPLY_BUTTON_DIM, APPLY_BUTTON_TOP_LEFT, "APPLY")
        self.buttons.append(apply_button)

    def reset_friends(self):
        FRIEND_NAMES = ["Aman", "Bo", "Charlie",
                        "AJ", "Jackson", "Sam",
                        "Jonathan", "Patrick", "John",
                        "Subbarao"]
        friend_limit = random.randint(4, 10)
        self.available_friends = FRIEND_NAMES[:friend_limit]
        self.friends_requested.clear()

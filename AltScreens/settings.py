from ConstantVars import Constants, Colors
from Utilities.button import Button, ScrollColorButton
import pygame


class Settings:
    def __init__(self, current_bullet_color):
        self.buttons = {}
        self.draw_apply_button()
        self.bullet_color = current_bullet_color
        self.GENERAL_MARGIN = 20
        self.BUTTON_X_POS = 100
        self.BUTTON_HEIGHT = 50
        self.settings = {
            "bullet_color": self.bullet_color
        }

        self.colors_options = dict()
        self.draw_colors_options()
        self.draw_apply_button()

    def draw_colors_options(self):
        # draw Settings label
        settings_label = Constants.FONTS["HEADING_1_FONT"] \
            .render("Settings", True, Colors.BLACK)
        settings_label_pos = [
            Constants.WINDOW_WIDTH / 4 - settings_label.get_width() / 2,
            self.GENERAL_MARGIN
        ]
        self.colors_options["settings_label"] = settings_label
        self.colors_options["settings_label_pos"] = settings_label_pos

        # draw "Colors:" label
        colors_label = Constants.FONTS["HEADING_2_FONT"] \
            .render("Bullet color: ", True, Colors.BLACK)
        colors_label_pos = [
            self.GENERAL_MARGIN,
            self.GENERAL_MARGIN * 2 + settings_label.get_height()
            + self.BUTTON_HEIGHT / 2 - colors_label.get_height() / 2
        ]
        self.colors_options["colors_label"] = colors_label
        self.colors_options["colors_label_pos"] = colors_label_pos

        # draw Colors options button
        colors_options_btn_size = [
            Constants.WINDOW_WIDTH / 2 - self.BUTTON_X_POS
            - self.GENERAL_MARGIN,
            self.BUTTON_HEIGHT
        ]
        colors_options_btn_pos = [
            self.BUTTON_X_POS,
            self.GENERAL_MARGIN * 2 + settings_label.get_height()
        ]
        colors_options_btn = ScrollColorButton(
            Colors.inverse_color_dict[self.bullet_color],
            Constants.FONTS["HEADING_2_FONT"],
            colors_options_btn_size,
            colors_options_btn_pos, self.bullet_color)
        self.colors_options["colors_options_btn"] = colors_options_btn
        self.buttons["colors_options_btn"] = colors_options_btn

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
        screen.blit(background, (0, 0))

    def draw_apply_button(self):
        APPLY_BUTTON_DIM = [
            150, 40
        ]
        APPLY_BUTTON_TOP_LEFT = [
            Constants.WINDOW_WIDTH * 1 / 4 - APPLY_BUTTON_DIM[0] / 2,
            Constants.WINDOW_HEIGHT * 0.9
        ]
        apply_button = Button("Apply", Constants.FONTS["HEADING_1_FONT"],
                              APPLY_BUTTON_DIM, APPLY_BUTTON_TOP_LEFT, "APPLY")
        self.buttons["apply_button"] = apply_button

    def update_colors_options(self, screen):
        settings_label = self.colors_options["settings_label"]
        settings_label_pos = self.colors_options["settings_label_pos"]
        screen.blit(settings_label, tuple(settings_label_pos))

        colors_label = self.colors_options["colors_label"]
        colors_label_pos = self.colors_options["colors_label_pos"]
        screen.blit(colors_label, tuple(colors_label_pos))

    def update_gui(self, screen, event=None):
        self.draw_background(screen)

        for _, button in self.buttons.items():
            button.update_button(screen, event)
            if button.btn_type == "APPLY" and button.is_enabled():
                self.settings["bullet_color"] = \
                    self.buttons["colors_options_btn"]\
                        .bg_color_options["current"]
                return self.settings

        self.update_colors_options(screen)
        return None

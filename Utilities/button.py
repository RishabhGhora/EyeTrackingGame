from ConstantVars import Colors
import pygame


class Button:
    def __init__(self, message: str, font: pygame.font, dimension: list,
                 top_left: list, btn_type: str = "Generic", onClick=None,
                 **kwargs):
        self.message = message
        self.font = font
        self.width = dimension[0]
        self.height = dimension[1]
        self.btn_type = btn_type
        self.kwargs = kwargs

        self.top_left = top_left
        self.bg_color_options = {
            "current": Colors.LIGHT_GRAY,
            "disabled": Colors.LIGHT_GRAY,
            "constant": Colors.DARK_GRAY,
            "enabled": Colors.SILVER,
            "hovered": Colors.WHITE
        }
        self.bg_color = self.bg_color_options["disabled"]

        self.text_color_options = {
            "disabled": Colors.BLACK,
            "enabled": Colors.BLUE
        }
        self.text_color = self.text_color_options["disabled"]
        self.enabled = False

        self.onClick = onClick

        self.hover_enabled = True
        self.binary_status_enabled = True
        if btn_type == "Constant":
            self.update_bg_color(self.bg_color_options["constant"])
            self.binary_status_enabled = False
            self.hover_enabled = False
        elif btn_type == "Non-binary-status":
            self.binary_status_enabled = False

    def update_button(self, screen, event: pygame.event = None):
        # draw button box
        button_rect = pygame.Rect((self.top_left[0], self.top_left[1],
                                   self.width, self.height))
        mouse_pos = pygame.mouse.get_pos()
        if self.hover_enabled:
            if button_rect.collidepoint(mouse_pos):
                self.hover_button()
            else:
                self.dishover_button()

        # if click on button, change color and status
        if event is not None \
                and event.type == pygame.MOUSEBUTTONUP \
                and button_rect.collidepoint(mouse_pos):
            self.click_button()

        pygame.draw.rect(screen, self.bg_color, button_rect)

        # draw label
        label = self.font.render(self.message, True, self.text_color)
        label_pos = [
            self.top_left[0] + self.width / 2 - label.get_width() / 2,
            self.top_left[1] + self.height / 2 - label.get_height() / 2,
        ]

        screen.blit(label, tuple(label_pos))

    def click_button(self):
        if self.onClick is not None:
            if len(self.kwargs) == 0:
                self.onClick()
            else:
                self.onClick(self.kwargs)
        if self.binary_status_enabled:
            if self.enabled:
                self.disable_button()
            else:
                self.enable_button()

    def hover_button(self):
        self.bg_color = self.bg_color_options["hovered"]

    def dishover_button(self):
        # unhover or dis-hover over button
        self.bg_color = self.bg_color_options["current"]

    def enable_button(self):
        self.enabled = True
        self.update_bg_color(self.bg_color_options["enabled"])
        self.text_color = self.text_color_options["enabled"]

    def disable_button(self):
        self.enabled = False
        self.update_bg_color(self.bg_color_options["disabled"])
        self.text_color = self.text_color_options["disabled"]

    def update_position(self, top_left):
        self.top_left = top_left

    def is_enabled(self):
        return self.enabled

    def update_bg_color(self, color):
        self.bg_color = color
        self.bg_color_options["current"] = color

    def update_text(self, message):
        self.message = message


class ScrollColorButton(Button):
    def __init__(self, message: str, font: pygame.font, dimension: list,
                 top_left: list, current_color):
        super().__init__(message, font, dimension, top_left, "ScrollColor")

        self.color_scroll_options = [Colors.BLUE, Colors.WHITE, Colors.RED,
                                     Colors.INDIGO, Colors.GREEN, Colors.SILVER]
        self.update_bg_color(current_color)
        self.hover_enabled = False

    def click_button(self):
        current_color_index = self.color_scroll_options.index(
            self.bg_color_options["current"])
        new_color_index = (current_color_index + 1) \
                          % len(self.color_scroll_options)
        new_color = self.color_scroll_options[new_color_index]
        self.update_bg_color(new_color)
        self.update_text(Colors.inverse_color_dict[new_color])



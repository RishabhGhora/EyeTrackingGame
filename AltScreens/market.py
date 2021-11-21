import random
from ConstantVars import Constants, Colors
import pygame
from Utilities.button import Button
from main_objects.spaceship import Spaceship


class Market:
    def __init__(self, spaceship: Spaceship = None, current_planet: str = None):
        self.spaceship = spaceship
        current_inventory = {}
        initial_cash = 0
        if spaceship is not None:
            current_inventory = spaceship.current_inventory
            initial_cash = spaceship.wallet

        self.close_market = False

        possible_planet_goods = {
            "Diamond": 1000,
            "Gold": 100,
            "Silver": 80,

            "Gallium": 70,
            "Silicone": 60,
            "Metal": 50,

            "Oil": 40,
            "Ore": 30,
            "Glass": 20,
            "Wood": 10,
        }
        possible_planets = Constants.POSSIBLE_PLANETS
        self.possible_ship_upgrades = {
            "Shield": 200,
            "Bullet Power": 500
        }

        self.current_planet = current_planet
        self.planet_goods = dict()
        self.buttons = dict()
        self.items_to_draw = dict()
        self.current_inventory = current_inventory
        self.initial_cash = initial_cash
        self.change_in_cash = 0
        self.order_cart = dict()

        self.sizes = {
            "GENERAL_MARGIN": 20,
            "INTERNAL_MARGIN": 10,
            "BUTTON_HEIGHT": 40,
            "UNIT_PRICE_WIDTH": 80,
            "ITEM_COUNT_WIDTH": 80,
            "BUY_SELL_WIDTH": 80,
            "UNIT_PRICE_X_POS": 130,
            "MARKET_LABEL_HEIGHT": -1,
            "SHIP_MARKET_X_POS": Constants.WINDOW_WIDTH / 2
        }
        self.sizes["SHIP_MARKET_UNIT_PRICE_X"] = \
            self.sizes.get("SHIP_MARKET_X_POS", 0) \
            + self.sizes["UNIT_PRICE_X_POS"] \
            - self.sizes["GENERAL_MARGIN"]

        self.generate_planet_market(possible_planets, possible_planet_goods)
        self.draw_market()
        self.draw_apply_cancel_button()

    def generate_planet_market(self, possible_planets: list,
                               possible_items: dict):
        if self.current_planet is None:
            self.current_planet = random.choice(possible_planets)

        # picks a random number of items to be available at the planet
        current_planet_items = random.sample(possible_items.keys(),
                                             random.randint(3, 10))
        for item in current_planet_items:
            self.planet_goods[item] = int(possible_items[item] *
                                          random.randint(1, 10))

    def draw_background(self, screen):
        # citation for translucent: https://stackoverflow.com/questions/
        # 6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
        translucent_surface = pygame.Surface((Constants.WINDOW_WIDTH,
                                              Constants.WINDOW_HEIGHT))
        translucent_surface.set_alpha(int(255 * 0.75))  # alpha level
        translucent_surface.fill(Colors.WHITE)  # this fills the entire surface
        screen.blit(translucent_surface, (0, 0))

    def draw_apply_cancel_button(self):
        APPLY_CANCEL_BUTTON_DIM = [
            150, 40
        ]

        APPLY_BUTTON_TOP_LEFT = [
            Constants.WINDOW_WIDTH / 2
            - APPLY_CANCEL_BUTTON_DIM[0]
            - self.sizes["INTERNAL_MARGIN"],
            Constants.WINDOW_HEIGHT * 0.9
        ]
        apply_button = Button("Apply", Constants.FONTS["HEADING_1_FONT"],
                              APPLY_CANCEL_BUTTON_DIM, APPLY_BUTTON_TOP_LEFT,
                              "APPLY", self.apply_order_cart)
        self.buttons["apply_button"] = apply_button

        CANCEL_BUTTON_TOP_LEFT = [
            Constants.WINDOW_WIDTH / 2 + self.sizes["INTERNAL_MARGIN"],
            Constants.WINDOW_HEIGHT * 0.9
        ]
        cancel_button = Button("Cancel", Constants.FONTS["HEADING_1_FONT"],
                               APPLY_CANCEL_BUTTON_DIM, CANCEL_BUTTON_TOP_LEFT,
                               "CANCEL", self.exit_market)
        self.buttons["cancel_button"] = cancel_button

    def update_headers(self, screen, offset: list = None):
        if offset is None:
            offset = [0, 0]
        header_items = self.items_to_draw["headers"]

        item_name_label = header_items["item_name_label"]
        screen.blit(
            item_name_label[0],
            [p + q for p, q in zip(item_name_label[1], offset)]
        )

        unit_price_label = header_items["unit_price_label"]
        screen.blit(
            unit_price_label[0],
            [p + q for p, q in zip(unit_price_label[1], offset)]
        )

        current_item_count_label = header_items["current_item_count_label"]
        screen.blit(
            current_item_count_label[0],
            [p + q for p, q in zip(current_item_count_label[1], offset)]
        )

    def update_gui(self, screen, event=None):
        self.draw_background(screen)

        market_label = self.items_to_draw["market_label"]
        screen.blit(market_label[0], market_label[1])

        # update planet market items
        self.update_headers(screen, [0, 0])
        self.update_market(screen, self.planet_goods, event)

        # update main_objects market items
        self.update_headers(
            screen,
            [self.sizes["SHIP_MARKET_X_POS"] - self.sizes["GENERAL_MARGIN"], 0]
        )
        self.update_market(screen, self.possible_ship_upgrades, event)
        self.update_cash_change(screen)

        self.buttons["apply_button"].update_button(screen, event)
        self.buttons["cancel_button"].update_button(screen, event)

        if self.close_market:
            return 1
        else:
            return None

    def draw_headers(self, header_y_pos: int) -> int:
        header_items = {}
        self.items_to_draw["headers"] = header_items

        item_name_label = Constants.FONTS["HEADING_2_FONT"] \
            .render("Item", True, Colors.BLACK)
        item_name_label_pos = [
            self.sizes["GENERAL_MARGIN"],
            header_y_pos
        ]
        header_items["item_name_label"] = [item_name_label, item_name_label_pos]

        unit_price_label = Constants.FONTS["HEADING_2_FONT"] \
            .render("Unit Price", True, Colors.BLACK)
        unit_price_label_pos = [
            self.sizes["UNIT_PRICE_X_POS"]
            + self.sizes["ITEM_COUNT_WIDTH"] / 2
            - unit_price_label.get_width() / 2,
            header_y_pos
        ]
        header_items["unit_price_label"] = [unit_price_label,
                                            unit_price_label_pos]

        current_item_count_label = Constants.FONTS["HEADING_2_FONT"] \
            .render("Inventory", True, Colors.BLACK)
        current_item_count_label_pos = [
            self.sizes["UNIT_PRICE_X_POS"]
            + self.sizes["UNIT_PRICE_WIDTH"]
            + self.sizes["INTERNAL_MARGIN"]
            + self.sizes["ITEM_COUNT_WIDTH"] / 2
            - current_item_count_label.get_width() / 2,
            header_y_pos
        ]
        header_items["current_item_count_label"] = \
            [current_item_count_label, current_item_count_label_pos]

        # sell_item_label = Constants.FONTS["HEADING_2_FONT"] \
        #     .render("Sell", True, Colors.BLACK)
        # sell_item_label_pos = [
        #     self.sizes["UNIT_PRICE_X_POS"]
        #     + self.sizes["UNIT_PRICE_WIDTH"]
        #     + self.sizes["INTERNAL_MARGIN"]
        #     + self.sizes["ITEM_COUNT_WIDTH"]
        #     + self.sizes["GENERAL_MARGIN"],
        #     header_y_pos
        # ]
        # header_items["sell_item_label"] = [sell_item_label,
        # sell_item_label_pos]
        #
        # buy_item_label = Constants.FONTS["HEADING_2_FONT"] \
        #     .render("Buy", True, Colors.BLACK)
        # buy_item_label_pos = [
        #     self.sizes["UNIT_PRICE_X_POS"]
        #     + self.sizes["UNIT_PRICE_WIDTH"]
        #     + self.sizes["INTERNAL_MARGIN"]
        #     + self.sizes["ITEM_COUNT_WIDTH"]
        #     + self.sizes["GENERAL_MARGIN"]
        #     + self.sizes["BUY_SELL_WIDTH"]
        #     + self.sizes["INTERNAL_MARGIN"],
        #     header_y_pos
        # ]
        # header_items["buy_item_label"] = [buy_item_label, buy_item_label_pos]

        return item_name_label.get_height()

    def update_market(self, screen, item_dict, event=None):
        for item in item_dict.keys():
            item_label = self.items_to_draw[f"item_label_{item}"]
            screen.blit(item_label[0], item_label[1])

            this_item_buttons = self.buttons[item]
            this_item_buttons["unit_price_button"].update_button(screen, event)
            this_item_buttons["current_item_count_button"].update_button(
                screen, event)
            this_item_buttons["sell_btn"].update_button(screen, event)
            this_item_buttons["buy_btn"].update_button(screen, event)

    def draw_market(self):
        # draw Market label
        market_label = Constants.FONTS["HEADING_1_FONT"] \
            .render(f"Market of {self.current_planet}", True, Colors.BLACK)
        market_label_pos = [
            Constants.WINDOW_WIDTH / 2 - market_label.get_width() / 2,
            self.sizes["GENERAL_MARGIN"]
        ]
        self.items_to_draw["market_label"] = [market_label, market_label_pos]
        self.sizes["MARKET_LABEL_HEIGHT"] = market_label.get_height()

        header_y_pos = self.sizes["GENERAL_MARGIN"] \
                       + self.sizes["MARKET_LABEL_HEIGHT"] \
                       + self.sizes["GENERAL_MARGIN"]

        header_height = self.draw_headers(header_y_pos)

        first_button_y_pos = header_y_pos + header_height \
                             + self.sizes["INTERNAL_MARGIN"]
        button_y_variable = self.sizes["BUTTON_HEIGHT"] \
                            + self.sizes["INTERNAL_MARGIN"]

        for item_i, item in enumerate(self.planet_goods.keys()):
            button_y_pos = first_button_y_pos + button_y_variable * item_i

            this_item_buttons = dict()
            self.buttons[item] = this_item_buttons

            # draw item label
            item_label = Constants.FONTS["HEADING_2_FONT"] \
                .render(item, True, Colors.BLACK)
            item_pos = [
                self.sizes["GENERAL_MARGIN"],
                button_y_pos + self.sizes["BUTTON_HEIGHT"] / 2
                - item_label.get_height() / 2
            ]
            self.items_to_draw[f"item_label_{item}"] = [item_label, item_pos]

            # draw unit price button
            unit_price_button_pos = [
                self.sizes["UNIT_PRICE_X_POS"], button_y_pos
            ]
            unit_price_button_dim = [
                self.sizes["UNIT_PRICE_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            unit_price_button = Button(f"${self.planet_goods[item]}",
                                       Constants.FONTS["HEADING_2_FONT"],
                                       unit_price_button_dim,
                                       unit_price_button_pos, "Constant")
            this_item_buttons["unit_price_button"] = unit_price_button

            # draw current number of items in spaceship
            current_item_count_pos = [
                self.sizes["UNIT_PRICE_X_POS"]
                + self.sizes["UNIT_PRICE_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"],
                button_y_pos
            ]
            current_item_count_dim = [
                self.sizes["ITEM_COUNT_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            current_item_count_button = Button(
                f"{self.current_inventory.get(item, 0)}",
                Constants.FONTS["HEADING_2_FONT"],
                current_item_count_dim, current_item_count_pos,
                "Constant")
            this_item_buttons[
                "current_item_count_button"] = current_item_count_button

            # draw sell button
            sell_pos = [
                self.sizes["UNIT_PRICE_X_POS"]
                + self.sizes["UNIT_PRICE_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"]
                + self.sizes["ITEM_COUNT_WIDTH"]
                + self.sizes["GENERAL_MARGIN"],
                button_y_pos
            ]
            sell_dim = [
                self.sizes["BUY_SELL_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            sell_btn = Button("Sell",
                              Constants.FONTS["HEADING_2_FONT"],
                              sell_dim, sell_pos,
                              "Non-binary-status", self.sell_onClick,
                              item=item)
            this_item_buttons["sell_btn"] = sell_btn

            # draw buy button
            buy_pos = [
                self.sizes["UNIT_PRICE_X_POS"]
                + self.sizes["UNIT_PRICE_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"]
                + self.sizes["ITEM_COUNT_WIDTH"]
                + self.sizes["GENERAL_MARGIN"]
                + self.sizes["BUY_SELL_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"],
                button_y_pos
            ]
            buy_dim = [
                self.sizes["BUY_SELL_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            buy_btn = Button("Buy",
                             Constants.FONTS["HEADING_2_FONT"],
                             buy_dim, buy_pos,
                             "Non-binary-status", self.buy_onClick,
                             item=item)
            this_item_buttons["buy_btn"] = buy_btn

        self.draw_wallet()
        self.draw_ship_market(first_button_y_pos)

    def draw_ship_market(self, first_button_y_pos: int):
        button_y_variable = self.sizes["BUTTON_HEIGHT"] \
                            + self.sizes["INTERNAL_MARGIN"]

        for item_i, (item, item_price) in \
                enumerate(self.possible_ship_upgrades.items()):
            button_y_pos = first_button_y_pos + button_y_variable * item_i

            this_item_buttons = dict()
            self.buttons[item] = this_item_buttons

            # draw item label
            item_label = Constants.FONTS["HEADING_2_FONT"] \
                .render(item, True, Colors.BLACK)
            item_pos = [
                self.sizes["SHIP_MARKET_X_POS"],
                button_y_pos + self.sizes["BUTTON_HEIGHT"] / 2
                - item_label.get_height() / 2
            ]
            self.items_to_draw[f"item_label_{item}"] = [item_label, item_pos]

            # draw unit price button
            unit_price_button_pos = [
                self.sizes["SHIP_MARKET_UNIT_PRICE_X"], button_y_pos
            ]
            unit_price_button_dim = [
                self.sizes["UNIT_PRICE_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            unit_price_button = Button(f"${item_price}",
                                       Constants.FONTS["HEADING_2_FONT"],
                                       unit_price_button_dim,
                                       unit_price_button_pos, "Constant")
            this_item_buttons["unit_price_button"] = unit_price_button

            # draw current number of items in spaceship
            current_item_count_pos = [
                self.sizes["SHIP_MARKET_UNIT_PRICE_X"]
                + self.sizes["UNIT_PRICE_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"],
                button_y_pos
            ]
            current_item_count_dim = [
                self.sizes["ITEM_COUNT_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            current_item_count_button = Button(
                f"{self.current_inventory.get(item, 0)}",
                Constants.FONTS["HEADING_2_FONT"],
                current_item_count_dim, current_item_count_pos,
                "Constant")
            this_item_buttons[
                "current_item_count_button"] = current_item_count_button

            # draw sell button
            sell_pos = [
                self.sizes["SHIP_MARKET_UNIT_PRICE_X"]
                + self.sizes["UNIT_PRICE_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"]
                + self.sizes["ITEM_COUNT_WIDTH"]
                + self.sizes["GENERAL_MARGIN"],
                button_y_pos
            ]
            sell_dim = [
                self.sizes["BUY_SELL_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            sell_btn = Button("Sell",
                              Constants.FONTS["HEADING_2_FONT"],
                              sell_dim, sell_pos,
                              "Non-binary-status", self.sell_onClick,
                              item=item)
            this_item_buttons["sell_btn"] = sell_btn

            # draw buy button
            buy_pos = [
                self.sizes["SHIP_MARKET_UNIT_PRICE_X"]
                + self.sizes["UNIT_PRICE_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"]
                + self.sizes["ITEM_COUNT_WIDTH"]
                + self.sizes["GENERAL_MARGIN"]
                + self.sizes["BUY_SELL_WIDTH"]
                + self.sizes["INTERNAL_MARGIN"],
                button_y_pos
            ]
            buy_dim = [
                self.sizes["BUY_SELL_WIDTH"], self.sizes["BUTTON_HEIGHT"]
            ]
            buy_btn = Button("Buy",
                             Constants.FONTS["HEADING_2_FONT"],
                             buy_dim, buy_pos,
                             "Non-binary-status", self.buy_onClick,
                             item=item)
            this_item_buttons["buy_btn"] = buy_btn

    def draw_wallet(self):
        wallet_label = Constants.FONTS["HEADING_1_FONT"] \
            .render(f"Wallet: ${self.initial_cash}", True, Colors.BLACK)
        wallet_label_pos = [
            self.sizes["GENERAL_MARGIN"],
            0.8 * Constants.WINDOW_HEIGHT
        ]
        self.items_to_draw["wallet_label"] = [wallet_label, wallet_label_pos]

    def update_cash_change(self, screen):
        wallet_label = self.items_to_draw["wallet_label"]
        screen.blit(wallet_label[0], wallet_label[1])

        cash_change_label = None
        if self.change_in_cash > 0:
            cash_change_message = f"You gain: ${self.change_in_cash}"
            cash_change_label = Constants.FONTS["HEADING_1_FONT"] \
                .render(cash_change_message, True, Colors.GREEN)
        elif self.change_in_cash == 0:
            cash_change_message = f"Trade something!"
            cash_change_label = Constants.FONTS["HEADING_1_FONT"] \
                .render(cash_change_message, True, Colors.BLACK)
        elif self.change_in_cash < 0:
            cash_change_message = f"You are spending: ${-self.change_in_cash}"
            cash_change_label = Constants.FONTS["HEADING_1_FONT"] \
                .render(cash_change_message, True, Colors.RED)
        cash_change_label_pos = [
            self.sizes["GENERAL_MARGIN"],
            wallet_label[1][1] + wallet_label[0].get_height()
            + self.sizes["INTERNAL_MARGIN"]
        ]
        screen.blit(cash_change_label, cash_change_label_pos)

    def sell_onClick(self, kwargs: dict):
        item = kwargs.get("item")
        self.order_cart[item] = self.order_cart.get(item, 0) - 1
        if item in self.planet_goods:
            self.change_in_cash += self.planet_goods[item]
        elif item in self.possible_ship_upgrades:
            self.change_in_cash += self.possible_ship_upgrades[item]
        self.refurbish_cart_button(item)

    def buy_onClick(self, kwargs: dict):
        item = kwargs.get("item")
        self.order_cart[item] = self.order_cart.get(item, 0) + 1
        if item in self.planet_goods:
            self.change_in_cash -= self.planet_goods[item]
        elif item in self.possible_ship_upgrades:
            self.change_in_cash -= self.possible_ship_upgrades[item]
        self.refurbish_cart_button(item)

    def refurbish_cart_button(self, item):
        # update cart with current order, changing color as necessary
        current_item_count_button = \
            self.buttons[item]["current_item_count_button"]
        current_item_count = \
            self.current_inventory.get(item, 0) + self.order_cart.get(item, 0)
        if current_item_count > self.current_inventory.get(item, 0):
            current_item_count_button.update_bg_color(Colors.GREEN)
        elif current_item_count == self.current_inventory.get(item, 0):
            current_item_count_button.update_bg_color(Colors.DARK_GRAY)
        elif current_item_count < self.current_inventory.get(item, 0):
            current_item_count_button.update_bg_color(Colors.RED)
        current_item_count_button.update_text(f"{current_item_count}")

    def apply_order_cart(self):
        self.spaceship.update_inventory(self.order_cart)
        self.spaceship.update_wallet(self.change_in_cash)
        self.exit_market()

    def exit_market(self):
        self.close_market = True


if __name__ == "__main__":
    pygame.init()
    Constants.initiate_constants(pygame)

    # Set up the drawing window
    ss_screen = pygame.display.set_mode([Constants.WINDOW_WIDTH,
                                         Constants.WINDOW_HEIGHT])

    market = Market()

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for ss_event in pygame.event.get():
            # Fill the background with white
            ss_screen.fill(Colors.BLACK)

            if ss_event.type == pygame.QUIT:
                running = False
            market.update_gui(ss_screen, ss_event)
        ss_screen.fill(Colors.BLACK)
        market.update_gui(ss_screen, None)

        # Draw a solid blue circle in the center
        # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Flip the display
        pygame.display.update()

    # Done! Time to quit.
    pygame.quit()

    # Market({}, 0)

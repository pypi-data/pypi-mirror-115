import logging
import math
from typing import Type

import pygame.gfxdraw
import pygame.surface

from trosnoth.gui.common import TextImage
from trosnoth.gui.framework.framework import Element, CompoundElement
from trosnoth.model.upgrades import Categories, ShopItem, gun_types, GunType
from trosnoth.utils.math import distance

log = logging.getLogger(__name__)


VERTICES_IN_FULL_CIRCLE = 36

CENTRAL_AREA = object()


class RadialUpgradeMenu(CompoundElement):
    def __init__(self, app, player, set_upgrade):
        super().__init__(app)
        self.player = player
        self.set_upgrade = set_upgrade
        self.child = None

    def set_player(self, player):
        self.player = player
        if self.child:
            if player is None:
                self.set_child(None)
            else:
                self.child.set_player(player)

    def start(self):
        pass

    def stop(self):
        if self.child:
            self.child.stop()

    def set_child(self, child):
        if self.child:
            self.child.stop()
        self.child = child
        self.elements = [child] if child else []
        if self.child:
            self.child.start()

    def toggle(self):
        if self.child or self.player is None:
            self.set_child(None)
        else:
            self.set_child(CategoryMenu(self.app, self.player, self.set_child, self.set_upgrade))


class RadialMenu(Element):
    outline_offset = 0.05
    outline_colour = (125, 125, 125, 225)
    background_colour = (170, 170, 170, 225)
    disabled_colour = (170, 170, 170, 225)
    hover_colour = (255, 255, 100, 225)

    degrees_in_gap = 5

    def __init__(self, app, player, set_menu):
        super().__init__(app)
        self.player = player
        self.set_menu = set_menu
        self.surface = None

        self.screen_centre = (0, 0)
        self.display_radius_max = 0
        self.display_radius_min = 0
        self.current_selection = None
        self.options = []
        self.polygon_coordinates = {}
        self.image_coordinates = {}
        self.degrees_per_option = 0

        self.item_label = ItemLabel(self.app, self.app.fonts.gameMenuFont)

    def start(self):
        self.app.screenManager.onResize.addListener(self.screen_resized)
        self.screen_resized()

    def stop(self):
        self.app.screenManager.onResize.removeListener(self.screen_resized)

    def set_player(self, player):
        self.player = player

    def screen_resized(self):
        self.surface = pygame.surface.Surface(self.app.screenManager.size, pygame.SRCALPHA)
        self.screen_centre = self.surface.get_rect().center
        self.display_radius_max = min(self.app.screenManager.size) / 4
        self.display_radius_min = self.display_radius_max * 0.5

        self.polygon_coordinates.clear()
        self.image_coordinates.clear()

        num_options = len(self.options)
        self.degrees_per_option = 360 / num_options
        vertex_count = VERTICES_IN_FULL_CIRCLE // num_options
        degrees_offset = {0: self.degrees_in_gap * 0.5, vertex_count: -self.degrees_in_gap * 0.5}

        for option_index, option in enumerate(self.options):
            polygon = []
            self.polygon_coordinates[option] = polygon
            arc_coordinates = []
            for vertex_index in range(vertex_count + 1):
                offset = degrees_offset.get(vertex_index, 0)

                arc_coordinates.append(self.get_position(
                    option_index * self.degrees_per_option + offset
                    + vertex_index * self.degrees_per_option / vertex_count, 1))

            for vertex_coordinate in arc_coordinates:
                polygon.append((
                    vertex_coordinate[0] * self.display_radius_max + self.screen_centre[0],
                    vertex_coordinate[1] * self.display_radius_max + self.screen_centre[1]))

            for vertex_coordinate in reversed(arc_coordinates):
                polygon.append((
                    vertex_coordinate[0] * self.display_radius_min + self.screen_centre[0],
                    vertex_coordinate[1] * self.display_radius_min + self.screen_centre[1]))

            image_position = self.get_position(
                (option_index + 0.5) * self.degrees_per_option, self.display_radius_max * 0.75)
            image_position = (
                image_position[0] + self.screen_centre[0], image_position[1] + self.screen_centre[1])
            self.image_coordinates[option] = image_position
        self.current_selection = self.selection_from_position(pygame.mouse.get_pos())

    def get_position(self, angle, magnitude):
        radians = math.radians(angle)
        x = magnitude * math.sin(radians)
        y = -magnitude * math.cos(radians)
        return (x, y)

    def processEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.current_selection = self.selection_from_position(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_selection == CENTRAL_AREA:
                self.close_menu()
                return None

            if self.current_selection is not None:
                option = self.current_selection
                if self.is_option_enabled(option):
                    self.click(option)
                return None
        return event

    def selection_from_position(self, given_pos):
        magnitude = distance(given_pos, self.screen_centre)
        if self.display_radius_max > magnitude > self.display_radius_min:
            index = math.floor(
                math.degrees(math.atan2(
                    given_pos[0] - self.screen_centre[0],
                    -given_pos[1] + self.screen_centre[1])) % 360 / self.degrees_per_option)
            return self.options[index]
        elif magnitude < self.display_radius_min:
            return CENTRAL_AREA
        return None

    def draw(self, screen):
        # Draw the background
        self.surface.fill((0, 0, 0, 0))
        draw_circle(self.surface, self.outline_colour, self.screen_centre, math.floor(
            self.display_radius_max * (1 + self.outline_offset)))
        draw_circle(self.surface, (0, 0, 0, 0), self.screen_centre, math.floor(
            self.display_radius_min * (1 - self.outline_offset)))

        # Draw the ‘X’ in the centre
        background_colour = self.background_colour
        if self.current_selection == CENTRAL_AREA:
            background_colour = self.hover_colour
        central_radius = int(self.display_radius_min // 3)
        draw_circle(
            self.surface, self.outline_colour, self.screen_centre, central_radius + 3)
        draw_circle(
            self.surface, background_colour, self.screen_centre, central_radius)
        central_rect = pygame.Rect(
            0, 0, int(self.display_radius_min // 4), int(self.display_radius_min // 4))
        central_rect.center = self.screen_centre
        pygame.draw.line(
            self.surface, (96, 96, 96), central_rect.topleft, central_rect.bottomright, 5)
        pygame.draw.line(
            self.surface, (96, 96, 96), central_rect.topright, central_rect.bottomleft, 5)

        # Draw the segments around the circle
        for option in self.options:
            if self.is_option_enabled(option):
                background_colour = self.background_colour
                if self.current_selection == option:
                    background_colour = self.hover_colour
                draw_polygon(self.surface, background_colour, self.polygon_coordinates[option])
            self.draw_icon(option, self.surface, self.image_coordinates[option])

        screen.blit(self.surface, (0, 0))

        # Add mouse hover text
        if self.current_selection is not None and self.current_selection != CENTRAL_AREA:
            self.item_label.set_text(self.get_display_name(self.current_selection))
            x, y = pygame.mouse.get_pos()
            self.item_label.blit_to(screen, (x, y + 30))

    def close_menu(self):
        self.set_menu(None)

    def is_option_enabled(self, option):
        raise NotImplementedError()

    def get_display_name(self, option):
        raise NotImplementedError()

    def draw_icon(self, option, surface, pos):
        raise NotImplementedError()

    def click(self, option):
        raise NotImplementedError()


class CategoryMenu(RadialMenu):
    def __init__(self, app, player, set_menu, set_upgrade):
        super().__init__(app, player, set_menu)
        self.set_upgrade = set_upgrade
        self.options = list(Categories)

    def is_option_enabled(self, option):
        if option == Categories.WEAPON and not self.player.aggression:
            return False
        return True

    def get_display_name(self, option):
        return option.display_name

    def draw_icon(self, option, surface, pos):
        enabled = self.is_option_enabled(option)
        if enabled:
            image = self.app.theme.sprites.category_image(option.icon_filename)
        else:
            image = self.app.theme.sprites.disabled_category_image(option.icon_filename)

        rect = image.get_rect()
        rect.center = pos
        surface.blit(image, rect)

    def click(self, option):
        if option == Categories.WEAPON:
            self.set_menu(GunMenu(self.app, self.player, self.set_menu))
        else:
            self.set_menu(ItemMenu(self.app, self.player, option, self.set_menu, self.set_upgrade))


class TextCache:
    def __init__(self, app):
        self.app = app
        self.cache = {}

    def render(self, text, colour):
        key = (text, colour)
        if key not in self.cache:
            self.cache[key] = TextImage(
                text,
                font=self.app.screenManager.fonts.cost_font,
                colour=colour,
            )

        return self.cache[key].getImage(self.app)


class ItemMenu(RadialMenu):
    def __init__(self, app, player, category, set_menu, set_upgrade):
        super().__init__(app, player, set_menu)
        self.set_upgrade = set_upgrade
        self.options = category.upgrades
        self.text_cache = TextCache(app)

    def is_option_enabled(self, option: ShopItem):
        return option.get_required_coins(self.player) is not None

    def get_display_name(self, option: ShopItem):
        return option.name

    def draw_icon(self, option: ShopItem, surface, pos):
        enabled = self.is_option_enabled(option)
        image = option.get_icon(self.app.theme.sprites, enabled)
        rect = image.get_rect()
        rect.center = pos
        surface.blit(image, rect)

        if enabled:
            colours = self.app.theme.colours
            required_coins = option.get_required_coins(self.player)
            affordable = self.player.coins >= required_coins
            colour = colours.cost_affordable if affordable else colours.cost_prohibitive
            text = self.text_cache.render(f'${required_coins}', colour)
            text_rect = text.get_rect()
            text_rect.midtop = rect.midbottom
            surface.blit(text, text_rect)

    def click(self, option: ShopItem):
        self.set_upgrade(option)
        self.close_menu()


class GunMenu(RadialMenu):
    def __init__(self, app, player, set_menu):
        super().__init__(app, player, set_menu)
        self.options = [g for g in gun_types if g.max_ammo > 0]
        self.text_cache = TextCache(app)

    def is_option_enabled(self, option: Type[GunType]):
        if not self.player.aggression:
            return False

        required_coins = option.get_required_coins(self.player)
        if required_coins is None or self.player.coins < required_coins:
            return False

        return True

    def get_display_name(self, option: Type[GunType]):
        return option.name

    def draw_icon(self, option: Type[GunType], surface, pos):
        enabled = self.is_option_enabled(option)
        image = option.get_icon(self.app.theme.sprites, enabled)
        rect = image.get_rect()
        rect.center = pos
        surface.blit(image, rect)
        next_point = rect.midbottom

        colours = self.app.theme.colours
        gun = self.player.guns.get(option)
        if gun.ammo > 0:
            ammo_rect = pygame.Rect(0, 0, rect.width, 5)
            ammo_rect.midtop = next_point
            next_point = ammo_rect.midbottom
            pygame.draw.rect(surface, colours.gauge_ammo, ammo_rect, 1)
            ammo_rect.width = round(rect.width * gun.ammo / option.max_ammo)
            pygame.draw.rect(surface, colours.gauge_ammo, ammo_rect)

        required_coins = option.get_required_coins(self.player)
        cost_string = f'${required_coins}'
        if required_coins is None:
            colour = colours.cost_unavailable
            cost_string = 'MAX'
        elif self.player.coins >= required_coins:
            colour = colours.cost_affordable
        else:
            colour = colours.cost_prohibitive

        text = self.text_cache.render(cost_string, colour)
        text_rect = text.get_rect()
        text_rect.midtop = next_point
        surface.blit(text, text_rect)

    def click(self, option: GunType):
        self.player.guns.get(option).please_buy_ammo()


def draw_circle(surface, colour, centre, radius):
    pygame.gfxdraw.aacircle(surface, *centre, radius, colour)
    pygame.gfxdraw.filled_circle(surface, *centre, radius, colour)


def draw_polygon(surface, colour, points):
    pygame.gfxdraw.aapolygon(surface, points, colour)
    pygame.gfxdraw.filled_polygon(surface, points, colour)


class ItemLabel:
    def __init__(self, app, font, colour=(200, 200, 200), shadow=(50, 50, 50)):
        self.app = app
        self.font = font
        self.colour = colour
        self.shadow = shadow
        self.text = None
        self.main_surface = None
        self.shadow_surface = None

    def set_text(self, text):
        if text == self.text:
            return
        self.text = text
        self.main_surface = self.font.render(self.app, text, True, self.colour)
        self.shadow_surface = self.font.render(self.app, text, True, self.shadow)

    def blit_to(self, screen, position):
        r = self.main_surface.get_rect()
        r.center = position
        x, y = r.topleft
        screen.blit(self.shadow_surface, (x + 2, y + 2))
        screen.blit(self.main_surface, r)

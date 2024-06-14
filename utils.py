from pathlib import Path

import numpy as np
import pygame as pg

COLOR_LIGHT_BLUE = (170, 255, 245)
COLOR_BROWN = (208, 130, 40)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (42, 101, 128)
COLOR_RED = (198, 103, 53)

COLORS_DICT = {'Sea': COLOR_LIGHT_BLUE,
               'Block': COLOR_BROWN,
               'Island': COLOR_BLACK,
               'Player': [COLOR_BLUE, COLOR_RED],
               }

IMAGES_PATH = Path(__file__).parent.resolve() / 'images'

IMAGES_DICT = {'Block': IMAGES_PATH / 'block.png',
               'Island': IMAGES_PATH / 'neutral_island.png',
               'Player': [{'Ship': IMAGES_PATH / 'blue_ship.png', 'Island': IMAGES_PATH / 'blue_island.png'},
                          {'Ship': IMAGES_PATH / 'red_ship.png', 'Island': IMAGES_PATH / 'red_island.png'}],
               }

BLOCK_ASPECT_RATIO = 1.45  # multiply width by this
ISLAND_ASPECT_RATIO = 1.55  # multiply width by this

SIZE_DICT = {'Block': (BLOCK_ASPECT_RATIO * 50, 50),
             'Island': (ISLAND_ASPECT_RATIO * 70, 70),
             'Player': (70, 70),
             }

SCREEN_WIDTH = 0.8 * 1280
SCREEN_HEIGHT = 0.8 * 720


class InvalidMoveError(Exception):
    pass


def get_class_from_module_name(folder_name: str, module_name: str):
    my_module = __import__(f'{folder_name}.{module_name}')
    my_class = getattr(my_module, module_name)
    class_name = get_class_name_from_module_name(module_name)
    return getattr(my_class, class_name)


def get_class_name_from_module_name(module_name: str) -> str:
    """
    replace every underscore with next letter capitalized"""
    class_name = ''
    capitalized_letter = True
    for character in module_name:
        if character != '_':
            class_name += character.upper() if capitalized_letter else character
            if capitalized_letter:
                capitalized_letter = not capitalized_letter
        else:
            class_name += ''
            capitalized_letter = True
    return class_name


def verify_location(location: np.ndarray, board_size: int) -> np.ndarray:
    # Keep location on the board
    if location[0] < 0:
        location[0] = 0
    if location[0] > board_size - 1:
        location[0] = board_size - 1
    if location[1] < 0:
        location[1] = 0
    if location[1] > board_size - 1:
        location[1] = board_size - 1
    return location


class FrontEndObj(pg.sprite.Sprite):
    def __init__(self, name, location, **kwargs):
        super(FrontEndObj, self).__init__()
        self.name = name
        # self.surf = pg.Surface(SIZE_DICT[name])

        # For Ship
        if 'player_id' in kwargs.keys():
            player_id = kwargs['player_id']
            # self.surf.fill(COLORS_DICT[name][player_id])
            self.image = pg.image.load(IMAGES_DICT[name][player_id]['Ship'])

        # For Block and Island
        else:
            # self.surf.fill(COLORS_DICT[name])
            self.image = pg.image.load(IMAGES_DICT[name])

        self.image = pg.transform.scale(self.image, SIZE_DICT[name])
        # self.rect = self.surf.get_rect()
        self.location = location
        self.frontend_location = 0

    def draw_sprite(self, location, board_size, screen):
        self.frontend_location = self.get_frontend_location(location, board_size)
        # self.rect = self.surf.get_rect(center=frontend_location)
        # screen.blit(self.surf, self.rect)
        screen.blit(self.image, self.frontend_location)

    # def verify_frontend_location(self):
    #     # Keep sprite on the screen
    #     if self.rect.left < 0:
    #         self.rect.left = 0
    #     if self.rect.right > SCREEN_WIDTH:
    #         self.rect.right = SCREEN_WIDTH
    #     if self.rect.top <= 0:
    #         self.rect.top = 0
    #     if self.rect.bottom >= SCREEN_HEIGHT:
    #         self.rect.bottom = SCREEN_HEIGHT

    @staticmethod
    def get_frontend_location(location, board_size):
        width_scale_factor = SCREEN_WIDTH / board_size
        height_scale_factor = SCREEN_HEIGHT / board_size
        frontend_location = (location[0] * width_scale_factor,
                             location[1] * height_scale_factor)
        return frontend_location

    def change_to_player_color(self, player_id):
        """ Change to player color once captured by a player"""
        # player_color = COLORS_DICT['Player'][player_id]
        # self.surf.fill(player_color)
        self.image = pg.image.load(IMAGES_DICT['Player'][player_id]['Island'])
        self.image = pg.transform.scale(self.image, SIZE_DICT['Island'])

    def change_to_neutral_color(self):
        """ Change to player color once captured by a player"""
        # player_color = COLORS_DICT['Island']
        # self.surf.fill(player_color)
        self.image = pg.image.load(IMAGES_DICT['Island'])
        self.image = pg.transform.scale(self.image, SIZE_DICT['Island'])

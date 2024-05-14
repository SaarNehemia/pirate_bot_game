from pathlib import Path

import numpy as np
import pygame as pg

COLOR_LIGHT_BLUE = (170, 255, 245)
COLOR_BLACK = (0, 0, 0)
COLOR_BROWN = (208, 130, 40)
COLOR_BLUE = (0, 0, 200)
COLOR_RED = (200, 0, 0)

COLORS_DICT = {'Sea': COLOR_LIGHT_BLUE,
               'Block': COLOR_BLACK,
               'Island': COLOR_BROWN,
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
             'Player': (80, 80),
             }

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def split_list_according_to_indices_list(my_list: list, indices_list: list,
                                         return_in_indices_list: bool):
    """
    l1 is a list of all elements in my_list whose indices aren't in indices_list.
    l1 is a list of all elements in my_list whose indices are in indices_list.
    based on: https://stackoverflow.com/questions/45649106/get-list-elements-that-are-not-in-index-list
    """
    indices = set(indices_list)  # convert to set for fast lookups
    l1, l2 = [], []
    l_append = (l1.append, l2.append)
    for idx, element in enumerate(my_list):
        l_append[idx in indices](element)
    if return_in_indices_list:
        return l2
    else:
        return l1


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

    def draw_sprite(self, location, board_size, screen):
        frontend_location = self.get_frontend_location(location, board_size)
        # self.rect = self.surf.get_rect(center=frontend_location)
        # screen.blit(self.surf, self.rect)
        screen.blit(self.image, frontend_location)

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

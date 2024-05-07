import random

import numpy as np

import utils
from classes.island import Island
from classes.player import Player
from classes.ship import Ship


def extract_board_params(board_params):
    return board_params['board_size'], \
        board_params['blocks'], \
        board_params['islands'], \
        board_params['players_base_islands_indices'], \
        board_params['players_ship_speed'], \
        board_params['players_num_ships']


class API():
    def __init__(self, board_params, player_names):
        # init players
        self.player_names = player_names
        random.shuffle(self.player_names)
        self.players = []
        for player_id, player_name in enumerate(player_names):
            self.players.append(Player(player_id, player_name))

        self.board_size, self.blocks, self.islands, self.players_base_islands_indices, \
            self.players_ship_speed, self.players_num_ships = \
            extract_board_params(board_params)
        self.board = []  # Backend

        self.num_turn = 0
        self.direction_dict = {'N': (0, -1),
                               'S': (0, 1),
                               'W': (-1, 0),
                               'E': (1, 0)}

    def get_my_player_obj(self, player_name: str):
        return self.players[self.player_names.index(player_name)]

    def move_ship(self, ship: Ship, direction: str):
        # Update board
        current_obj = self.board[ship.location[0]][ship.location[1]]
        if isinstance(current_obj, Ship):
            self.board[ship.location[0]][ship.location[1]] = 'Sea'

        new_location = np.array(ship.location) + ship.ship_speed * np.array(self.direction_dict[direction])
        # TODO - check for blocks or islands
        ship.update_location(new_location, self.board_size)
        self.board[ship.location[0]][ship.location[1]] = ship

    def is_block_in_location(self):  # TODO
        pass

    def is_island_in_location(self):  # TODO
        pass

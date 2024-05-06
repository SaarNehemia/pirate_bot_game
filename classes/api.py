import random

import numpy as np

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
        self.board = []

        self.direction_dict = {'N': (0, 1),
                               'S': (0, -1),
                               'W': (-1, 0),
                               'E': (1, 0)}

    def get_my_player_obj(self, player_name: str):
        return self.players[self.player_names.index(player_name)]

    def move_ship(self, ship: Ship, direction: str):
        # Update ship location
        self.board[ship.location[0]][ship.location[1]] = 'Sea'
        ship.location = np.array(ship.location) + np.array(ship.ship_speed * self.direction_dict[direction])
        self.board[ship.location[0]][ship.location[1]] = ship
        # TODO - Handle getting off screen bounds, add ships

        # Move ship in frontend
        ship.frontend_obj.move_sprite(num_steps=ship.ship_speed,
                                      step=self.direction_dict[direction])


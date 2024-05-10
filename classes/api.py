import random

import numpy as np

import utils
from classes.block import Block
from classes.island import Island
from classes.player import Player
from classes.ship import Ship


def extract_board_params(board_params):
    return board_params['board_size'], \
        board_params['blocks'], \
        board_params['islands'], \
        board_params['players_base_islands_indices'], \
        board_params['players_ship_speed'], \
        board_params['players_num_ships'],\
        board_params['victory_criterion']


class API():
    def __init__(self, board_params, player_names):
        # init players
        self.player_names = player_names
        random.shuffle(self.player_names)
        self.players = []
        for player_id, player_name in enumerate(player_names):
            self.players.append(Player(player_id, player_name))

        # Init board
        self.board_size, self.blocks, self.islands, self.players_base_islands_indices, \
            self.players_ship_speed, self.players_num_ships, self.victory_criterion = \
            extract_board_params(board_params)
        self.board = []  # Backend

        # Init
        self.num_turn = 0
        self.direction_dict = {'N': (0, -1),
                               'S': (0, 1),
                               'W': (-1, 0),
                               'E': (1, 0)}

    def get_my_player_obj(self):
        return self.players[self.get_my_player_id()]

    def get_my_player_id(self):
        return self.num_turn % len(self.players)

    def get_num_owned_islands(self, player_id):
        count = 0
        for island in self.islands:
            if island.own_player_id == player_id:
                count += 1
        return count

    def move_ship(self, ship: Ship, direction: str):
        # Update board
        self.update_tile_ship_left(ship)
        new_location = self.check_route(ship=ship, direction=direction)
        ship.update_location(new_location, self.board_size)
        self.update_tile_ship_entered(ship)

    def move_ship_towards_location(self, ship, location):
        horizontal_diff, vertical_diff = tuple(np.array(location) - np.array(ship.location))

        # ship in location
        if horizontal_diff == 0 and vertical_diff == 0:
            return

        # ship only need to move horizontally
        if horizontal_diff != 0 and vertical_diff == 0:
            self.move_horizontally(ship, horizontal_diff)

        if horizontal_diff == 0 and vertical_diff != 0:
            self.move_vertically(ship, vertical_diff)

        if horizontal_diff != 0 and vertical_diff != 0:
            if random.randint(0, 1) == 0:
                self.move_horizontally(ship, horizontal_diff)
            else:
                self.move_vertically(ship, vertical_diff)

    def move_vertically(self, ship, vertical_diff):
        if vertical_diff > 0:
            self.move_ship(ship, direction='S')
        else:
            self.move_ship(ship, direction='N')

    def move_horizontally(self, ship, horizontal_diff):
        if horizontal_diff > 0:
            self.move_ship(ship, direction='E')
        else:
            self.move_ship(ship, direction='W')

    def check_route(self, ship, direction):
        current_location = ship.location
        for step in range(ship.ship_speed + 1):
            if step == 0: continue
            new_location = np.array(current_location) + \
                           step * np.array(self.direction_dict[direction])
            new_location = utils.verify_location(new_location, self.board_size)
            current_obj = self.board[new_location[0]][new_location[1]]
            if isinstance(current_obj, Block):
                print(f'ship encountered block in {new_location}')
                new_location = np.array(current_location) + \
                               (step - 1) * np.array(self.direction_dict[direction])
                return new_location
            elif isinstance(current_obj, Island):
                print(f'ship encountered island in {new_location}')
                ship.location = new_location
                ship.frontend_obj.kill()
                return new_location
        return new_location

    def update_tile_ship_left(self, ship):
        current_obj = self.board[ship.location[0]][ship.location[1]]
        if isinstance(current_obj, Ship):
            self.board[ship.location[0]][ship.location[1]] = 'Sea'
        elif isinstance(current_obj, Island):
            print(f'ship of {self.players[ship.player_id].player_name} left island in {current_obj.location}')
            current_obj.ships.remove(ship)

    def update_tile_ship_entered(self, ship):
        current_obj = self.board[ship.location[0]][ship.location[1]]
        if isinstance(current_obj, Island):
            island = current_obj
            if not island.ships:  # no ships on island
                island.add_ship(ship)
            elif island.ships[0].player_id == ship.player_id:  # only my ships on island
                island.add_ship(ship)
            else:  # enemy ships on island!
                # prints island and collision status
                enemy_ship = island.ships[0]
                print(f'Collision detected in island in {island.location} '
                      f'is owned by {self.players[island.own_player_id].player_name} '
                      f'with {island.current_life} HP')

                print(f'{self.players[ship.player_id].player_name} is attacking '
                      f'{self.players[enemy_ship.player_id].player_name}')

                # kills your ship one enemy ship
                enemy_ship.frontend_obj.kill()
                self.players[enemy_ship.player_id].ships.remove(enemy_ship)  # enemy ship
                island.ships.remove(enemy_ship)

                ship.frontend_obj.kill()
                self.players[ship.player_id].ships.remove(ship)  # your ship
        elif isinstance(current_obj, Ship):
            other_ship = current_obj
            other_ship.frontend_obj.kill()
            self.players[other_ship.player_id].ships.remove(other_ship)  # other ship

            ship.frontend_obj.kill()
            self.players[ship.player_id].ships.remove(ship)  # your ship

            self.board[ship.location[0]][ship.location[1]] = 'Sea'
        else:
            self.board[ship.location[0]][ship.location[1]] = ship

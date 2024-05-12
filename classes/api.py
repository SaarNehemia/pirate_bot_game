import random

import numpy as np

import utils
from classes.block import Block
from classes.island import Island
from classes.player import Player
from classes.ship import Ship


class API():
    def __init__(self, board_settings: dict, player_names: list[str], time_out: int):
        # init players in random order
        self.player_names = player_names
        random.shuffle(self.player_names)
        self.players = []
        for player_id, player_name in enumerate(player_names):
            self.players.append(Player(player_id, player_name))

        # Init board and extract all board params to attributes
        self.board = []  # Backend
        for key, value in board_settings.items():
            setattr(self, key, value)
        # self.board_size = board_settings['board_size']
        # self.blocks = board_settings['blocks']
        # self.islands = board_settings['islands']
        # self.players_base_islands_indices = board_settings['players_base_islands_indices']
        # self.players_ship_speed = board_settings['players_ship_speed']
        # self.players_num_ships = board_settings['players_num_ships']
        # self.victory_criterion = board_settings['victory_criterion']

        # Init all other attributes
        self.num_turn = 0
        self.time_out = time_out
        self.direction_dict = {'N': (0, -1),
                               'S': (0, 1),
                               'W': (-1, 0),
                               'E': (1, 0)}

    # ------------------------------- GET API ATTRIBUTES METHODS ----------------------------------- #
    def get_num_turn(self):
        return self.num_turn

    def get_time_out(self):
        return self.time_out

    def get_board_size(self) -> int:
        """
        :return: board side length (board is a board_size X board_size matrix)
        """
        return self.board_size

    def get_player_index(self, player_id: int) -> int:
        """
        :param player_id:
        :return: player index (first or second in turn order)
        """
        player_ids = [player.player_id for player in self.players]
        player_index = player_ids.index(player_id)
        return player_index

    def get_player_ship_speed(self, player_id: int) -> int:
        """

        :param player_id:
        :return: given player ship speed (in board size units).
        """
        player_index = self.get_player_index(player_id)
        return self.players_ship_speed[player_index]

    def get_player_initial_num_ships(self, player_id: int) -> int:
        """
        :param player_id:
        :return: given player initial number of ships
        """
        player_index = self.get_player_index(player_id)
        return self.players_num_ships[player_index]

    def get_victory_criterion(self) -> int:
        """
        Right now there is only one victory criterion: capture X islands.
        :return: number of captured islands that is needed to win.
        """
        return self.victory_criterion

    # --------------------------------- PLAYERS METHODS ------------------------------------------- #
    def get_my_player_id(self) -> int:
        return self.num_turn % len(self.players)

    def get_enemy_player_id(self) -> int:
        return int(not self.get_my_player_id())

    def get_num_players(self) -> int:
        return len(self.players)

    # --------------------------------- BLOCKS METHODS ------------------------------------------- #

    def get_num_blocks(self):
        return len(self.blocks)

    def get_blocks_locations(self) -> list[tuple]:
        blocks_locations = []
        for block in self.blocks:
            blocks_locations.append(block.location)
        return blocks_locations

    # --------------------------------- ISLANDS METHODS ------------------------------------------- #

    def get_num_islands(self) -> int:
        return len(self.islands)

    def get_islands_locations(self) -> list[tuple]:
        islands_locations = []
        for island in self.islands:
            islands_locations.append(island.location)
        return islands_locations

    def get_player_owned_islands_indices(self, player_id: int) -> list[int]:
        player_owned_island_indices = []
        for island_id, island in enumerate(self.islands):
            if island.own_player_id == player_id:
                player_owned_island_indices.append(island_id)
        return player_owned_island_indices

    def get_player_owned_islands_locations(self, player_id: int) -> list[tuple]:
        player_owned_islands = utils.split_list_according_to_indices_list(my_list=self.islands,
                                                                          indices_list=
                                                                          self.get_player_owned_islands_indices(
                                                                              player_id),
                                                                          return_in_indices_list=True)
        return [island.location for island in player_owned_islands]

    def get_num_player_owned_islands(self, player_id: int) -> int:
        return len(self.get_player_owned_islands_indices(player_id))

    def get_neutral_islands_indices(self) -> list[int]:
        all_owned_island_indices = []
        for player_id, _ in self.players:
            player_owned_island_indices = self.get_player_owned_islands_indices(player_id)
            all_owned_island_indices.extend(player_owned_island_indices)
        neutral_islands = utils.split_list_according_to_indices_list(my_list=self.islands,
                                                                     indices_list=all_owned_island_indices,
                                                                     return_in_indices_list=False)
        return [neutral_island_index for neutral_island_index, _ in enumerate(neutral_islands)]

    def get_neutral_islands_locations(self) -> list[tuple]:
        neutral_islands = utils.split_list_according_to_indices_list(my_list=self.islands,
                                                                     indices_list=self.get_neutral_islands_indices(),
                                                                     return_in_indices_list=True)
        return [island.location for island in neutral_islands]

    # --------------------------------- SHIPS METHODS ------------------------------------------- #

    def get_player_num_ships(self, player_id: int) -> int:
        return len(self.players[player_id].ships)

    def get_player_ships_ids(self, player_id: int) -> list[int]:
        return self.players[player_id].get_ships_ids()

    def get_player_ships_locations(self, player_id: int) -> list[tuple]:
        return self.players[player_id].get_ships_locations()

    def get_player_ship_location_from_id(self, player_id: int, ship_id: int) -> tuple:
        player_ships_locations = self.get_player_ships_locations(player_id)
        ship_index = self.get_player_ships_ids(player_id).index(ship_id)
        return player_ships_locations[ship_index]

    def move_ship(self, ship_id: int, direction: str):
        current_player_obj = self.players[self.get_my_player_id()]
        ship = current_player_obj.get_ship_obj(ship_id)
        player_id = self.get_my_player_id()
        self._update_tile_ship_left(ship)
        new_location, collision_info = self.check_ship_route(player_id=player_id,
                                                             ship_id=ship_id,
                                                             direction=direction)
        ship.update_location(new_location, self.board_size)
        if collision_info == 'islands':
            ship.frontend_obj.kill()
        self._update_tile_ship_entered(ship)

    def move_ship_towards_location(self, ship_id, location):
        current_player_obj = self.players[self.get_my_player_id()]
        ship = current_player_obj.get_ship_obj(ship_id)
        horizontal_diff, vertical_diff = tuple(np.array(location) - np.array(ship.location))

        # ship in location
        if horizontal_diff == 0 and vertical_diff == 0:
            return

        # ship only need to move horizontally
        if horizontal_diff != 0 and vertical_diff == 0:
            self._move_horizontally(ship_id, horizontal_diff)

        if horizontal_diff == 0 and vertical_diff != 0:
            self._move_vertically(ship_id, vertical_diff)

        if horizontal_diff != 0 and vertical_diff != 0:
            if random.randint(0, 1) == 0:
                self._move_horizontally(ship_id, horizontal_diff)
            else:
                self._move_vertically(ship_id, vertical_diff)

    def check_ship_route(self, player_id: int, ship_id: int, direction: str) \
            -> tuple[tuple, tuple[str, tuple, int]]:
        ship = self.players[player_id].get_ship_obj(ship_id)
        current_location = ship.location
        collision_info = ""
        for step in range(ship.ship_speed + 1):
            if step == 0: continue
            new_location = tuple(np.array(current_location) + \
                                 step * np.array(self.direction_dict[direction]))
            new_location = utils.verify_location(new_location, self.board_size)
            current_obj = self.board[new_location[0]][new_location[1]]
            if isinstance(current_obj, Block):
                print(f'ship encountered block in {new_location}')
                collision_info = 'blocks', new_location, current_obj.block_id
                new_location = tuple(np.array(current_location) + \
                                     (step - 1) * np.array(self.direction_dict[direction]))
                return new_location, collision_info
            elif isinstance(current_obj, Island):
                collision_info = 'islands', new_location, current_obj.island_id
                print(f'ship encountered island in {new_location}')
                return new_location, collision_info
            return new_location, collision_info

    # --------------------------------- INTERNAL METHODS ------------------------------------------ #

    def _move_vertically(self, ship_id: int, vertical_diff: int):
        if vertical_diff > 0:
            self.move_ship(ship_id, direction='S')
        else:
            self.move_ship(ship_id, direction='N')

    def _move_horizontally(self, ship_id: int, horizontal_diff: int):
        if horizontal_diff > 0:
            self.move_ship(ship_id, direction='E')
        else:
            self.move_ship(ship_id, direction='W')

    def _update_tile_ship_left(self, ship: Ship):
        current_obj = self.board[ship.location[0]][ship.location[1]]
        if isinstance(current_obj, Ship):
            self.board[ship.location[0]][ship.location[1]] = 'Sea'
        elif isinstance(current_obj, Island):
            print(f'ship of {self.players[ship.player_id].player_name} left island in {current_obj.location}')
            current_obj.remove_ship(ship)

    def _update_tile_ship_entered(self, ship: Ship):
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
                island.remove_ship(enemy_ship)
                self._ships_collide(enemy_ship, ship)

        elif isinstance(current_obj, Ship):  # ship collision
            other_ship = current_obj
            self._ships_collide(ship, other_ship)
            self.board[ship.location[0]][ship.location[1]] = 'Sea'
        else:  # move ship freely
            self.board[ship.location[0]][ship.location[1]] = ship

    def _ships_collide(self, ship1: Ship, ship2: Ship):
        self._kill_ship(ship1)
        self._kill_ship(ship2)

    def _kill_ship(self, ship: Ship):
        # Remove from backend
        player = self.players[ship.player_id]
        player.remove_ship(ship)

        # Remove from frontend
        ship.frontend_obj.kill()

import random
from typing import Union

import numpy as np

import utils
from classes.block import Block
from classes.island import Island
from classes.player import Player
from classes.ship import Ship


class API():
    def __init__(self, board_name: str, player_names: list[str], max_num_turns: int):
        # init players in random order
        self.player_names = player_names
        random.shuffle(self.player_names)
        self.players = []
        for player_id, player_name in enumerate(player_names):
            self.players.append(Player(player_id, player_name))

        # Init board and extract all board settings to API attributes
        self.board = []  # Backend
        board_class = utils.get_class_from_module_name(folder_name='boards',
                                                       module_name=board_name)
        for key, value in board_class.get_board_settings().items():
            setattr(self, key, value)

        # Init all other attributes
        self.num_turn = 1
        self.max_num_turns = max_num_turns
        self.directions_dict = {'N': np.array([0, -1]),
                                'S': np.array([0, 1]),
                                'W': np.array([-1, 0]),
                                'E': np.array([1, 0])}

    # ------------------------------- GET API ATTRIBUTES METHODS ----------------------------------- #
    def get_num_turn(self) -> int:
        """
        :return: current turn number.
        """
        return self.num_turn

    def get_max_num_turns(self) -> int:
        """
        :return: maximal num turns until game ends.
        """
        return self.max_num_turns

    def get_directions_dict(self):
        """
        :return: directions dict (key=letter, value=normalized vector)
        """
        return self.directions_dict

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
        """
        :return: your player id to use in other functions.
        """
        return self.num_turn % len(self.players)

    def get_enemy_player_id(self) -> int:
        """
        :return: enemy player id to use in other functions.
        """
        return int(not self.get_my_player_id())

    def get_num_players(self) -> int:
        """
        :return: number of players in the game.
        """
        return len(self.players)

    # --------------------------------- BLOCKS METHODS ------------------------------------------- #

    def get_blocks_info(self) -> list[dict]:
        """
        :return: all blocks location in the current board.
        """
        blocks_info = []
        for block in self.blocks:
            blocks_info.append({'id': block.block_id,
                                'location': block.location,
                                'current_life': block.current_life})
        return blocks_info

    # --------------------------------- ISLANDS METHODS ------------------------------------------- #

    def get_islands_info(self, **kwargs) -> list[dict]:
        """
        :param player_id: use -1 for neutral island, player_id for specific player or not at all for all islands
        :return: List with info on all islands (or only neutral or only that given player owns).
                 Each island info is a tuple of (id, own player id, location, current life, num ships on island, ship's player id).
        """

        islands_info = []
        for island in self.islands:
            island_ships_player_id = island.ships[0].player_id if island.ships else -1
            island_info = {'id': island.island_id,
                           'own_player_id': island.own_player_id,
                           'location': island.location,
                           'current_life': island.current_life,
                           'num_ships': len(island.ships),
                           'ships player_id': island_ships_player_id}
            # if player_id given return only islands info of given player.
            if 'player_id' in kwargs:
                player_id = kwargs['player_id']
                if island.own_player_id == player_id:
                    islands_info.append(island_info)
            # if player_id not given return all islands info on board.
            else:
                islands_info.append(island_info)

        return islands_info

    # --------------------------------- SHIPS METHODS ------------------------------------------- #

    def get_player_ships_info(self, player_id: int) -> list[dict]:
        """
        :param player_id:
        :return: List of given player current ships info (id, location, ship speed, is_moved).
        """
        return self.players[player_id].get_ships_info()

    def get_player_ship_location_from_id(self, player_id: int, ship_id: int) -> np.ndarray:
        """
        :param player_id:
        :param ship_id:
        :return: ship location from ship id of given player.
        """
        player_ships_info = self.get_player_ships_info(player_id)
        player_ships_ids = [player_ship_info['id'] for player_ship_info in player_ships_info]
        player_ships_locations = [player_ship_info['location'] for player_ship_info in player_ships_info]
        ship_index = player_ships_ids.index(ship_id)
        return player_ships_locations[ship_index]

    def move_ship_in_direction(self, ship_id: int, direction: str) -> None:
        """
         This function moves given ship in given direction on board according to ship speed and collisions.
         Only horizontal movement or vertical movement are supported.
         If reached collision (block/island/other ship), move until possible and act accordingly.
         If reached board limits, stay there.
        :param ship_id:
        :param direction: options: 'N' (north, up), 'E' (east, right), 'W' (west, left), 'S' (south, down)
        """
        current_player_obj = self.players[self.get_my_player_id()]
        ship = current_player_obj.get_ship_obj(ship_id)
        destination = ship.ship_speed * self.directions_dict[direction]
        self.move_ship_towards_destination(ship_id, destination)

    def move_ship_towards_destination(self, ship_id, destination) -> None:
        """
        This function moves given ship towards given destination on board according to ship speed and collisions.
        Both horizontal/vertical movement and diagonal movement are supported.
        If reached collision (block/island/other ship), move until possible and act accordingly.
        If reached board limits, stay there.
        :param ship_id:
        :param location:
        """
        # check ship route to destination
        current_player_obj = self.players[self.get_my_player_id()]
        ship = current_player_obj.get_ship_obj(ship_id)
        player_id = self.get_my_player_id()

        # Tried to move same ship twice in the same turn
        if ship.is_moved:
            current_player_name = current_player_obj.player_name
            raise utils.InvalidMoveError(f"{current_player_name} tried to move ship {ship_id} twice.")

        # Move ship
        print(f"ship {ship_id} wants to move from {ship.location} to {destination}")
        new_location, collision_info = self.check_ship_route_to_destination(player_id, ship_id, destination)

        # update ship location
        print(f"ship {ship_id} move from {ship.location} to {new_location}")
        if not (new_location == ship.location).all():
            self._update_tile_ship_left(ship)
            ship.update_location(new_location, self.board_size)
            self._update_tile_ship_entered(ship)

    def check_ship_route_to_destination(self, player_id: int, ship_id: int, destination: np.ndarray) \
            -> tuple[np.ndarray, dict]:
        """
        This function checks if given player's ship route from its location to given destination is possible.
        If no collisions are detected it returns the destination and collision info set to {'no', None}.
        If a collision is detected it return the last possible location and collision info.
        :param player_id:
        :param ship_id:
        :param destination:
        :return: new_location:   destination (in case of no collision) or last possible location (in case of collision)
                 collision_info: dictionary containing collision type ('no'/'blocks'/'islands'/'ships') and relevant ids
                                 (None for sea / island id / block id / player id & ship id)
        """
        ship = self.players[player_id].get_ship_obj(ship_id)
        new_location, collision_info = self.check_route_from_location_to_destination(location=ship.location,
                                                                                     destination=destination,
                                                                                     num_steps=ship.ship_speed)
        return new_location, collision_info

    def check_route_from_location_to_destination(self, location: np.ndarray, destination: np.ndarray,
                                                 num_steps: int = np.inf):
        """
        This function checks if the route from given location to given destination is possible according to num steps given.
        num steps can be ship speed or other, and if leave empty it will check route from location up to destination.
        If no collisions are detected it returns the destination and collision info set to {'no', None}
        If a collision is detected it return the last possible location and collision info.
        :param location:
        :param destination:
        :param num_steps:
        :return: new_location:   destination (in case of no collision) or last possible location (in case of collision)
                 collision_info: dictionary containing collision type ('no'/'blocks'/'islands'/'ships') and relevant ids
                                 (None for sea / island id / block id / player id & ship id)
        """

        # update horizontal and vertical diff
        last_location = location
        location_diff = destination - last_location

        # Set num steps if not given
        if num_steps == np.inf:
            num_steps = sum(location_diff)

        for step in range(num_steps + 1):
            if step == 0: continue

            # location reached destination
            if not location_diff.any():
                break

            # ship need to move diagonally so choose randomly between horizontally and vertically
            elif location_diff.all():
                random_index = random.randint(0, 1)
                direction_value = np.array([location_diff[random_index], 0]) / abs(location_diff[random_index])
                direction_value = np.flip(direction_value) if random_index else direction_value  # vertical if needed

            # ship only need to move horizontally or vertically
            else:
                direction_value = location_diff / max(abs(location_diff))

            # get new location and check for collision
            direction_key = self._get_direction_key(direction_value)
            new_location = last_location + self.directions_dict[direction_key]
            collision_info = self.check_location(new_location)

            # In case of detected collision try other direction if diagonal movement
            if collision_info['collision type'] != 'no' and location_diff.all():
                # check other direction if diagonal movement
                random_index = int(not random_index)
                direction_value = np.array([location_diff[random_index], 0]) / abs(location_diff[random_index])
                direction_value = np.flip(direction_value) if random_index else direction_value  # vertical if needed
                direction_key = self._get_direction_key(direction_value)
                new_location = last_location + self.directions_dict[direction_key]
                collision_info = self.check_location(new_location)

            # In case of detected collision return last possible location and collision info
            if collision_info['collision type'] != 'no':
                if collision_info['collision type'] == 'blocks':  # block collision
                    new_location = last_location
                return new_location, collision_info

            # update horizontal and vertical diff
            last_location = new_location
            location_diff = destination - last_location

        collision_info = self.check_location(last_location)
        return last_location, collision_info

    def check_location(self, location) -> dict:
        """
        This function checks if given location is occupied and returns relevant collision info.
        :param location:
        :return: dictionary containing: collision type ('no'/'blocks'/'islands'/'ships')
                                        and relevant ids (None for sea / island id / block id / player id & ship id)
        """
        location = utils.verify_location(location, self.board_size)
        current_obj = self.board[location[0]][location[1]]
        collision_info = dict()

        if isinstance(current_obj, str):  # Sea tile
            collision_info = self._set_collision_info('no', None)

        elif isinstance(current_obj, Block):  # block tile
            print(f'There is a block in {location}')
            collision_info = self._set_collision_info('blocks', None)

        elif isinstance(current_obj, Island):  # island tile
            print(f'There is an island in {location}')
            collision_info = self._set_collision_info('islands', current_obj.island_id)

        elif isinstance(current_obj, Ship):  # ship tile
            print(f'There is another ship in {location}')
            collision_info = self._set_collision_info('ships', (current_obj.player_id, current_obj.ship_id))

        return collision_info

    # --------------------------------- INTERNAL METHODS ------------------------------------------ #

    def _get_direction_key(self, direction_value: np.ndarray) -> str:
        """
        This function get direction key (letter) from direction value (vector).
        :param direction_value: must be only vertical or only horizontal.
        :return: direction key ('N'/'E'/'W'/'S')
        """
        # Get direction key from value
        all_direction_values = list(self.directions_dict.values())
        for direction_index, current_direction_value in enumerate(all_direction_values):
            if (direction_value == current_direction_value).all():
                direction_key = list(self.directions_dict.keys())[direction_index]
                return direction_key

    @staticmethod
    def _set_collision_info(collision_type: str, collided_object_id=Union[int, tuple[int, int]]):
        collision_info = {'collision type': collision_type,
                          'collided object id': collided_object_id}
        return collision_info

    def _update_tile_ship_left(self, ship: Ship):
        """
        This function checks if ship was on island or not and update board accordingly.
        :param ship:
        """
        current_obj = self.board[ship.location[0]][ship.location[1]]
        if isinstance(current_obj, Ship):
            self.board[ship.location[0]][ship.location[1]] = 'Sea'
        elif isinstance(current_obj, Island):
            print(f'ship of {self.players[ship.player_id].player_name} left island in {current_obj.location}')
            current_obj.remove_ship(ship)

    def _update_tile_ship_entered(self, ship: Ship):
        """
        This function checks final location of ship after turn and update board accordingly.
        If island - check if island is safe: safe - no ships or only only same team ships dock here. Then, dock.
                                             not safe - enemy ships dock here. Attack and kill your ship and 1 enemy ship.
        if ship - destroy both your ship and other ship (whether yours or enemy)
        if sea - travel freely.
        :param ship:
        :return:
        """
        current_obj = self.board[ship.location[0]][ship.location[1]]

        # ship reached island
        if isinstance(current_obj, Island):
            island = current_obj
            if not island.ships or island.ships[0].player_id == ship.player_id:  # no ships or my ships on island
                island.add_ship(ship)
            else:  # enemy ships on island!
                # prints island and collision status
                enemy_ship = island.ships[0]
                print(f'Collision detected in island in {island.location} '
                      f'is owned by {self.players[island.own_player_id].player_name} '
                      f'with {island.current_life} HP')

                print(f'{self.players[ship.player_id].player_name} is attacking '
                      f'{self.players[enemy_ship.player_id].player_name}')

                # kills your ship and one enemy ship
                island.remove_ship(enemy_ship)
                self._ships_collide(enemy_ship, ship)

        # ship collision
        elif isinstance(current_obj, Ship):
            other_ship = current_obj
            self._ships_collide(ship, other_ship)
            self.board[ship.location[0]][ship.location[1]] = 'Sea'

        # ship destination is sea
        else:
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

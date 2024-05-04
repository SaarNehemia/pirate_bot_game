from typing import Callable

from classes.ship import Ship


class Player:
    def __init__(self, player_id: int, player_name: str):
        self.player_id = player_id
        self.player_name = player_name

        player_info = getattr(__import__(f'players.{self.player_name}'), self.player_name)
        self.player_params = player_info.params
        self.player_do_turn_func = player_info.do_turn

        self.ships = []
        for ship_id in range(self.player_params['num_ships']):
            self.ships.append(Ship(player_id=player_id, ship_id=ship_id,
                                   ship_speed=self.player_params['ship_speed'],
                                   location=self.player_params['base_location']))

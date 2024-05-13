import numpy as np

import utils
from classes.ship import Ship


class Island:
    def __init__(self, location: np.ndarray, current_life: int, ship_creation_time: float):
        self.island_id = -1
        self.own_player_id = -1  # not captured by any player
        self.location = location
        self.ships = []
        self.current_life = current_life
        self.ship_creation_time = ship_creation_time
        self.frontend_obj: utils.FrontEndObj = utils.FrontEndObj(name='Island', location=location)

    def add_ship(self, ship: Ship):
        self.ships.append(ship)
        ship.frontend_obj.kill()

    def remove_ship(self, ship: Ship):
        self.ships.remove(ship)

    def assign_id(self, island_id):
        self.island_id = island_id

    def get_ship_obj(self, ship_id):
        ship_ids, _ = self.get_ships_ids()
        ship_index = ship_ids.index(ship_id)
        ship = self.ships[ship_index]
        return ship

    def get_ships_ids(self):
        player_id = self.ships[0].player_id if self.ships else 0
        ship_ids = [ship.ship_id for ship in self.ships]
        return ship_ids, player_id




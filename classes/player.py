import utils
from classes.ship import Ship


class Player:
    def __init__(self, player_id: int, player_name: str):
        self.player_id = player_id
        self.player_name = player_name
        self.player_class = utils.get_class_from_module_name(folder_name='players',
                                                             module_name=self.player_name)()
        self.ships = []
        self.max_ship_id = 0

    def add_ship(self, ship: Ship):
        self.ships.append(ship)

    def remove_ship(self, ship: Ship):
        self.ships.remove(ship)

    def get_ship_obj(self, ship_id):
        ships_info = self.get_ships_info()
        ships_ids = [ship_info['id'] for ship_info in ships_info]
        ship_index = ships_ids.index(ship_id)
        ship = self.ships[ship_index]
        return ship

    def get_ships_info(self) -> list[dict]:
        return [{'id': ship.ship_id,
                 'location': ship.location,
                 'speed': ship.ship_speed,
                 'is_moved': ship.is_moved} for ship in self.ships]

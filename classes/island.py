import utils


class Island:
    def __init__(self, location: tuple, current_life: int, ship_creation_time: float):
        self.own_player_id = -1  # not captured by any player
        self.location = location
        self.ships = []
        self.current_life = current_life
        self.ship_creation_time = ship_creation_time
        self.frontend_obj = utils.FrontEndObj(name='Island')

    def add_ship(self, ship):
        self.ships.append(ship)

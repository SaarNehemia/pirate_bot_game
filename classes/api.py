import utils


class API():
    def __init__(self):
        pass

    def move_ship(self, ship, direction):
        ship.location = ship.location + ship.ship_speed * utils.DIRECTION_DICT[direction]

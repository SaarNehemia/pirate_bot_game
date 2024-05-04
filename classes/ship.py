DIRECTION_DICT = {'N': (0, 1),
                  'S': (0, -1),
                  'W': (-1, 0),
                  'E': (1, 0)}


class Ship:
    def __init__(self, player_id: int, ship_id: int, ship_speed: float, location: tuple):
        self.player_id = player_id
        self.ship_id = ship_id
        self.ship_speed = ship_speed
        self.location = location

    def move_ship(self, direction):
        self.location = self.location + self.ship_speed * DIRECTION_DICT[direction]

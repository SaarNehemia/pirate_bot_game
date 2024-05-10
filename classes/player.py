from classes.ship import Ship


class Player:
    def __init__(self, player_id: int, player_name: str):
        self.player_id = player_id
        self.player_name = player_name

        player_info = getattr(__import__(f'players.{self.player_name}'), self.player_name)
        self.player_do_turn_func = player_info.do_turn
        self.ships = []

    def add_ship(self, ship: Ship):
        self.ships.append(ship)

    def remove_ship(self, ship: Ship):
        self.ships.remove(ship)

import classes.api as game_api


class Yossi:
    def __init__(self):
        self.strategy = 1

    def do_turn(self, game_api: game_api.API):
        my_player_id = game_api.get_my_player_id()
        enemy_player_id = game_api.get_enemy_player_id()

        if self.strategy == 1:
            # strategy 1: move my first ship to first enemy ship
            try:
                my_first_ship_id = game_api.get_player_ships_info(my_player_id)[0]['id']
            except IndexError:
                print('No ships for me :(')
                return

            try:
                first_enemy_ship_id = game_api.get_player_ships_info(enemy_player_id)[0]['id']
            except IndexError:
                print('No ships for enemy :)')
                self.strategy = 2
                print(f'Changing strategy to {self.strategy}')
                return

            enemy_ship_location = game_api.get_player_ship_location_from_id(player_id=enemy_player_id,
                                                                            ship_id=first_enemy_ship_id)
            game_api.move_ship_towards_destination(ship_id=my_first_ship_id,
                                                   destination=enemy_ship_location)

        elif self.strategy == 2:
            # strategy 2: move my first ship towards first enemy island
            try:
                my_first_ship_id = game_api.get_player_ships_info(my_player_id)[0]['id']
            except IndexError:
                print('No ships for me :(')
                return

            try:
                enemy_islands_info = game_api.get_islands_info(player_id=enemy_player_id)
                first_enemy_island_location = enemy_islands_info[0]['location']
            except IndexError:
                print('No enemy islands :)')
                return

            game_api.move_ship_towards_destination(ship_id=my_first_ship_id,
                                                   destination=first_enemy_island_location)

        elif self.strategy == 3:
            # strategy 3: move my first ship around my first island
            round_time = 300
            rest_time = 100

            try:
                my_first_ship_id = game_api.get_player_ships_info(my_player_id)[0]['id']
                my_first_ship_location = game_api.get_player_ships_info(my_player_id)[0]['location']
            except IndexError:
                print('No ships for me :(')
                return

            try:
                my_first_island_location = game_api.get_islands_info(player_id=my_player_id)[0]['location']
            except IndexError:
                print('No islands for me :(')
                return

            # ship rounds island only if it is not in base island
            if game_api.get_num_turn() < game_api.get_num_players()\
                    or my_first_ship_location != my_first_island_location:
                self.ship_go_round(game_api=game_api, ship_id=my_first_ship_id, round_time=round_time)
                return

            # ship leaves island if rest time passed
            if game_api.get_num_turn() % (round_time + rest_time) == 0:
                self.ship_go_round(game_api=game_api, ship_id=my_first_ship_id, round_time=round_time)
                return

    @staticmethod
    def ship_go_round(game_api: game_api.API, ship_id: int, round_time: int):
        if 0 <= game_api.get_num_turn() % round_time < 0.25 * round_time:
            game_api.move_ship_in_direction(ship_id=ship_id, direction='S')
        elif 0.25 * round_time <= game_api.get_num_turn() % round_time < 0.5 * round_time:
            game_api.move_ship_in_direction(ship_id=ship_id, direction='W')
        elif 0.5 * round_time <= game_api.get_num_turn() % round_time < 0.75 * round_time:
            game_api.move_ship_in_direction(ship_id=ship_id, direction='N')
        elif 0.75 * round_time <= game_api.get_num_turn() % round_time < round_time:
            game_api.move_ship_in_direction(ship_id=ship_id, direction='E')

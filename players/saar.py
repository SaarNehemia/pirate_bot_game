import classes.api as game_api

PLAYER_NAME = 'saar'


def do_turn(game_api: game_api.API):
    round_time = 500
    if 0 <= game_api.num_turn % round_time < 0.25 * round_time:
        my_player_obj = game_api.get_my_player_obj(PLAYER_NAME)
        my_first_ship = my_player_obj.ships[0]
        game_api.move_ship(ship=my_first_ship, direction='N')
    elif 0.25 * round_time <= game_api.num_turn % round_time < 0.5 * round_time:
        my_player_obj = game_api.get_my_player_obj(PLAYER_NAME)
        my_first_ship = my_player_obj.ships[0]
        game_api.move_ship(ship=my_first_ship, direction='E')
    elif 0.5 * round_time <= game_api.num_turn % round_time < 0.75 * round_time:
        my_player_obj = game_api.get_my_player_obj(PLAYER_NAME)
        my_first_ship = my_player_obj.ships[0]
        game_api.move_ship(ship=my_first_ship, direction='S')
    elif 0.75 * round_time <= game_api.num_turn % round_time < round_time:
        my_player_obj = game_api.get_my_player_obj(PLAYER_NAME)
        my_first_ship = my_player_obj.ships[0]
        game_api.move_ship(ship=my_first_ship, direction='W')

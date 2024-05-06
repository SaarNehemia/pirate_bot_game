import classes.api as game_api

PLAYER_NAME = 'yossi'


def do_turn(game_api: game_api.API):
    my_player_obj = game_api.get_my_player_obj(PLAYER_NAME)
    my_first_ship = my_player_obj.ships[0]
    game_api.move_ship(ship=my_first_ship, direction='S')

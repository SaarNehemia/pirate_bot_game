import classes.api as game_api


def do_turn(game_api: game_api.API):
    my_player_obj = game_api.get_my_player_obj()
    if my_player_obj.ships:
        my_first_ship = my_player_obj.ships[0]
    else:
        return

    # TODO - change this to API function of patrol_radius(round_time=int(ship_speed)/radius)
    round_time = 300
    my_base_island_location = game_api.islands[game_api.players_base_islands_indices[
        game_api.get_my_player_id(PLAYER_NAME)]].location
    if my_first_ship.location != my_base_island_location or game_api.num_turn == 1:
        if 0 <= game_api.num_turn % round_time < 0.25 * round_time:
            game_api.move_ship(ship=my_first_ship, direction='S')
            return
        elif 0.25 * round_time <= game_api.num_turn % round_time < 0.5 * round_time:
            game_api.move_ship(ship=my_first_ship, direction='W')
            return
        elif 0.5 * round_time <= game_api.num_turn % round_time < 0.75 * round_time:
            game_api.move_ship(ship=my_first_ship, direction='N')
            return
        elif 0.75 * round_time <= game_api.num_turn % round_time < round_time:
            game_api.move_ship(ship=my_first_ship, direction='E')
            return

    if game_api.num_turn % 100 == 0:
        if 0 <= game_api.num_turn % round_time < 0.25 * round_time:
            game_api.move_ship(ship=my_first_ship, direction='S')
            return
        elif 0.25 * round_time <= game_api.num_turn % round_time < 0.5 * round_time:
            game_api.move_ship(ship=my_first_ship, direction='W')
            return
        elif 0.5 * round_time <= game_api.num_turn % round_time < 0.75 * round_time:
            game_api.move_ship(ship=my_first_ship, direction='N')
            return
        elif 0.75 * round_time <= game_api.num_turn % round_time < round_time:
            game_api.move_ship(ship=my_first_ship, direction='E')
            return

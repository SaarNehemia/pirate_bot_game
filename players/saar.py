import classes.api as game_api


def do_turn(game_api: game_api.API):

    strategy = 1

    my_player_obj = game_api.get_my_player_obj()
    if my_player_obj.ships:
        my_first_ship = my_player_obj.ships[0]
    else:
        return

    if strategy == 1:
        # Strategy 1: move my first ship to first enemy ship
        enemy_player_id = ~my_player_obj.player_id
        enemy_player = game_api.players[enemy_player_id]
        if enemy_player.ships:
            enemy_first_ship = enemy_player.ships[0]
            game_api.move_ship_towards_location(ship=my_first_ship, location=enemy_first_ship.location)

    elif strategy == 2:
        # Strategy 2: move my first ship towards enemy base island
        enemy_player_id = ~my_player_obj.player_id
        enemy_base_island_location = game_api.islands[game_api.players_base_islands_indices[enemy_player_id]].location
        game_api.move_ship_towards_location(ship=my_first_ship, location=enemy_base_island_location)

    elif strategy == 3:
        # Strategy 3: move my first ship around my base island
        round_time = 300
        my_base_island_location = game_api.islands[game_api.players_base_islands_indices[
            game_api.get_my_player_id()]].location
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


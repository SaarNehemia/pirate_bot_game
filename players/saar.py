import classes.api as game_api


def do_turn(game_api: game_api.API):
    my_player_obj = game_api.get_my_player_obj()
    if my_player_obj.ships:
        my_first_ship = my_player_obj.ships[0]
    else:
        return

    enemy_player_id = ~my_player_obj.player_id
    enemy_base_island_location = game_api.islands[game_api.players_base_islands_indices[enemy_player_id]].location
    game_api.move_ship_towards_location(ship=my_first_ship, location=enemy_base_island_location)

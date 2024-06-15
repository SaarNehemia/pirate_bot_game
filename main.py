import utils
from classes.api import API
from classes.game import Game

if __name__ == '__main__':
    # ----------------------------------------- Choose games settings ----------------------------------------- #
    player_names: list[str] = ['yossi', 'saar']
    board_name: str = 'board1'
    num_games: int = 5
    max_num_turns: int = 1000
    to_draw_game: bool = True
    debug_mode = True

    # ---------------------------------------------- DO NOT TOUCH ---------------------------------------------- #

    # Init game results count
    wins_count = dict((player_name, 0) for player_name in player_names)

    # Start game
    for game_number in range(1, num_games + 1):
        print(f"****************** Game number {game_number} out of {num_games} started ******************")

        # init API and game
        game_api = API(board_name=board_name,
                       player_names=player_names,
                       max_num_turns=max_num_turns)
        current_game = Game(game_api=game_api,
                            game_number=game_number, num_games=num_games, wins_count=wins_count,
                            to_draw_game=to_draw_game, debug_mode=debug_mode)

        # Play game
        player_name_won = current_game()

        # Save game result
        if player_name_won != "draw":
            wins_count[player_name_won] += 1

    # Print all games summary result
    print(f"{num_games=}")
    print(f"{wins_count=}")
from classes.api import API
from classes.game import Game

if __name__ == '__main__':
    # Choose games settings
    player_names: list[str] = ['yossi', 'saar']
    board_name: str = 'board1'
    num_games: int = 2
    time_out: int = 1000
    to_draw_game: bool = True

    # Init game results count
    wins_count = dict((player_name, 0) for player_name in player_names)
    draw_count = 0

    # Start game
    for i in range(num_games):
        print(f"****************** Game number {i + 1} out of {num_games} started ******************")
        # Import board settings
        board = __import__(f'boards.{board_name}')
        board_settings = getattr(board, board_name).get_board_settings()

        # init API and game
        game_api = API(board_settings=board_settings,
                       player_names=player_names,
                       time_out=time_out)
        current_game = Game(game_api, to_draw_game  )

        # Play game
        player_name_won = current_game()

        # Save game result
        if player_name_won == "draw":
            draw_count += 1
        else:
            wins_count[player_name_won] += 1

    # Print all games summary result
    print(f"{wins_count=}")
    print(f"{draw_count=}")

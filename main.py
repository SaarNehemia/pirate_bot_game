from classes.game import Game

if __name__ == '__main__':
    # Choose board and player names:
    board_name = 'board1'
    player_names = ['yossi', 'saar']
    num_games = 2
    time_out = 100

    # Init game results count
    wins_count = dict((player_name, 0) for player_name in player_names)
    draw_count = 0

    # Import board params
    board = __import__(f'boards.{board_name}')
    board_params = getattr(board, board_name).board_params

    # Start game
    for _ in range(num_games):
        current_game = Game(board_params=board_params,
                            player_names=player_names,
                            time_out=time_out)
        player_name_won = current_game()
        if player_name_won == "draw":
            draw_count += 1
        else:
            wins_count[player_name_won] += 1

    # Print run result
    print(f"{wins_count=}")
    print(f"{draw_count=}")



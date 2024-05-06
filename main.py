from classes.game import Game

if __name__ == '__main__':
    # Choose board and player names:
    board_name = 'board1'
    player_names = ['yossi', 'saar']

    # Import board params
    board = __import__(f'boards.{board_name}')
    board_params = getattr(board, board_name).board_params

    # Start game
    game = Game(board_params=board_params, player_names=player_names)

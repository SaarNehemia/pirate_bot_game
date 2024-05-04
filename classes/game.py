import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

from classes.player import Player

# first index: value, 3 other indices: R,G,B values
COLOR_DICT = {'Sea': [0, 170, 255, 245],  # light blue
              'Block': [1, 0, 0, 0],  # black
              'Island': [2, 208, 130, 40],  # brown
              'Ship': [3, 200, 200, 200],  # gray
              }


class Game:
    def __init__(self, board_params: dict, player_names: list[str]):
        # init board
        self.board = []
        self.board_params = board_params
        self.board_img = np.array([])

        # init players
        self.player_names = player_names
        random.shuffle(self.player_names)
        self.players = []
        for player_id, player_name in enumerate(player_names):
            self.players.append(Player(player_id, player_name))

        # draw board
        self.init_board()

    def init_board(self):
        board_size = self.board_params['board_size']
        blocks_locations = self.board_params['blocks_locations']
        islands_locations = self.board_params['islands_locations']

        # Init board with 'Sea' tiles
        for i in range(board_size):
            self.board.append([])
            for j in range(board_size):
                self.board[i].append('Sea')

        # Add blocks
        for block_locations in blocks_locations:
            self.board[block_locations[0]][block_locations[1]] = 'Block'

        # Add islands
        for islands_locations in islands_locations:
            self.board[islands_locations[0]][islands_locations[1]] = 'Island'

        # Add ships
        for player in self.players:
            for ship in player.ships:
                self.board[ship.location[0]][ship.location[1]] = 'Ship'

        # Draw board
        self.draw_board()

    def draw_board(self):
        # transform board (list of str) to board_img (list of values)
        self.board_img = np.zeros_like(self.board)
        board_size = self.board_params['board_size']
        for i in range(board_size):
            for j in range(board_size):
                self.board_img[i][j] = COLOR_DICT[self.board[i][j]][0]

        # define colormap based on COLOR_DICT
        ca = []
        for value in COLOR_DICT.values():
            ca.append(value)
        ca = np.array(ca)

        u, ind = np.unique(self.board_img, return_inverse=True)
        b = ind.reshape(self.board_img.shape)

        colors = ca[ca[:, 0].argsort()][:, 1:] / 255.
        cmap = matplotlib.colors.ListedColormap(colors)
        norm = matplotlib.colors.BoundaryNorm(np.arange(len(ca) + 1) - 0.5, len(ca))

        plt.imshow(b, cmap=cmap, norm=norm, aspect='auto', origin='lower')

        # Add colorbar
        # cb = plt.colorbar(ticks=np.arange(len(ca)))
        # cb.ax.set_yticklabels(np.unique(ca[:, 0]))

        plt.show()

    def update_board(self):
        # TODO: think how to update plot and not draw everything again
        pass

    def play_game(self):
        game_end = False
        player_won = ""
        while not game_end:
            pass
        print(f"{player_won} won!")



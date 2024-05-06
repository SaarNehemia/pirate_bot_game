import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import pygame as pg
from pygame.locals import KEYDOWN, K_ESCAPE

import utils
from classes.block import Block
from classes.island import Island
from classes.player import Player
from classes.ship import Ship


class Game:
    def __init__(self, board_params: dict, player_names: list[str]):

        # init players
        self.player_names = player_names
        random.shuffle(self.player_names)
        self.players = []
        for player_id, player_name in enumerate(player_names):
            self.players.append(Player(player_id, player_name))

        # init board
        self.board_size = board_params['board_size']
        self.board_params = board_params
        self.blocks: list[Block] = board_params['blocks']
        self.islands: list[Island] = board_params['islands']
        self.board = []

        # Init screen
        pg.init()
        self.screen = pg.display.set_mode([utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT])
        self.screen.fill(utils.COLORS_DICT['Sea'])  # fill all with sea (light blue)

        # Start game
        self.start_game()

    def start_game(self):
        # Init game
        self.init_game()

        # Game loop
        running = True
        game_end = False
        while running:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == pg.QUIT:
                    running = False

            if game_end:
                running = False
                player_won = ""
                print(f"{player_won} won!")

            # Play players turns
            # TODO: write example do_turn function to test ship movement
            for player in self.players:
                player.player_do_turn_func()

            # Update game
            self.update_game()

            pg.display.flip()

        pg.quit()

    def init_game(self):
        self.init_board()
        self.init_screen()

    def update_game(self):
        self.update_board()
        self.update_screen()

    def init_board(self):
        # extract variables from board params
        self.blocks = self.board_params['blocks']
        self.islands = self.board_params['islands']
        players_base_islands_indices = self.board_params['players_base_islands_indices']
        players_ship_speed = self.board_params['players_ship_speed']
        players_num_ships = self.board_params['players_num_ships']

        # Init board with 'Sea' tiles
        for i in range(self.board_size):
            self.board.append([])
            for j in range(self.board_size):
                self.board[i].append('Sea')

        # Add blocks
        for block in self.blocks:
            self.board[block.location[0]][block.location[1]] = block

        # Update players
        for player in self.players:
            # Get params
            player_base_island_index = players_base_islands_indices[player.player_id]
            player_num_ships = players_num_ships[player.player_id]
            player_ship_speed = players_ship_speed[player.player_id]
            player_base_island = self.islands[player_base_island_index]

            # Init player ships and base island
            player_base_island.own_player_id = player.player_id
            base_island_location = player_base_island.location
            player_base_island.ships = player_num_ships * [Ship(player_id=player.player_id,
                                                                ship_speed=player_ship_speed,
                                                                location=base_island_location
                                                                )]
            player.ships = player_base_island.ships

        # Add islands
        for island in self.islands:
            self.board[island.location[0]][island.location[1]] = island

    def update_board(self):
        # TODO
        pass

    def init_screen(self):
        # Add blocks, islands and ships
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != 'Sea':
                    location = self.board[i][j].location
                    self.board[i][j].frontend_obj.draw_sprite(self.screen, location, self.board_size)
        pg.display.flip()

    def update_screen(self):
        # TODO
        pg.display.flip()

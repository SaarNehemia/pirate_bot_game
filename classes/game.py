import pygame as pg
from pygame.locals import KEYDOWN, K_ESCAPE

import utils
from classes.api import API
from classes.ship import Ship


class Game:
    def __init__(self, board_params: dict, player_names: list[str]):

        # init board
        self.game_api = API(board_params=board_params,
                            player_names=player_names)

        # Init screen
        self.screen = []

        # Start game
        self.init_game()
        self.game_loop()

    def game_loop(self):
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
            for player in self.game_api.players:
                player.player_do_turn_func(self.game_api)

            # Update frontend
            pg.display.flip()
            breakpoint()

        pg.quit()

    def init_game(self):
        self.init_board()
        self.init_screen()

    def init_board(self):
        # Init board with 'Sea' tiles
        for i in range(self.game_api.board_size):
            self.game_api.board.append([])
            for j in range(self.game_api.board_size):
                self.game_api.board[i].append('Sea')

        # Add blocks
        for block in self.game_api.blocks:
            self.game_api.board[block.location[0]][block.location[1]] = block

        # Update players
        for player in self.game_api.players:
            # Get params
            player_base_island_index = self.game_api.players_base_islands_indices[player.player_id]
            player_base_island = self.game_api.islands[player_base_island_index]
            player_num_ships = self.game_api.players_num_ships[player.player_id]
            player_ship_speed = self.game_api.players_ship_speed[player.player_id]

            # Init player ships and base island
            player_base_island.own_player_id = player.player_id
            base_island_location = player_base_island.location
            player_base_island.ships = player_num_ships * [Ship(player_id=player.player_id,
                                                                ship_speed=player_ship_speed,
                                                                location=base_island_location
                                                                )]
            player.ships = player_base_island.ships

        # Add islands
        for island in self.game_api.islands:
            self.game_api.board[island.location[0]][island.location[1]] = island

    def init_screen(self):
        # Fill all screen with sea (light blue)
        pg.init()
        self.screen = pg.display.set_mode([utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT])
        self.screen.fill(utils.COLORS_DICT['Sea'])

        # Add blocks, islands and ships
        for i in range(self.game_api.board_size):
            for j in range(self.game_api.board_size):
                if self.game_api.board[i][j] != 'Sea':
                    location = self.game_api.board[i][j].location
                    self.game_api.board[i][j].frontend_obj.draw_sprite(self.screen, location, self.game_api.board_size)
        pg.display.flip()


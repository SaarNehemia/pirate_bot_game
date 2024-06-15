import numpy as np
import pygame as pg
from pygame.locals import KEYDOWN, K_ESCAPE

import utils
from classes.api import API
from classes.player import Player
from classes.ship import Ship


class Game:
    def __init__(self, game_api: API, to_draw_game: bool, debug_mode: bool):
        # Init API
        self.game_api = game_api

        # Init backend (board)
        self.player_name_won = ""
        self.debug_mode = debug_mode
        self.max_num_turns = self.game_api.max_num_turns
        self.init_board()

        # Init frontend (screen)
        self.to_draw_game = to_draw_game
        if self.to_draw_game:
            # init screen
            pg.init()
            self.all_sprites = pg.sprite.Group()
            # display_info = pg.display.Info()
            # SCREEN_WIDTH, SCREEN_HEIGHT = 0.8 * np.array([display_info.current_w, display_info.current_h])
            # self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

            self.screen = pg.display.set_mode([utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT])
            pg.display.set_caption('Pirate Bot Game')

            # init text font objects
            self.player_font_size = 24
            self.player_font_obj = pg.font.Font(pg.font.get_default_font(), self.player_font_size)
            self.island_font_size = 12
            self.island_font_obj = pg.font.Font(pg.font.get_default_font(), self.island_font_size)
            self.player_won_font_size = 100
            self.player_won_font_obj = pg.font.Font(pg.font.get_default_font(), self.player_won_font_size)

            # Update screen
            self.draw_all_sprites()

    def __call__(self, *args, **kwargs):
        self.game_loop()
        return self.player_name_won

    def game_loop(self):
        running = True

        while running:
            if self.to_draw_game:
                for event in pg.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                    elif event.type == pg.QUIT:
                        running = False

            # Play players turn
            current_player = self.get_current_player()

            try:
                print(f'Turn {self.game_api.num_turn} starting ({current_player.player_name} playing):')
                self.play_player_turn(current_player)
                print(f'Turn {self.game_api.num_turn} ended.')

                if self.to_draw_game:
                    self.draw_all_sprites()

                self.print_game_status()
                running = self.check_for_victory()

            except Exception as e:
                # notify player that his code has a bug and crashed (not invalid move)
                if not isinstance(e, utils.InvalidMoveError):
                    print(f'{current_player.player_name} code crashed :(')

                # other player wins
                print(f'Turn {self.game_api.num_turn} ended.')
                other_player = self.game_api.players[~current_player.player_id]
                self.player_name_won = other_player.player_name
                print(f"{self.player_name_won} won!")
                running = False

                if self.to_draw_game:
                    self.print_result(player=other_player)

                if self.debug_mode:
                    raise e

            # check if time out reached, if not update num turn
            if self.game_api.num_turn >= self.max_num_turns:
                self.player_name_won = "draw"
                running = False

                if self.to_draw_game:
                    self.print_result(player="")
            else:
                self.game_api.num_turn += 1

        if self.to_draw_game:
            pg.quit()

    def get_current_player(self):
        current_player_id = self.game_api.num_turn % len(self.game_api.players)
        return self.game_api.players[current_player_id]

    def play_player_turn(self, player):
        player.player_class.do_turn(self.game_api)
        self.update_islands()
        self.reset_ships_is_moved()

    def check_for_victory(self):
        running = True
        victory_criterion = self.game_api.victory_criterion
        for player in self.game_api.players:
            num_owned_island = len(self.game_api.get_islands_info(player_id=player.player_id))
            if num_owned_island >= victory_criterion:
                self.player_name_won = player.player_name
                print(f"{self.player_name_won} won!")
                running = False

                if self.to_draw_game:
                    self.print_result(player=player)

        return running

    def print_game_status(self):
        print(f'~~~~~ Game Status (turn {self.game_api.num_turn}): ~~~~~')
        self.print_players_status()
        self.print_islands_status()
        print('~~~~~~~~~~~~~~~~~~~~~~~')

    def print_players_status(self):
        print(f'*** Players status (turn {self.game_api.num_turn}): ***')
        for player in self.game_api.players:
            num_owned_islands = len(self.game_api.get_islands_info(player_id=player.player_id))
            print(f"{player.player_name} has "
                  f"{num_owned_islands} islands and "
                  f"{len(player.ships)} ships.")

            for ship in player.ships:
                print(f'Ship in {ship.location}')

            for island in self.game_api.islands:
                if island.own_player_id == player.player_id:
                    player_own_island = player.player_name
                    self.print_island_status(island, player_own_island)

        print('-------------------')

    def print_islands_status(self):
        print(f'*** Islands status (turn {self.game_api.num_turn}): ***')
        for island in self.game_api.islands:

            # check if island is captured and print island status accordingly
            if island.own_player_id == -1:
                player_own_island = 'no one'
            else:
                player_own_island = self.game_api.players[island.own_player_id].player_name
            self.print_island_status(island, player_own_island)
        print('-------------------')

    def print_island_status(self, island, player_own_island):
        # check if there are ships in island, if there is get player name
        if island.ships:
            island_ship_player_name = self.game_api.players[island.ships[0].player_id].player_name
            island_ship_player_name = f' of {island_ship_player_name}'
        else:
            island_ship_player_name = ''

        # Print island status
        print(f'Island in {island.location} '
              f'is owned by {player_own_island} and has '
              f'{island.current_life} HP and '
              f'{len(island.ships)} ships{island_ship_player_name}.')

    def init_board(self):
        # Init board with 'Sea' tiles
        for i in range(self.game_api.board_size):
            self.game_api.board.append([])
            for j in range(self.game_api.board_size):
                self.game_api.board[i].append('Sea')

        # Add blocks
        for block_id, block in enumerate(self.game_api.blocks):
            block.assign_id(block_id)
            self.game_api.board[block.location[0]][block.location[1]] = block

        # Add islands
        for island_id, island in enumerate(self.game_api.islands):
            island.assign_id(island_id)
            self.game_api.board[island.location[0]][island.location[1]] = island

        # Update players
        for player in self.game_api.players:
            # Get params
            player_base_island_index = self.game_api.players_base_islands_indices[player.player_id]
            player_base_island = self.game_api.islands[player_base_island_index]
            player_num_ships = self.game_api.players_num_ships[player.player_id]
            player_ship_speed = self.game_api.players_ship_speed[player.player_id]

            # Update player base island
            player_base_island.frontend_obj.change_to_player_color(player.player_id)
            player_base_island.own_player_id = player.player_id
            for ship_id in range(player_num_ships):
                player_base_island.add_ship(Ship(ship_id=ship_id,
                                                 player_id=player.player_id,
                                                 ship_speed=player_ship_speed,
                                                 location=player_base_island.location
                                                 ))
            # Update player ships
            player.ships = list(player_base_island.ships)
            player.max_ship_id = len(player.ships) - 1

    def draw_all_sprites(self):
        # Update all sprites from board
        for i in range(self.game_api.board_size):
            for j in range(self.game_api.board_size):
                if self.game_api.board[i][j] != 'Sea':
                    current_obj = self.game_api.board[i][j]
                    self.all_sprites.add(current_obj.frontend_obj)

        # Draw all sprites on screen
        self.screen.fill(utils.COLORS_DICT['Sea'])
        for sprite in self.all_sprites:
            sprite.draw_sprite(location=sprite.location,
                               board_size=self.game_api.board_size,
                               screen=self.screen)

        # print players status on screen
        for player in self.game_api.players:
            num_owned_islands = len(self.game_api.get_islands_info(player_id=player.player_id))
            num_ships = len(player.ships)
            text = f'{player.player_name}: {num_owned_islands} islands, {num_ships} ships'
            text_location = np.array([0, 0]) + player.player_id * np.array([0, self.player_font_size])
            text__color = utils.COLORS_DICT['Player'][player.player_id]
            self.print_text(font_obj=self.player_font_obj, text=text, frontend_location=text_location,
                            color=text__color)

        # print game progress on screen
        num_players = len(self.game_api.players)
        text = f'Turn: {self.game_api.num_turn} / {self.max_num_turns} ' \
               f'({round(self.game_api.num_turn / self.max_num_turns * 100)}%)'
        text_location = np.array([0, 0]) + num_players * np.array([0, self.player_font_size])
        text_color = utils.COLORS_DICT['Island']
        self.print_text(font_obj=self.player_font_obj, text=text, frontend_location=text_location,
                        color=text_color)

        # print islands status on screen
        for island in self.game_api.islands:
            # island life
            text = f'Life: {island.current_life}'
            text_location = np.array(island.frontend_obj.frontend_location) + np.array([100, 20])
            if island.own_player_id == -1:
                text_color = utils.COLORS_DICT['Island']
            else:
                text_color = utils.COLORS_DICT['Player'][island.own_player_id]
            self.print_text(font_obj=self.island_font_obj, text=text, frontend_location=text_location,
                            color=text_color)

            # island timer
            text = f'Timer: {island.timer}'
            text_location = text_location + np.array([0, self.island_font_size])
            if island.own_player_id == -1:
                text_color = utils.COLORS_DICT['Island']
            else:
                text_color = utils.COLORS_DICT['Player'][island.own_player_id]
            self.print_text(font_obj=self.island_font_obj, text=text, frontend_location=text_location,
                            color=text_color)

            # island ships
            text = f'Ships: {len(island.ships)}'
            text_location = text_location + np.array([0, self.island_font_size])
            if island.ships:
                text_color = utils.COLORS_DICT['Player'][island.ships[0].player_id]
            else:
                text_color = utils.COLORS_DICT['Island']
            self.print_text(font_obj=self.island_font_obj, text=text, frontend_location=text_location,
                            color=text_color)

        pg.display.flip()

    def print_text(self, font_obj, text, frontend_location, color):
        text_surface = font_obj.render(text, True, color)
        self.screen.blit(text_surface, frontend_location)

    def print_result(self, player):
        if isinstance(player, Player):
            text = f"{player.player_name} won!"
            text_color = utils.COLORS_DICT['Player'][player.player_id]
        else:
            text = "Draw!"
            text_color = utils.COLORS_DICT['Island']

        text_width, text_height = self.player_won_font_obj.size(text)
        text_location = [utils.SCREEN_WIDTH // 2 - text_width // 2,
                         utils.SCREEN_HEIGHT // 2 - text_height // 2]

        self.print_text(font_obj=self.player_won_font_obj, text=text,
                        frontend_location=text_location, color=text_color)
        pg.display.flip()

    def update_islands(self):
        for island in self.game_api.islands:
            # Add/decrease life to island with ships
            if island.ships:
                island_ships_player_id = island.ships[0].player_id
                num_island_ships = len(island.ships)
                if island.own_player_id == island_ships_player_id:
                    island.current_life += num_island_ships
                else:
                    island.current_life -= num_island_ships

            # Island neutralized
            if island.current_life == 0:
                island.own_player_id = -1
                island.frontend_obj.change_to_neutral_color()
                island.timer = island.ship_creation_time  # reset timer

            # Island captured
            elif island.current_life < 0:
                island.own_player_id = island_ships_player_id
                island.frontend_obj.change_to_player_color(island.own_player_id)
                island.current_life = -island.current_life
                island.timer = island.ship_creation_time  # reset timer

            # Create ships on island
            if island.own_player_id != -1:
                # decrease timer
                island.timer -= 1

                # create new ship when timer reached zero and reset timer
                if island.timer == 0:
                    # create new ship
                    if island.ships:
                        island_ships_player_id = island.ships[0].player_id

                        # friendly ships on island
                        if island.own_player_id == island_ships_player_id:
                            self.create_ship_on_island(island)

                        # enemy ships on island
                        else:
                            self.kill_ship_on_island(ship=island.ships[0], island=island)
                    else:
                        self.create_ship_on_island(island)

                    # reset timer
                    island.timer = island.ship_creation_time

    def create_ship_on_island(self, island):
        player = self.game_api.players[island.own_player_id]
        new_ship = Ship(player_id=island.own_player_id,
                        ship_id=player.max_ship_id + 1,
                        ship_speed=self.game_api.players_ship_speed[island.own_player_id],
                        location=island.location)
        island.add_ship(new_ship)
        player.add_ship(new_ship)
        print(f'New ship of {player.player_name} created on island in {island.location}.')

    def kill_ship_on_island(self, ship, island):
        player = self.game_api.players[ship.player_id]
        island.remove_ship(ship)
        player.remove_ship(ship)
        print(f'Ship of {player.player_name} destroyed on island in {island.location}.')

    def reset_ships_is_moved(self):
        for player in self.game_api.players:
            for ship in player.ships:
                ship.is_moved = False

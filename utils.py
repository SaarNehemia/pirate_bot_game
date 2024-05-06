import pygame as pg

DIRECTION_DICT = {'N': (0, 1),
                  'S': (0, -1),
                  'W': (-1, 0),
                  'E': (1, 0)}

COLORS_DICT = {'Sea': (170, 255, 245),  # Light blue
               'Block': (0, 0, 0),  # Black
               'Island': (208, 130, 40),  # Brown
               'Player': [(200, 200, 200), (100, 100, 100)],  # Gray, Dark gray
               }

SIZE_DICT = {'Block': (10, 10),
             'Island': (50, 50),
             'Player': (25, 25),
             }

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class FrontEndObj(pg.sprite.Sprite):
    def __init__(self, name, **kwargs):
        super(FrontEndObj, self).__init__()
        self.name = name
        self.surf = pg.Surface(SIZE_DICT[name])
        if 'player_id' in kwargs.keys():  # For Ship
            player_id = kwargs['player_id']
            self.surf.fill(COLORS_DICT[name][player_id])
        else:  # For Block and Island
            self.surf.fill(COLORS_DICT[name])
        self.rect = self.surf.get_rect()
        self.frontend_location = (0, 0)

    def draw_sprite(self, screen, location, board_size):
        width_board_size = SCREEN_WIDTH / board_size
        height_board_size = SCREEN_HEIGHT / board_size
        self.frontend_location = (location[0] * width_board_size,
                                  location[1] * height_board_size)
        screen.blit(self.surf, self.frontend_location)
        pass

    def change_to_player_color(self, player_id):
        """ Change to player color once conquered by a player"""
        player_color = COLORS_DICT['Player'][player_id]
        self.surf.fill(player_color)

    def change_to_specific_color(self, color_name):
        """ Change to specific color"""
        self.surf.fill(COLORS_DICT[color_name])

    def change_to_default_color(self):
        """ Change back to specific color"""
        self.surf.fill(COLORS_DICT[self.name])

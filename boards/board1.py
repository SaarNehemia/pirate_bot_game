import numpy as np

from classes.block import Block
from classes.island import Island

board_params = {'board_size': 5,
                'blocks': [Block(location=(1, 1),
                                 current_life=np.inf),
                           Block(location=(1, 2),
                                 current_life=np.inf),
                           Block(location=(1, 3),
                                 current_life=np.inf),
                           ],
                'islands': [Island(location=(2, 2),
                                   current_life=4,
                                   ship_creation_time=2),
                            Island(location=(3, 3),
                                   current_life=2,
                                   ship_creation_time=2),
                            ],
                'max_num_players': 2,
                'players_base_islands_indices': [0, 1],
                'players_ship_speed': [1, 1],
                'players_num_ships': [5, 5],
                }

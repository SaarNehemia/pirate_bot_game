import numpy as np

from classes.block import Block
from classes.island import Island


def get_board_settings():
    return {'board_size': 500,
            'blocks': [Block(location=(100, 100),
                             current_life=np.inf),
                       Block(location=(100, 200),
                             current_life=np.inf),
                       Block(location=(100, 300),
                             current_life=np.inf),
                       ],
            'islands': [Island(location=(200, 200),
                               current_life=4,
                               ship_creation_time=2),
                        Island(location=(300, 300),
                               current_life=2,
                               ship_creation_time=2),
                        ],
            'players_base_islands_indices': [0, 1],
            'players_ship_speed': [1, 1],
            'players_num_ships': [2, 1],
            'victory_criterion': 2,  # num islands which has to be captured to win the game.
            }

import numpy as np
import utils


class Ship:
    def __init__(self, player_id: int, ship_id: int, ship_speed: int, location: np.ndarray):
        self.ship_id = ship_id
        self.player_id = player_id
        self.location = location
        self.ship_speed = ship_speed
        self.is_moved = False
        self.frontend_obj: utils.FrontEndObj = utils.FrontEndObj(name='Player', location=location,
                                                                 player_id=self.player_id)

    def update_location(self, location, board_size):
        new_location = utils.verify_location(location, board_size)
        self.location = new_location
        self.frontend_obj.location = new_location
        self.is_moved = True

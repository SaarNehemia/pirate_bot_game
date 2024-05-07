import pygame as pg
import utils


class Ship:
    def __init__(self, player_id: int, ship_speed: int, location: tuple):
        self.player_id = player_id
        self.ship_speed = ship_speed
        self.location = location
        self.frontend_obj: utils.FrontEndObj = utils.FrontEndObj(name='Player', location=location,
                                                                 player_id=self.player_id)

    def update_location(self, location, board_size):
        new_location = utils.verify_location(location, board_size)
        self.location = new_location
        self.frontend_obj.location = new_location

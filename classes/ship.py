import pygame as pg
import utils


class Ship:
    def __init__(self, player_id: int, ship_speed: int, location: tuple):
        self.player_id = player_id
        self.ship_speed = ship_speed
        self.location = location
        self.frontend_obj = utils.FrontEndObj(name='Player', player_id=self.player_id)

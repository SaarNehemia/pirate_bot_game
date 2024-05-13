import numpy as np

import utils


class Sea:
    def __init__(self, location: np.ndarray):
        self.location = location
        self.frontend_obj: utils.FrontEndObj = utils.FrontEndObj(name='Sea', location=location)
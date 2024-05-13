import numpy as np

import utils


class Block:
    def __init__(self, location: np.ndarray, current_life: int):
        self.block_id = ""
        self.location = location
        self.current_life = current_life  # for future feature: enable block destroy
        self.frontend_obj: utils.FrontEndObj = utils.FrontEndObj(name='Block', location=location)

    def assign_id(self, block_id):
        self.block_id = block_id

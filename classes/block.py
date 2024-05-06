import utils


class Block:
    def __init__(self, location: tuple, current_life: int):
        self.location = location
        self.current_life = current_life  # for future feature: enable block destroy
        self.frontend_obj = utils.FrontEndObj(name='Block')

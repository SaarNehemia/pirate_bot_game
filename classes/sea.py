import utils


class Sea:
    def __init__(self, location: tuple):
        self.location = location
        self.frontend_obj = utils.FrontEndObj(name='Sea')
from ..errors import NotImplemented


class BaseScript:
    def __init__(self) -> None:
        pass

    def run(self):
        raise NotImplemented("Run method is not implemented yet!")

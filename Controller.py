from abc import ABCMeta, abstractmethod
import Game
import pyglet
import Constants


class AbstractController(metaclass=ABCMeta):
    @abstractmethod
    def get_next_move(self):
        raise NotImplementedError


class PlayerController(AbstractController):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.next_move = Constants.SNAKE_MOVE_FORWARD

    def get_next_move(self):
        return self.next_move


class GeneticController(AbstractController):
    def get_next_move(self):
        pass

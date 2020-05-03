from abc import ABCMeta, abstractmethod
import Game
import pyglet

class AbstractController(metaclass=ABCMeta):
    @abstractmethod
    def get_next_move(self):
        raise NotImplementedError


class PlayerController(AbstractController):
    def get_next_move(self):
        return Game.FORWARD


class GeneticController(AbstractController):
    def get_next_move(self):
        pass

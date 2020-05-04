from abc import ABCMeta, abstractmethod
import Game
import Snake
import pyglet
import Constants


class AbstractController(metaclass=ABCMeta):
    pass


class PlayerController(AbstractController):
    def __init__(self, window, game):
        super().__init__()
        self.window = window
        self.game = game
        self.next_move = Constants.SNAKE_MOVE_FORWARD

        pyglet.clock.schedule_interval(self.control, 1/30)

    def control(self, dt):
        self.game.play(self.next_move)

    def on_key_press(self, symbol, modifiers):
        self.next_move = Constants.SNAKE_MOVE_FORWARD



class GeneticController(AbstractController):
    def get_next_move(self):
        pass

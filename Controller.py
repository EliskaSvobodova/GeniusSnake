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

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            direction = Snake.heads_direction(self.game.snake.head)
            if direction is Constants.SNAKE_HEADS_UP:
                self.game.play(Constants.SNAKE_MOVE_FORWARD)
            elif direction is Constants.SNAKE_HEADS_LEFT:
                self.game.play(Constants.SNAKE_MOVE_RIGHT)
            elif direction is Constants.SNAKE_HEADS_RIGHT:
                self.game.play(Constants.SNAKE_MOVE_LEFT)
        if symbol == pyglet.window.key.RIGHT:
            direction = Snake.heads_direction(self.game.snake.head)
            if direction is Constants.SNAKE_HEADS_UP:
                self.game.play(Constants.SNAKE_MOVE_RIGHT)
            elif direction is Constants.SNAKE_HEADS_DOWN:
                self.game.play(Constants.SNAKE_MOVE_LEFT)
            elif direction is Constants.SNAKE_HEADS_RIGHT:
                self.game.play(Constants.SNAKE_MOVE_LEFT)
        if symbol == pyglet.window.key.UP:
            direction = Snake.heads_direction(self.game.snake.head)
            if direction is Constants.SNAKE_HEADS_UP:
                self.game.play(Constants.SNAKE_MOVE_FORWARD)
            elif direction is Constants.SNAKE_HEADS_LEFT:
                self.game.play(Constants.SNAKE_MOVE_RIGHT)
            elif direction is Constants.SNAKE_HEADS_RIGHT:
                self.game.play(Constants.SNAKE_MOVE_LEFT)
        if symbol == pyglet.window.key.UP:
            direction = Snake.heads_direction(self.game.snake.head)
            if direction is Constants.SNAKE_HEADS_UP:
                self.game.play(Constants.SNAKE_MOVE_FORWARD)
            elif direction is Constants.SNAKE_HEADS_LEFT:
                self.game.play(Constants.SNAKE_MOVE_RIGHT)
            elif direction is Constants.SNAKE_HEADS_RIGHT:
                self.game.play(Constants.SNAKE_MOVE_LEFT)



class GeneticController(AbstractController):
    def get_next_move(self):
        pass

from abc import ABCMeta, abstractmethod
import pyglet
import CommonHelpers
import Snake


class AbstractUI(metaclass=ABCMeta):
    def __init__(self, x, y, width, height, square_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.square_size = square_size
        CommonHelpers.configure_resources()

    """ GETTERS """

    @abstractmethod
    def get_num_squares_height(self):
        raise NotImplementedError()

    @abstractmethod
    def get_num_squares_width(self):
        raise NotImplementedError()

    """ DRAWING """

    @abstractmethod
    def prepare_game(self, snake: Snake.Snake):
        raise NotImplementedError

    @abstractmethod
    def draw_snake_eat(self, snake: Snake.Snake):
        raise NotImplementedError

    @abstractmethod
    def draw_snake_move(self, snake: Snake.Snake, prev_tail):
        raise NotImplementedError

    @abstractmethod
    def draw_apple(self, x, y):
        raise NotImplementedError

    @abstractmethod
    def draw_snake(self, snake: Snake.Snake):
        raise NotImplementedError()

    @abstractmethod
    def draw_snake_dead(self, snake: Snake.Snake):
        raise NotImplementedError()

    @abstractmethod
    def draw_game_field(self):
        raise NotImplementedError()

    @abstractmethod
    def draw_square(self, x, y):
        raise NotImplementedError

    @abstractmethod
    def draw_score(self, score):
        raise NotImplementedError()

    @abstractmethod
    def draw_background(self):
        raise NotImplementedError()

    @abstractmethod
    def draw_game_over(self):
        raise NotImplementedError

    @abstractmethod
    def draw_game_won(self):
        raise NotImplementedError

    def draw_boundary(self):
        pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                             ("v2f", (self.x, self.y, self.x, self.y + self.height,
                                      self.x, self.y + self.height, self.x + self.width, self.y + self.height,
                                      self.x + self.width, self.y + self.height, self.x + self.width, self.y,
                                      self.x + self.width, self.y, self.x, self.y)))

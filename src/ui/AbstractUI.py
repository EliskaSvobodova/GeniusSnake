from abc import ABCMeta, abstractmethod
from src import CommonHelpers, Snake, Settings


class AbstractUI(metaclass=ABCMeta):
    def __init__(self, x, y, width, height, square_size):
        self.width = width
        self.height = height
        self.square_size = square_size
        h = Settings.max_game_height if Settings.max_game_height < self.height else self.height
        w = Settings.max_game_width if Settings.max_game_width < self.width else self.width
        self.num_squares_height = (h - self.square_size) // self.square_size
        self.num_squares_width = w // self.square_size
        self.x = x
        self.y = y
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
    def redraw(self, snake: Snake.Snake, score, identification, num_runs, apple):
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

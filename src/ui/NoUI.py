from src import Snake
from src.ui import AbstractUI

"""
UI that doesn't draw anything
"""


class NoUI(AbstractUI.AbstractUI):
    def __init__(self, x, y, width, height, square_size):
        super().__init__(x, y, width, height, square_size, 2)

    def get_num_squares_height(self):
        return self.num_squares_height

    def get_num_squares_width(self):
        return self.num_squares_width

    def prepare_game(self, snake: Snake.Snake):
        pass

    def redraw(self, snake: Snake.Snake, score, identifier, num_runs, apple):
        pass

    def draw_snake_eat(self, snake: Snake.Snake):
        pass

    def draw_snake_move(self, snake: Snake.Snake, prev_tail):
        pass

    def draw_apple(self, x, y):
        pass

    def draw_snake(self, snake: Snake.Snake):
        pass

    def draw_snake_dead(self, snake: Snake.Snake):
        pass

    def draw_game_field(self):
        pass

    def draw_square(self, x, y):
        pass

    def draw_score(self, score):
        pass

    def draw_background(self):
        pass

    def draw_game_over(self):
        pass

    def draw_game_won(self):
        pass

    def draw_snake_shrink(self, snake: Snake.Snake):
        pass

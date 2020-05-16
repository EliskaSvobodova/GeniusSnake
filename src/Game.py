from src import Constants, Snake, Settings
from src.ui import AbstractUI
import random
import numpy as np


class Game:
    def __init__(self, ui: AbstractUI.AbstractUI):
        self.ui = ui
        self.game_field_height = self.ui.get_num_squares_height()
        self.game_field_width = self.ui.get_num_squares_width()
        self.game_field = np.full([self.game_field_height - 2, self.game_field_width - 2], True)
        self.game_field = np.concatenate((np.full([1, self.game_field_width - 2], False),
                                          self.game_field,
                                          np.full([1, self.game_field_width - 2], False)))
        self.game_field = np.concatenate((np.full([self.game_field_height, 1], False),
                                          self.game_field,
                                          np.full([self.game_field_height, 1], False)),
                                         axis=1)

        self.snake = Snake.Snake()
        for part in self.snake:
            self.game_field[part.y][part.x] = False

        self.score = 0
        self.score_max = ((self.game_field_width - 2) * (self.game_field_height - 2)) - self.snake.length
        if Settings.max_score != -1 and Settings.max_score < self.score_max:
            self.score_max = Settings.max_score

        self.prev_apple = tuple([0, 0])
        self.apple = None
        self.put_apple()
        self.game_state = Constants.PLAY

    def make_next_move(self, next_move):
        next_square = self.snake.next_square(next_move, 1)
        if self.game_field[next_square[1]][next_square[0]]:  # there is no obstacle
            if self.apple[0] == next_square[0] and self.apple[1] == next_square[1]:  # there is an apple
                self.prev_apple = self.apple
                self.eat_apple()
            else:
                if not self.move_snake(next_square):
                    self.ui.draw_snake_dead(self.snake)
                    self.ui.draw_game_over()
                    self.game_state = Constants.LOOSE
        else:  # snake bumped into an obstacle
            self.ui.draw_snake_dead(self.snake)
            self.ui.draw_game_over()
            self.game_state = Constants.LOOSE

    def put_apple(self):
        x = random.randint(1, self.game_field_width - 1)
        y = random.randint(1, self.game_field_height - 1)
        while not self.game_field[y][x]:
            x = random.randint(1, self.game_field_width - 1)
            y = random.randint(1, self.game_field_height - 1)
        self.apple = tuple([x, y])
        self.ui.draw_apple(x, y)

    def move_snake(self, next_square):
        self.game_field[next_square[1]][next_square[0]] = False
        self.game_field[self.snake.tail.y][self.snake.tail.x] = True
        prev_tail = tuple([self.snake.tail.x, self.snake.tail.y])
        self.snake.move(next_square)
        self.ui.draw_snake_move(self.snake, prev_tail)
        if self.snake.without_food == self.snake.stamina:
            return False  # snake starved to death
        return True

    def eat_apple(self):
        self.game_field[self.apple[1]][self.apple[0]] = False
        self.snake.eat_apple(self.apple)
        self.ui.draw_snake_eat(self.snake)
        self.score += 1
        self.ui.draw_score(self.score)
        if self.score == self.score_max:
            self.ui.draw_game_won()
            self.game_state = Constants.WIN
        else:
            self.put_apple()

    def just_eaten_apple(self):
        return self.snake.head.next_n.x == self.prev_apple[0] and self.snake.head.next_n.y == self.prev_apple[1]

    def get_move_from_direction(self, direction):
        snake_heads = Snake.heads_direction(self.snake.head)
        if (snake_heads is Constants.UP and direction is Constants.LEFT) \
                or (snake_heads is Constants.RIGHT and direction is Constants.UP) \
                or (snake_heads is Constants.DOWN and direction is Constants.RIGHT) \
                or (snake_heads is Constants.LEFT and direction is Constants.DOWN):
            return Constants.SNAKE_MOVE_LEFT
        elif (snake_heads is Constants.UP and direction is Constants.RIGHT) \
                or (snake_heads is Constants.RIGHT and direction is Constants.DOWN) \
                or (snake_heads is Constants.DOWN and direction is Constants.LEFT) \
                or (snake_heads is Constants.LEFT and direction is Constants.UP):
            return Constants.SNAKE_MOVE_RIGHT
        else:
            return Constants.SNAKE_MOVE_FORWARD

    def get_move_from_next_square(self, next_square):
        if next_square[0] < self.snake.head.x:
            return self.get_move_from_direction(Constants.LEFT)
        if next_square[0] > self.snake.head.x:
            return self.get_move_from_direction(Constants.RIGHT)
        if next_square[1] < self.snake.head.y:
            return self.get_move_from_direction(Constants.DOWN)
        if next_square[1] > self.snake.head.y:
            return self.get_move_from_direction(Constants.UP)
        raise ValueError("Cannot get move from snake's head")

    def redraw(self, identification, num_runs):
        self.ui.redraw(self.snake, self.score,
                       identification, num_runs, self.apple)


def is_wall(game, next_square):
    if next_square[0] == 0 or next_square[0] == game.game_field_width - 1 \
            or next_square[1] == 0 or next_square[1] == game.game_field_height - 1:
        return True
    else:
        return False


""" Functions for genetic programming """


def if_food_forward(game, yes, no):
    snake_heads = Snake.heads_direction(game.snake.head)
    if snake_heads is Constants.UP:
        if game.apple[1] > game.snake.head.y:
            return yes
        else:
            return no
    if snake_heads is Constants.RIGHT:
        if game.apple[0] > game.snake.head.x:
            return yes
        else:
            return no
    if snake_heads is Constants.DOWN:
        if game.apple[1] < game.snake.head.y:
            return yes
        else:
            return no
    if snake_heads is Constants.LEFT:
        if game.apple[0] < game.snake.head.x:
            return yes
        else:
            return no


def if_food_left(game, yes, no):
    snake_heads = Snake.heads_direction(game.snake.head)
    if snake_heads is Constants.UP:
        if game.apple[1] == game.snake.head.y and game.apple[0] < game.snake.head.x:
            return yes
        else:
            return no
    if snake_heads is Constants.RIGHT:
        if game.apple[0] == game.snake.head.x and game.apple[1] > game.snake.head.y:
            return yes
        else:
            return no
    if snake_heads is Constants.DOWN:
        if game.apple[1] == game.snake.head.y and game.apple[0] > game.snake.head.x:
            return yes
        else:
            return no
    if snake_heads is Constants.LEFT:
        if game.apple[0] == game.snake.head.x and game.apple[1] < game.snake.head.y:
            return yes
        else:
            return no


def if_food_right(game, yes, no):
    snake_heads = Snake.heads_direction(game.snake.head)
    if snake_heads is Constants.UP:
        if game.apple[1] == game.snake.head.y and game.apple[0] > game.snake.head.x:
            return yes
        else:
            return no
    if snake_heads is Constants.RIGHT:
        if game.apple[0] == game.snake.head.x and game.apple[1] < game.snake.head.y:
            return yes
        else:
            return no
    if snake_heads is Constants.DOWN:
        if game.apple[1] == game.snake.head.y and game.apple[0] < game.snake.head.x:
            return yes
        else:
            return no
    if snake_heads is Constants.LEFT:
        if game.apple[0] == game.snake.head.x and game.apple[1] > game.snake.head.y:
            return yes
        else:
            return no


def if_wall_forward(game, yes, no):
    next_square = game.snake.next_square(Constants.SNAKE_MOVE_FORWARD, 1)
    if is_wall(game, next_square):
        return yes
    else:
        return no


def if_wall_left(game, yes, no):
    next_square = game.snake.next_square(Constants.SNAKE_MOVE_LEFT, 1)
    if is_wall(game, next_square):
        return yes
    else:
        return no


def if_wall_right(game, yes, no):
    next_square = game.snake.next_square(Constants.SNAKE_MOVE_RIGHT, 1)
    if is_wall(game, next_square):
        return yes
    else:
        return no


def if_body_forward(game, yes, no):
    next_square = game.snake.next_square(Constants.SNAKE_MOVE_FORWARD, 1)
    if not game.game_field[next_square[1]][next_square[0]] and not is_wall(game, next_square):
        return yes
    else:
        return no


def if_body_left(game, yes, no):
    next_square = game.snake.next_square(Constants.SNAKE_MOVE_LEFT, 1)
    if not game.game_field[next_square[1]][next_square[0]] and not is_wall(game, next_square):
        return yes
    else:
        return no


def if_body_right(game, yes, no):
    next_square = game.snake.next_square(Constants.SNAKE_MOVE_RIGHT, 1)
    if not game.game_field[next_square[1]][next_square[0]] and not is_wall(game, next_square):
        return yes
    else:
        return no


def if_obstacle_two_forward(game, yes, no):
    next_next_square = game.snake.next_square(Constants.SNAKE_MOVE_FORWARD, 2)
    if next_next_square[0] < 0 or next_next_square[0] > game.game_field_width - 1 \
            or next_next_square[1] < 0 or next_next_square[1] > game.game_field_height - 1 \
            or not game.game_field[next_next_square[1]][next_next_square[0]]:
        return yes
    else:
        return no


def if_is_moving_up(game, yes, no):
    if Snake.heads_direction(game.snake.head) is Constants.UP:
        return yes
    else:
        return no


def if_is_moving_left(game, yes, no):
    if Snake.heads_direction(game.snake.head) is Constants.UP:
        return yes
    else:
        return no

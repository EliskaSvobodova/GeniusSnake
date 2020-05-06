import Game
import Constants
import random
import pyglet

max_depth = 10


class GeneticController:
    def __init__(self, game: Game.Game, root=None):
        self.game = game
        if root is None:
            self.root = generate_tree(0, self.game)
        else:
            self.root = root
        self.state = Constants.PLAY
        pyglet.clock.schedule_interval(self.play_on_tic, 1/3)

    def play(self):
        if callable(self.root):
            while self.game.game_state is Constants.PLAY:
                self.game.make_next_move(self.root())
        else:  # root is a terminal
            while self.game.game_state is Constants.PLAY:
                self.game.make_next_move(self.root)

    def play_on_tic(self, dt):
        if callable(self.root):
            self.game.make_next_move(self.root())
        else:  # root is a terminal
            self.game.make_next_move(self.root)
        self.state = self.game.game_state


def generate_tree(depth, game):
    if depth == max_depth:
        return get_random_terminal()
    if random.random() < 0.5:
        fnc = get_random_function(game)
        return fnc(generate_tree(depth + 1, game), generate_tree(depth + 1, game))
    else:
        return get_random_terminal()


def get_random_terminal():
    return random.choice([Constants.SNAKE_MOVE_RIGHT, Constants.SNAKE_MOVE_LEFT, Constants.SNAKE_MOVE_FORWARD])


def get_random_function(game):
    return random.choice([game.if_food_forward, game.if_food_left, game.if_food_right,
                          game.if_obstacle_forward, game.if_obstacle_left, game.if_obstacle_right])

import Game
import Constants
import random
import pyglet

max_depth = 10


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            return self.value(self.left(), self.right())
        else:
            return self.value


class GeneticController:
    def __init__(self, game: Game.Game, root=None):
        self.game = game
        if root is None:
            self.root = generate_tree(0, self.game)
        else:
            self.root = root
        self.state = Constants.PLAY
        pyglet.clock.schedule_interval(self.play_on_tic, 1 / 15)

    def play_on_tic(self, dt):
        move = self.root()
        self.game.make_next_move(move)
        self.state = self.game.game_state
        if self.state is not Constants.PLAY:
            pyglet.clock.unschedule(self.play_on_tic)


def generate_tree(depth, game):
    if depth == max_depth:
        return get_random_terminal()
    if random.random() < 0.5:
        fnc = get_random_function(game)
        fnc.left = generate_tree(depth + 1, game)
        fnc.right = generate_tree(depth + 1, game)
        return fnc
    else:
        return get_random_terminal()


def generate_test_tree(game):
    return TreeNode(game.if_obstacle_forward, TreeNode(Constants.SNAKE_MOVE_LEFT), TreeNode(Constants.SNAKE_MOVE_FORWARD))


def get_random_terminal():
    terminal = random.choice([Constants.SNAKE_MOVE_RIGHT, Constants.SNAKE_MOVE_LEFT, Constants.SNAKE_MOVE_FORWARD])
    return TreeNode(terminal)


def get_random_function(game):
    choice = random.choice(range(6))
    if choice == 0:
        fnc = game.if_food_forward
    elif choice == 1:
        fnc = game.if_food_left
    elif choice == 2:
        fnc = game.if_food_right
    elif choice == 3:
        fnc = game.if_obstacle_forward
    elif choice == 4:
        fnc = game.if_obstacle_left
    else:
        fnc = game.if_obstacle_right
    return TreeNode(fnc)

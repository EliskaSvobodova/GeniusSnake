from src import Constants, Game, Settings
from src.ui import NoUI
import numpy as np


def test_game():
    Settings.snake_start_length = 5
    Settings.max_score = 1000  # too much, game should adjust it to maximal value according to size of game field
    # height 11, one additional square for score area
    game = Game.Game(NoUI.NoUI(100, 100, 10, 11, 1))
    correct_field = np.array([[False, False, False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, False, False, False, False, False, False, False, False, False]])
    assert np.array_equal(correct_field, game.game_field)
    assert (game.score_max == 59)
    assert (0 < game.apple[0] < 10 and 0 < game.apple[1] < 11)


def test_make_next_move():
    Settings.snake_start_length = 5
    game = Game.Game(NoUI.NoUI(100, 100, 10, 11, 1))
    game.apple = tuple([6, 3])
    game.make_next_move(Constants.SNAKE_MOVE_FORWARD)
    correct_field = np.array([[False, False, False, False, False, False, False, False, False, False],
                              [False, True,  False, False, False, False, False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, False, False, False, False, False, False, False, False, False]])
    assert np.array_equal(correct_field, game.game_field)
    assert game.game_state is Constants.PLAY

    game.make_next_move(Constants.SNAKE_MOVE_LEFT)
    correct_field = np.array([[False, False, False, False, False, False, False, False, False, False],
                              [False, True,  True,  False, False, False, False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, False, False, False, False, False, False, False, False, False]])
    assert np.array_equal(correct_field, game.game_field)
    assert game.game_state is Constants.PLAY

    game.make_next_move(Constants.SNAKE_MOVE_FORWARD)
    correct_field = np.array([[False, False, False, False, False, False, False, False, False, False],
                              [False, True,  True,  False, False, False, False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, False, False, False, False, False, False, False, False, False]])
    assert np.array_equal(correct_field, game.game_field)
    assert game.apple != tuple([6, 3])
    game.apple = tuple([0, 0])  # off the field so it is not eaten accidentally
    assert game.game_state is Constants.PLAY

    correct_field = np.array([[False, False, False, False, False, False, False, False, False, False],
                              [False, True,  True,  True,  False, False, False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, False, True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, False, False, False, False, False, False, False, False, False]])
    game.make_next_move(Constants.SNAKE_MOVE_RIGHT)
    assert np.array_equal(correct_field, game.game_field)
    assert game.game_state is Constants.PLAY

    game.make_next_move(Constants.SNAKE_MOVE_FORWARD)
    correct_field = np.array([[False, False, False, False, False, False, False, False, False, False],
                              [False, True,  True,  True,  True,  False, False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, False, False, False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, False, False, False, False, False, False, False, False, False]])
    assert np.array_equal(correct_field, game.game_field)
    assert game.game_state is Constants.PLAY

    game.make_next_move(Constants.SNAKE_MOVE_FORWARD)
    correct_field = np.array([[False, False, False, False, False, False, False, False, False, False],
                              [False, True,  True,  True,  True,  False, False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, True,  True,  False],
                              [False, True,  True,  True,  True,  True,  False, False, False, False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, True,  True,  True,  True,  True,  True,  True,  True,  False],
                              [False, False, False, False, False, False, False, False, False, False]])
    assert np.array_equal(correct_field, game.game_field)
    assert game.game_state is Constants.LOOSE


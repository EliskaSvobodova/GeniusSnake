from src import Constants, Settings
import numpy as np
import pyglet


class HamiltonController:
    def __init__(self, game):
        self.game = game
        self.game.snake.stamina = 1000
        self.state = Constants.PLAY
        self.field = np.full([self.game.game_field_height - 2, self.game.game_field_width - 2], Constants.FREE)
        self.field = np.concatenate((np.full([1, self.game.game_field_width - 2], Constants.BUSH),
                                     self.field,
                                     np.full([1, self.game.game_field_width - 2], Constants.BUSH)))
        self.field = np.concatenate((np.full([self.game.game_field_height, 1], Constants.BUSH),
                                     self.field,
                                     np.full([self.game.game_field_height, 1], Constants.BUSH)),
                                    axis=1)
        for part in self.game.snake:
            self.field[part.y][part.x] = Constants.RIGHT
        self.mark_smallest_cycle()
        self.mark_hamiltonian_cycle()
        pyglet.clock.schedule_interval(self.control, Settings.hamilton_snake_speed)

    def control(self, dt):
        next_move = self.game.get_move_from_direction(self.field[self.game.snake.head.y][self.game.snake.head.x])
        self.game.make_next_move(next_move)
        if self.game.game_state is Constants.WIN:
            pyglet.clock.unschedule(self.control)
            self.state = Constants.WIN
        elif self.game.game_state is Constants.LOOSE:
            pyglet.clock.unschedule(self.control)
            self.state = Constants.LOOSE

    def mark_smallest_cycle(self):
        cur_x = self.game.snake.head.x
        cur_y = self.game.snake.head.y
        self.field[cur_y][cur_x] = Constants.UP
        cur_y += 1
        while cur_x > 1:
            self.field[cur_y][cur_x] = Constants.LEFT
            cur_x -= 1
        self.field[cur_y][cur_x] = Constants.DOWN

    def mark_hamiltonian_cycle(self):
        cur_x = self.game.snake.head.x
        cur_y = self.game.snake.head.y
        while cur_x != self.game.snake.tail.x or cur_y != self.game.snake.tail.y:
            if self.field[cur_y][cur_x] == Constants.UP:
                if self.field[cur_y][cur_x + 1] == Constants.FREE \
                        and self.field[cur_y + 1][cur_x + 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.RIGHT
                    self.field[cur_y][cur_x + 1] = Constants.UP
                    self.field[cur_y + 1][cur_x + 1] = Constants.LEFT
                    cur_x += 1
                    continue
                if self.field[cur_y][cur_x - 1] == Constants.FREE \
                        and self.field[cur_y + 1][cur_x - 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.LEFT
                    self.field[cur_y][cur_x - 1] = Constants.UP
                    self.field[cur_y + 1][cur_x - 1] = Constants.RIGHT
                    cur_x -= 1
                    continue
                cur_y += 1
            elif self.field[cur_y][cur_x] == Constants.DOWN:
                if self.field[cur_y][cur_x - 1] == Constants.FREE \
                        and self.field[cur_y - 1][cur_x - 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.LEFT
                    self.field[cur_y][cur_x - 1] = Constants.DOWN
                    self.field[cur_y - 1][cur_x - 1] = Constants.RIGHT
                    cur_x -= 1
                    continue
                if self.field[cur_y][cur_x + 1] == Constants.FREE \
                        and self.field[cur_y - 1][cur_x + 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.RIGHT
                    self.field[cur_y][cur_x + 1] = Constants.DOWN
                    self.field[cur_y - 1][cur_x + 1] = Constants.LEFT
                    cur_x += 1
                    continue
                cur_y -= 1
            elif self.field[cur_y][cur_x] == Constants.LEFT:
                if self.field[cur_y + 1][cur_x] == Constants.FREE \
                        and self.field[cur_y + 1][cur_x - 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.UP
                    self.field[cur_y + 1][cur_x] = Constants.LEFT
                    self.field[cur_y + 1][cur_x - 1] = Constants.DOWN
                    cur_y += 1
                    continue
                if self.field[cur_y - 1][cur_x] == Constants.FREE \
                        and self.field[cur_y - 1][cur_x - 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.DOWN
                    self.field[cur_y - 1][cur_x] = Constants.LEFT
                    self.field[cur_y - 1][cur_x - 1] = Constants.UP
                    cur_y -= 1
                    continue
                cur_x -= 1
            elif self.field[cur_y][cur_x] == Constants.RIGHT:
                if self.field[cur_y + 1][cur_x] == Constants.FREE \
                        and self.field[cur_y + 1][cur_x + 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.UP
                    self.field[cur_y + 1][cur_x] = Constants.RIGHT
                    self.field[cur_y + 1][cur_x + 1] = Constants.DOWN
                    cur_y += 1
                    continue
                if self.field[cur_y - 1][cur_x] == Constants.FREE \
                        and self.field[cur_y - 1][cur_x + 1] == Constants.FREE:
                    self.field[cur_y][cur_x] = Constants.DOWN
                    self.field[cur_y - 1][cur_x] = Constants.RIGHT
                    self.field[cur_y - 1][cur_x + 1] = Constants.UP
                    cur_y -= 1
                    continue
                cur_x += 1

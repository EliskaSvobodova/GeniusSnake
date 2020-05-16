from src import Constants, Settings
import pyglet
import heapq
import math
import random
import numpy as np

OPEN = 0
CLOSED = 1


class Tile:
    def __init__(self, path_length, distance, x, y, parent=None):
        self.path_length = path_length
        self.distance = distance
        self.x = x
        self.y = y
        self.parent = parent
        self.state = OPEN


class QueueElement:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return True  # so that all tuples in queue are compared just according to first value


class AStarController:
    def __init__(self, game):
        self.game = game
        self.speed = Settings.a_star_snake_speed
        self.state = Constants.PLAY
        self.queue = []
        self.field = None
        pyglet.clock.schedule_interval(self.control, self.speed)

    def control(self, dt):
        next_move = self.decide_next_move()
        self.game.make_next_move(next_move)
        if self.game.game_state is Constants.WIN:
            pyglet.clock.unschedule(self.control)
            self.state = Constants.WIN
        elif self.game.game_state is Constants.LOOSE:
            pyglet.clock.unschedule(self.control)
            self.state = Constants.LOOSE

    def decide_next_move(self):
        self.queue = []
        dist_to_apple = self.calculate_distance(self.game.snake.head.x, self.game.snake.head.y)
        head_tile = Tile(0, dist_to_apple, self.game.snake.head.x, self.game.snake.head.y)
        head_element = QueueElement(self.game.snake.head.x, self.game.snake.head.y)
        self.field = np.array(self.game.game_field, dtype="O")
        self.field[self.game.snake.head.y][self.game.snake.head.x] = head_tile
        heapq.heappush(self.queue, (head_tile.path_length + head_tile.distance, head_element))
        while self.queue:
            dummy, el = heapq.heappop(self.queue)
            if isinstance(self.field[el.y][el.x], Tile) and self.field[el.y][el.x].state == CLOSED:
                continue
            if el.x == self.game.apple[0] and el.y == self.game.apple[1]:
                next_square = self.backtrack_to_head_next()
                move = self.game.get_move_from_next_square(next_square)
                return move
            self.check(el, +1, 0)
            self.check(el, -1, 0)
            self.check(el, 0, +1)
            self.check(el, 0, -1)
            self.field[el.y][el.x].state = CLOSED
        # there is currently no available way, take random step
        available = [Constants.SNAKE_MOVE_FORWARD, Constants.SNAKE_MOVE_LEFT, Constants.SNAKE_MOVE_RIGHT]
        while True:
            if len(available) == 0:
                # there is no free tile, snake will die no matter in which direction it continues
                return Constants.SNAKE_MOVE_FORWARD
            move = random.choice(available)
            next_square = self.game.snake.next_square(move, 1)
            if self.game.game_field[next_square[1]][next_square[0]]:
                return self.game.get_move_from_next_square(next_square)
            available.remove(move)

    def check(self, el, pl_x, pl_y):
        if isinstance(self.field[el.y + pl_y][el.x + pl_x], Tile):
            if self.field[el.y + pl_y][el.x + pl_x].path_length > self.field[el.y][el.x].path_length + 1:
                self.field[el.y + pl_y][el.x + pl_x].path_length = self.field[el.y][el.x].path_length + 1
                self.field[el.y + pl_y][el.x + pl_x].parent = el
                heapq.heappush(self.queue,
                               (self.field[el.y + pl_y][el.x + pl_x].path_length
                                + self.field[el.y + pl_y][el.x + pl_x].distance,
                                QueueElement(el.x + pl_x, el.y + pl_y)))
        elif self.field[el.y + pl_y][el.x + pl_x]:
            self.field[el.y + pl_y][el.x + pl_x] = Tile(self.field[el.y][el.x].path_length + 1,
                                                        self.calculate_distance(el.x + pl_x, el.y + pl_y),
                                                        el.x + pl_x, el.y + pl_y,
                                                        el)
            heapq.heappush(self.queue,
                           (self.field[el.y + pl_y][el.x + pl_x].path_length
                            + self.field[el.y + pl_y][el.x + pl_x].distance,
                            QueueElement(el.x + pl_x, el.y + pl_y)))

    def backtrack_to_head_next(self):
        current = self.field[self.game.apple[1]][self.game.apple[0]]
        while current.parent.x != self.game.snake.head.x or current.parent.y != self.game.snake.head.y:
            current = self.field[current.parent.y][current.parent.x]
        return tuple([current.x, current.y])

    def calculate_distance(self, x, y):
        """ Manhattan distance """
        a_x = x if x > self.game.apple[0] else self.game.apple[0]
        b_x = x if x <= self.game.apple[0] else self.game.apple[0]
        a_y = y if y > self.game.apple[1] else self.game.apple[1]
        b_y = y if y <= self.game.apple[1] else self.game.apple[1]

        return (a_x - b_x) + (a_y - b_y)

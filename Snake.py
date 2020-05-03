import Game

class Node:
    def __init__(self, x, y, next_n=None, prev_n=None):
        self.x = x
        self.y = y
        self.next_n = next_n
        self.prev_n = prev_n


class SnakeIterator:
    def __init__(self, snake):
        self.snake_part = snake.head

    def __next__(self):
        if self.snake_part is not None:
            current = self.snake_part
            self.snake_part = self.snake_part.next_n
            return current
        else:
            raise StopIteration


"""
Direction constants
"""
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

"""
For head and body
"""
def heads_direction(node: Node):
    if node.next_n.x < node.x:
        return RIGHT
    if node.x < node.next_n.x:
        return LEFT
    if node.next_n.y < node.y:
        return UP
    if node.y < node.next_n.y:
        return DOWN

"""
For tail,  where rest of the body is
"""
def rest_direction(node: Node):
    if node.prev_n.x < node.x:
        return LEFT
    if node.x < node.prev_n.x:
        return RIGHT
    if node.prev_n.y < node.y:
        return DOWN
    if node.y < node.prev_n.y:
        return UP


"""
For corner
"""
def corner_type(node: Node) -> tuple:
    if (node.x < node.prev_n.x and node.y > node.next_n.y) or (node.x < node.next_n.x and node.y > node.prev_n.y):
        return tuple([DOWN, RIGHT])
    if (node.x > node.prev_n.x and node.y > node.next_n.y) or (node.x > node.next_n.x and node.y > node.prev_n.y):
        return tuple([DOWN, LEFT])
    if (node.x > node.prev_n.x and node.y < node.next_n.y) or (node.x > node.next_n.x and node.y < node.prev_n.y):
        return tuple([UP, LEFT])
    if (node.x < node.prev_n.x and node.y < node.next_n.y) or (node.x < node.next_n.x and node.y < node.prev_n.y):
        return tuple([UP, RIGHT])


def is_head(node: Node):
    return node.prev_n is None


def is_tail(node: Node):
    return node.next_n is None


def is_body(node: Node):
    return (node.next_n is not None and node.prev_n is not None) \
           and (node.prev_n.x == node.next_n.x or node.prev_n.y == node.next_n.y)


def is_corner(node: Node):
    return (node.next_n is not None and node.prev_n is not None) \
           and (node.prev_n.x != node.next_n.x or node.prev_n.y != node.next_n.y)


class Snake:
    def __init__(self):
        self.head = Node(3, 1)
        self.head.next_n = Node(2, 1, prev_n=self.head)
        self.tail = Node(1, 1, prev_n=self.head.next_n)
        self.head.next_n.next_n = self.tail

    def __iter__(self):
        return SnakeIterator(self)

    def next_square(self, next_move):
        direction = heads_direction(self.head)
        if (direction is UP and next_move is Game.FORWARD) \
                or (direction is RIGHT and next_move is Game.LEFT) \
                or (direction is LEFT and next_move is Game.RIGHT):
            return tuple([self.head.x, self.head.y + 1])
        if (direction is UP and next_move is Game.RIGHT) \
                or (direction is RIGHT and next_move is Game.FORWARD) \
                or (direction is DOWN and next_move is Game.LEFT):
            return tuple([self.head.x + 1, self.head.y])
        if (direction is RIGHT and next_move is Game.RIGHT) \
                or (direction is DOWN and next_move is Game.FORWARD) \
                or (direction is LEFT and next_move is Game.LEFT):
            return tuple([self.head.x, self.head.y - 1])
        if (direction is UP and next_move is Game.LEFT) \
                or (direction is DOWN and next_move is Game.RIGHT) \
                or (direction is LEFT and next_move is Game.FORWARD):
            return tuple([self.head.x - 1, self.head.y])

    def move(self, next_square):
        prev_head = self.head
        self.head = Node(next_square[0], next_square[1])
        prev_head.prev_n = self.head
        self.head.next_n = prev_head
        self.tail = self.tail.prev_n
        self.tail.next_n = None

    def eat_apple(self, apple):
        prev_head = self.head
        self.head = Node(apple[0], apple[1])
        prev_head.prev_n = self.head
        self.head.next_n = prev_head

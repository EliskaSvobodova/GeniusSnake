from src import Constants, Settings


class ListNode:
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
For head and body
"""


def heads_direction(node: ListNode):
    if node.next_n.x < node.x:
        return Constants.RIGHT
    if node.x < node.next_n.x:
        return Constants.LEFT
    if node.next_n.y < node.y:
        return Constants.UP
    if node.y < node.next_n.y:
        return Constants.DOWN


"""
For tail,  where rest of the body is
"""


def rest_direction(node: ListNode):
    if node.prev_n.x < node.x:
        return Constants.LEFT
    if node.x < node.prev_n.x:
        return Constants.RIGHT
    if node.prev_n.y < node.y:
        return Constants.DOWN
    if node.y < node.prev_n.y:
        return Constants.UP


"""
For corner
"""


def corner_type(node: ListNode) -> tuple:
    if (node.x < node.prev_n.x and node.y > node.next_n.y) or (node.x < node.next_n.x and node.y > node.prev_n.y):
        return tuple([Constants.DOWN, Constants.RIGHT])
    if (node.x > node.prev_n.x and node.y > node.next_n.y) or (node.x > node.next_n.x and node.y > node.prev_n.y):
        return tuple([Constants.DOWN, Constants.LEFT])
    if (node.x > node.prev_n.x and node.y < node.next_n.y) or (node.x > node.next_n.x and node.y < node.prev_n.y):
        return tuple([Constants.UP, Constants.LEFT])
    if (node.x < node.prev_n.x and node.y < node.next_n.y) or (node.x < node.next_n.x and node.y < node.prev_n.y):
        return tuple([Constants.UP, Constants.RIGHT])


def is_head(node: ListNode):
    return node.prev_n is None


def is_tail(node: ListNode):
    return node.next_n is None


def is_body(node: ListNode):
    return (node.next_n is not None and node.prev_n is not None) \
           and (node.prev_n.x == node.next_n.x or node.prev_n.y == node.next_n.y)


def is_corner(node: ListNode):
    return (node.next_n is not None and node.prev_n is not None) \
           and (node.prev_n.x != node.next_n.x or node.prev_n.y != node.next_n.y)


class Snake:
    def __init__(self):
        self.length = Settings.snake_start_length
        self.tail = self.head = ListNode(self.length, 1)
        for i in range(self.length - 1):
            self.add_part(self.head.x - i - 1, 1)
        self.stamina = Settings.snake_stamina  # how many times is snake able to move without shrinking
        self.without_food = 0

    def add_part(self, x, y):
        prev = self.tail
        self.tail = ListNode(x, y)
        self.tail.prev_n = prev
        prev.next_n = self.tail

    def __iter__(self):
        return SnakeIterator(self)

    def next_square(self, next_move, num_steps):
        direction = heads_direction(self.head)
        if (direction is Constants.UP and next_move is Constants.SNAKE_MOVE_FORWARD) \
                or (direction is Constants.RIGHT and next_move is Constants.SNAKE_MOVE_LEFT) \
                or (direction is Constants.LEFT and next_move is Constants.SNAKE_MOVE_RIGHT):
            return tuple([self.head.x, self.head.y + num_steps])
        if (direction is Constants.UP and next_move is Constants.SNAKE_MOVE_RIGHT) \
                or (direction is Constants.RIGHT and next_move is Constants.SNAKE_MOVE_FORWARD) \
                or (direction is Constants.DOWN and next_move is Constants.SNAKE_MOVE_LEFT):
            return tuple([self.head.x + num_steps, self.head.y])
        if (direction is Constants.RIGHT and next_move is Constants.SNAKE_MOVE_RIGHT) \
                or (direction is Constants.DOWN and next_move is Constants.SNAKE_MOVE_FORWARD) \
                or (direction is Constants.LEFT and next_move is Constants.SNAKE_MOVE_LEFT):
            return tuple([self.head.x, self.head.y - num_steps])
        if (direction is Constants.UP and next_move is Constants.SNAKE_MOVE_LEFT) \
                or (direction is Constants.DOWN and next_move is Constants.SNAKE_MOVE_RIGHT) \
                or (direction is Constants.LEFT and next_move is Constants.SNAKE_MOVE_FORWARD):
            return tuple([self.head.x - num_steps, self.head.y])

    def move(self, next_square):
        prev_head = self.head
        self.head = ListNode(next_square[0], next_square[1])
        prev_head.prev_n = self.head
        self.head.next_n = prev_head
        self.tail = self.tail.prev_n
        self.tail.next_n = None
        self.without_food += 1

    def eat_apple(self, apple):
        prev_head = self.head
        self.head = ListNode(apple[0], apple[1])
        prev_head.prev_n = self.head
        self.head.next_n = prev_head
        self.without_food = 0
        self.length += 1

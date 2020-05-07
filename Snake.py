import Game
import Constants


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
        self.head = ListNode(3, 1)
        self.head.next_n = ListNode(2, 1, prev_n=self.head)
        self.tail = ListNode(1, 1, prev_n=self.head.next_n)
        self.head.next_n.next_n = self.tail
        self.stamina = 10  # how many times is snake able to move without shrinking
        self.without_food = 0
        self.length = 3

    def __iter__(self):
        return SnakeIterator(self)

    def next_square(self, next_move):
        direction = heads_direction(self.head)
        if (direction is Constants.UP and next_move is Constants.SNAKE_MOVE_FORWARD) \
                or (direction is Constants.RIGHT and next_move is Constants.SNAKE_MOVE_LEFT) \
                or (direction is Constants.LEFT and next_move is Constants.SNAKE_MOVE_RIGHT):
            return tuple([self.head.x, self.head.y + 1])
        if (direction is Constants.UP and next_move is Constants.SNAKE_MOVE_RIGHT) \
                or (direction is Constants.RIGHT and next_move is Constants.SNAKE_MOVE_FORWARD) \
                or (direction is Constants.DOWN and next_move is Constants.SNAKE_MOVE_LEFT):
            return tuple([self.head.x + 1, self.head.y])
        if (direction is Constants.RIGHT and next_move is Constants.SNAKE_MOVE_RIGHT) \
                or (direction is Constants.DOWN and next_move is Constants.SNAKE_MOVE_FORWARD) \
                or (direction is Constants.LEFT and next_move is Constants.SNAKE_MOVE_LEFT):
            return tuple([self.head.x, self.head.y - 1])
        if (direction is Constants.UP and next_move is Constants.SNAKE_MOVE_LEFT) \
                or (direction is Constants.DOWN and next_move is Constants.SNAKE_MOVE_RIGHT) \
                or (direction is Constants.LEFT and next_move is Constants.SNAKE_MOVE_FORWARD):
            return tuple([self.head.x - 1, self.head.y])

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

    def shrink(self):
        self.tail = self.tail.prev_n
        self.tail.next_n = None
        self.length -= 1

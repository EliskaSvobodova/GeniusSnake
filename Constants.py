"""
Snake's next move
"""
SNAKE_MOVE_LEFT = -1
SNAKE_MOVE_FORWARD = 0
SNAKE_MOVE_RIGHT = 1

"""
Direction constants
"""
UP = 10
RIGHT = 11
DOWN = 12
LEFT = 13

"""
Game states
"""
PLAY = 20
WIN = 21
LOOSE = 22


def print_constant(constant):
    if constant is SNAKE_MOVE_LEFT:
        print("SNAKE_MOVE_LEFT", end="")
    elif constant is SNAKE_MOVE_FORWARD:
        print("SNAKE_MOVE_FORWARD", end="")
    elif constant is SNAKE_MOVE_RIGHT:
        print("SNAKE_MOVE_RIGHT", end="")
    elif constant is UP:
        print("UP", end="")
    elif constant is RIGHT:
        print("RIGHT", end="")
    elif constant is DOWN:
        print("DOWN", end="")
    elif constant is LEFT:
        print("LEFT", end="")
    elif constant is PLAY:
        print("PLAY", end="")
    elif constant is WIN:
        print("WIN", end="")
    elif constant is LOOSE:
        print("LOOSE", end="")

from src import Settings, Snake

Settings.snake_start_length = 3


def test_snake():
    snake = Snake.Snake()
    assert snake.length == Settings.snake_start_length
    x = Settings.snake_start_length
    y = 1
    assert snake.head.prev_n is None
    for part in snake:
        assert (part.x == x and part.y == y)
        if part != snake.head:
            assert part.prev_n.x == part.x + 1
        x -= 1
    assert x == 0


def test_move():
    snake = Snake.Snake()
    x = Settings.snake_start_length + 1
    y = 1
    snake.move(tuple([x, 1]))
    assert snake.length == Settings.snake_start_length
    assert snake.head.prev_n is None
    for part in snake:
        assert (part.x == x and part.y == y)
        if part != snake.head:
            assert part.prev_n.x == part.x + 1
        x -= 1
    assert x == 1


def test_add_part():
    snake = Snake.Snake()
    snake.move(tuple([Settings.snake_start_length + 1, 1]))
    snake.add_part(1, 1)
    assert snake.length == Settings.snake_start_length + 1
    assert snake.tail.x == 1 and snake.tail.y == 1
    assert snake.tail.next_n is None
    assert snake.tail.prev_n.x == 2 and snake.tail.prev_n.y == 1


def test_eat_apple():
    snake = Snake.Snake()
    snake.eat_apple(tuple([Settings.snake_start_length + 1, 1]))
    assert snake.head.x == Settings.snake_start_length + 1 and snake.head.y == 1
    assert snake.head.prev_n is None
    assert snake.head.next_n.x == Settings.snake_start_length and snake.head.next_n.y == 1

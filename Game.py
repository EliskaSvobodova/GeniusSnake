import UI
import Snake
import random
import Constants


class Game:
    def __init__(self, ui: UI.AbstractUI):
        self.ui = ui
        self.score = 0
        self.game_field_height = self.ui.get_num_squares_height()
        self.game_field_width = self.ui.get_num_squares_width()
        self.snake = Snake.Snake()
        self.ui.prepare_game(self.snake)
        self.speed = 1/3
        self.speed_max = 1/15
        self.score_max = (self.game_field_width * self.game_field_height)
        self.speed_step = (self.speed - self.speed_max) / self.score_max
        self.game_field = [[True for x in range(self.game_field_width)] for y in range(self.game_field_height)]
        # boundary
        for x in range(self.game_field_width):
            self.game_field[0][x] = self.game_field[self.game_field_height - 1][x] = False
        for y in range(self.game_field_height):
            self.game_field[y][0] = self.game_field[y][self.game_field_width - 1] = False
        for part in self.snake:
            self.game_field[part.y][part.x] = False # +1 for the boundary
        self.put_apple()
        self.game_state = Constants.PLAY

    def make_next_move(self, next_move):
        next_square = self.snake.next_square(next_move)
        if self.game_field[next_square[1]][next_square[0]]:  # there is no obstacle
            if self.apple[0] == next_square[0] and self.apple[1] == next_square[1]:  # there is an apple
                self.eat_apple()
            else:
                self.move_snake(next_square)
        else:  # snake bumped into an obstacle
            self.ui.draw_snake_dead(self.snake)
            self.ui.draw_game_over()
            self.game_state = Constants.LOOSE

    def put_apple(self):
        x = random.randint(1, self.game_field_width - 1)
        y = random.randint(1, self.game_field_height - 1)
        while not self.game_field[y][x]:
            x = random.randint(1, self.game_field_width - 1)
            y = random.randint(1, self.game_field_height - 1)
        self.apple = tuple([x, y])
        self.ui.draw_apple(x, y)

    def move_snake(self, next_square):
        self.game_field[next_square[1]][next_square[0]] = False
        self.game_field[self.snake.tail.y][self.snake.tail.x] = True
        prev_tail = tuple([self.snake.tail.x, self.snake.tail.y])
        self.snake.move(next_square)
        self.ui.draw_snake_move(self.snake, prev_tail)

    def eat_apple(self):
        self.game_field[self.apple[1]][self.apple[0]] = False
        self.snake.eat_apple(self.apple)
        self.ui.draw_snake_eat(self.snake)
        self.score += 1
        self.ui.draw_score(self.score)
        if self.score == self.score_max:
            self.game_state = Constants.WIN  # TODO: WIN THE GAME
        self.speed -= self.speed_step
        self.put_apple()

    def get_move_from_direction(self, direction):
        snake_heads = Snake.heads_direction(self.snake.head)
        if (snake_heads is Constants.UP and direction is Constants.LEFT) \
                or (snake_heads is Constants.RIGHT and direction is Constants.UP) \
                or (snake_heads is Constants.DOWN and direction is Constants.RIGHT) \
                or (snake_heads is Constants.LEFT and direction is Constants.DOWN):
            return Constants.SNAKE_MOVE_LEFT
        elif (snake_heads is Constants.UP and direction is Constants.RIGHT) \
                or (snake_heads is Constants.RIGHT and direction is Constants.DOWN) \
                or (snake_heads is Constants.DOWN and direction is Constants.LEFT) \
                or (snake_heads is Constants.LEFT and direction is Constants.UP):
            return Constants.SNAKE_MOVE_RIGHT
        else:
            return Constants.SNAKE_MOVE_FORWARD

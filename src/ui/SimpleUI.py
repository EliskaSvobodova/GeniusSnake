import pyglet
from src import CommonHelpers, Snake
from src.ui import AbstractUI


class SimpleUI(AbstractUI.AbstractUI):
    def __init__(self, x, y, width, height, square_size):
        super().__init__(x, y, width, height, square_size, 2)
        self.game_width = self.square_size * self.num_squares_width
        self.game_height = self.square_size * self.num_squares_height
        self.bushes_color = tuple([56, 88, 129])
        self.field_color = tuple([0, 0, 0])
        self.snake_color = tuple([255, 255, 255])
        self.dead_snake_color = tuple([65, 51, 101])
        self.apple_color = tuple([192, 0, 0])
        self.font_size = 50

    def get_num_squares_height(self):
        return self.num_squares_height

    def get_num_squares_width(self):
        return self.num_squares_width

    def prepare_game(self, snake: Snake.Snake):
        CommonHelpers.draw_colored_rectangle(self.game_x, self.game_y,
                                             self.game_width, self.game_height + self.score_squares * self.square_size,
                                             0, 0, 0)
        self.draw_game_field()
        self.draw_score(0)
        self.draw_bushes()
        self.draw_snake(snake)
        self.draw_boundary()

    def redraw(self, snake: Snake.Snake, score, identifier, num_runs, apple):
        self.draw_game_field()
        self.draw_score(score)
        self.draw_identifier(identifier, num_runs)
        self.draw_apple(apple[0], apple[1])
        self.draw_snake(snake)

    def draw_snake_eat(self, snake: Snake.Snake):
        CommonHelpers.draw_colored_rectangle(self.game_x + snake.head.x * self.square_size,
                                             self.game_y + snake.head.y * self.square_size,
                                             self.square_size, self.square_size,
                                             self.snake_color[0], self.snake_color[1], self.snake_color[2])

    def draw_snake_move(self, snake: Snake.Snake, prev_tail):
        CommonHelpers.draw_colored_rectangle(self.game_x + prev_tail[0] * self.square_size,
                                             self.game_y + prev_tail[1] * self.square_size,
                                             self.square_size, self.square_size,
                                             self.field_color[0], self.field_color[1], self.field_color[2])
        CommonHelpers.draw_colored_rectangle(self.game_x + snake.head.x * self.square_size,
                                             self.game_y + snake.head.y * self.square_size,
                                             self.square_size, self.square_size,
                                             self.snake_color[0], self.snake_color[1], self.snake_color[2])

    def draw_apple(self, x, y):
        CommonHelpers.draw_colored_rectangle(self.game_x + x * self.square_size, self.game_y + y * self.square_size,
                                             self.square_size, self.square_size,
                                             self.apple_color[0], self.apple_color[1], self.apple_color[2])

    def draw_snake(self, snake: Snake.Snake):
        for part in snake:
            CommonHelpers.draw_colored_rectangle(self.game_x + part.x * self.square_size,
                                                 self.game_y + part.y * self.square_size,
                                                 self.square_size, self.square_size,
                                                 self.snake_color[0], self.snake_color[1], self.snake_color[2])

    def draw_snake_dead(self, snake: Snake.Snake):
        for part in snake:
            CommonHelpers.draw_colored_rectangle(self.game_x + part.x * self.square_size,
                                                 self.game_y + part.y * self.square_size,
                                                 self.square_size, self.square_size,
                                                 self.dead_snake_color[0],
                                                 self.dead_snake_color[1],
                                                 self.dead_snake_color[2])

    def draw_game_field(self):
        x = self.game_x + self.square_size
        y = self.game_y + self.square_size
        width = self.game_width - 2 * self.square_size
        height = self.game_height - 2 * self.square_size
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ("v2f", (x, y,
                                      x, y + height,
                                      x + width, y + height,
                                      x + width, y)),
                             ("c3B", ((self.field_color[0], self.field_color[1], self.field_color[2]) * 4)))

    def draw_bushes(self):
        for i in range(self.num_squares_width):
            CommonHelpers.draw_colored_rectangle(self.game_x + i * self.square_size,
                                                 self.game_y,
                                                 self.square_size, self.square_size,
                                                 self.bushes_color[0], self.bushes_color[1], self.bushes_color[2])
            CommonHelpers.draw_colored_rectangle(self.game_x + i * self.square_size,
                                                 self.game_y + (self.num_squares_height - 1) * self.square_size,
                                                 self.square_size, self.square_size,
                                                 self.bushes_color[0], self.bushes_color[1], self.bushes_color[2])
        for i in range(self.num_squares_height):
            CommonHelpers.draw_colored_rectangle(self.game_x,
                                                 self.game_y + i * self.square_size,
                                                 self.square_size, self.square_size,
                                                 self.bushes_color[0], self.bushes_color[1], self.bushes_color[2])
            CommonHelpers.draw_colored_rectangle(self.game_x + (self.num_squares_width - 1) * self.square_size,
                                                 self.game_y + i * self.square_size,
                                                 self.square_size, self.square_size,
                                                 self.bushes_color[0], self.bushes_color[1], self.bushes_color[2])

    def draw_score(self, score):
        x = self.game_x + 2
        y = self.game_y + self.num_squares_height * self.square_size
        width = ((self.num_squares_width * self.square_size) / 2) - 2
        height = (self.score_squares * self.square_size) - 2

        CommonHelpers.draw_colored_rectangle(x, y, width, height, 0, 0, 0)

        score_label = pyglet.text.Label(text=f"Score: {score}",
                                        x=(x + 5), y=(y + (self.square_size * self.score_squares) / 2),
                                        anchor_x="left", anchor_y="center",
                                        font_name="Bangers", font_size=(self.square_size * self.score_squares) // 2)
        score_label.draw()
        pyglet.gl.glFlush()

    def draw_identifier(self, identifier, run):
        x = self.game_x + self.num_squares_width * self.square_size - 1
        y = self.game_y + self.num_squares_height * self.square_size
        width = ((self.num_squares_width * self.square_size) / 2)
        height = (self.score_squares * self.square_size) - 1

        CommonHelpers.draw_colored_rectangle(x - width, y, width, height, 0, 0, 0)

        pyglet.text.Label(text=f"ID: {identifier}, run: {run}",
                          x=(x - 5), y=(y + height / 2),
                          anchor_x="right", anchor_y="center",
                          font_name="Bangers", font_size=(self.square_size * self.score_squares) // 2
                          ).draw()
        pyglet.gl.glFlush()

    def draw_background(self):
        CommonHelpers.draw_colored_rectangle(self.screen_x, self.screen_y, self.width, self.height, 0, 0, 0)

    def draw_game_over(self):
        pyglet.text.Label(text="GAME OVER",
                          x=self.game_x + (self.game_width / 2),
                          y=self.game_y + (self.game_height / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=30).draw()
        pyglet.gl.glFlush()

    def draw_game_won(self):
        pyglet.text.Label(text="WINNER!",
                          x=self.game_x + (self.game_width / 2),
                          y=self.game_y + (self.game_height / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=30).draw()
        pyglet.gl.glFlush()

    def draw_boundary(self):
        width = self.num_squares_width * self.square_size
        height = (self.num_squares_height + self.score_squares) * self.square_size
        pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                             ("v2f", (self.game_x, self.game_y,
                                      self.game_x, self.game_y + height,
                                      self.game_x, self.game_y + height,
                                      self.game_x + width, self.game_y + height,
                                      self.game_x + width, self.game_y + height,
                                      self.game_x + width, self.game_y,
                                      self.game_x + width, self.game_y,
                                      self.game_x, self.game_y)))
        pyglet.gl.glFlush()

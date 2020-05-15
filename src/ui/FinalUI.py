import Snake
from src.ui import AbstractUI
import pyglet


class FinalUI(AbstractUI.AbstractUI):
    def __init__(self, x, y, width, height, square_size):
        super().__init__(x, y, width, height, square_size)
        self.num_squares_height = (self.height - self.square_size) // self.square_size
        self.num_squares_width = self.width // self.square_size
        self.game_width = self.square_size * self.num_squares_width
        self.game_height = self.square_size * self.num_squares_height

    def get_num_squares_height(self):
        return self.num_squares_height

    def get_num_squares_width(self):
        return self.num_squares_width

    def prepare_game(self, snake: Snake.Snake):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ("v2f", (self.x, self.y,
                                      self.x, self.y + self.height,
                                      self.x + self.width, self.y + self.height,
                                      self.x + self.width, self.y)),
                             ("c3B", ((0, 0, 0) * 4)))
        self.draw_score(0)
        self.draw_bushes()
        self.draw_game_field()
        self.draw_snake(snake)
        self.draw_boundary()
        pyglet.gl.glFlush()

    def redraw(self, snake: Snake.Snake, score, apple):
        x = self.x + self.square_size
        y = self.y + self.square_size
        width = self.game_width - 2 * self.square_size
        height = self.game_height - 2 * self.square_size
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ("v2f", (x, y,
                                      x, y + height,
                                      x + width, y + height,
                                      x + width, y)),
                             ("c3B", ((0, 0, 0) * 4)))
        self.draw_score(score)
        self.draw_apple(apple[0], apple[1])
        self.draw_snake(snake)
        pyglet.gl.glFlush()

    def draw_snake_eat(self, snake: Snake.Snake):
        self.draw_colorful_square(snake.head.x, snake.head.y, 255, 255, 255)
        pyglet.gl.glFlush()

    def draw_snake_move(self, snake: Snake.Snake, prev_tail):
        self.draw_square(prev_tail[0], prev_tail[1])
        self.draw_colorful_square(snake.head.x, snake.head.y, 255, 255, 255)
        pyglet.gl.glFlush()

    def draw_snake_shrink(self, snake: Snake.Snake):
        self.draw_colorful_square(snake.tail.x, snake.tail.y, 0, 0, 0)
        pyglet.gl.glFlush()

    def draw_apple(self, x, y):
        self.draw_colorful_square(x, y, 255, 106, 0)
        pyglet.gl.glFlush()

    def draw_snake(self, snake: Snake.Snake):
        for part in snake:
            self.draw_colorful_square(part.x, part.y, 255, 255, 255)
        pyglet.gl.glFlush()

    def draw_snake_dead(self, snake: Snake.Snake):
        for part in snake:
            self.draw_colorful_square(part.x, part.y, 15, 1, 51)
        pyglet.gl.glFlush()

    def draw_game_field(self):
        x = self.x + self.square_size
        y = self.y + self.square_size
        width = self.game_width - 2 * self.square_size
        height = self.game_height - 2 * self.square_size
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ("v2f", (x, y,
                                      x, y + height,
                                      x + width, y + height,
                                      x + width, y)),
                             ("c3B", ((116, 1, 113) * 4)))

    def draw_square(self, x, y):
        self.draw_colorful_square(x, y, 116, 1, 113)

    def draw_colorful_square(self, x, y, r, g, b):
        x2 = x1 = self.x + (x * self.square_size)
        y4 = y1 = self.y + (y * self.square_size)
        y2 = y1 + self.square_size
        x3 = x1 + self.square_size
        y3 = y1 + self.square_size
        x4 = x1 + self.square_size
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ("v2f", (x1, y1, x2, y2, x3, y3, x4, y4)),
                             ("c3B", ((r, g, b) * 4)))
        pyglet.gl.glFlush()

    def draw_bushes(self):
        for i in range(self.num_squares_width):
            self.draw_colorful_square(i, 0, 7, 87, 152)
            self.draw_colorful_square(i, self.num_squares_height - 1, 7, 87, 152)
        for i in range(self.num_squares_height):
            self.draw_colorful_square(0, i, 7, 87, 152)
            self.draw_colorful_square(self.num_squares_width - 1, i, 7, 87, 152)
        pyglet.gl.glFlush()

    def draw_score(self, score):
        x = self.x + 2
        y = self.y + self.num_squares_height * self.square_size
        width = self.width - 20  # minus few pixels so it doesn't cover boundary
        height = self.y + self.height - y
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ("v2f", (x, y, x, y + height, x + width, y + height, x + width, y)),
                             ("c3B", ((0, 0, 0) * 4)))
        pyglet.text.Label(text=f"Score: {score}", x=(x + width / 2), y=(y + height / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=height // 2
                          ).draw()
        pyglet.gl.glFlush()

    def draw_background(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ("v2f", (self.x, self.y,
                                      self.x, self.y + self.height,
                                      self.x + self.width, self.y + self.height,
                                      self.x + self.width, self.y)),
                             ("c3B", ((0, 0, 0) * 4)))
        pyglet.gl.glFlush()

    def draw_game_over(self):
        pyglet.text.Label(text="GAME OVER",
                          x=self.x + (self.width / 2),
                          y=self.y + (self.height / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=30).draw()
        pyglet.gl.glFlush()

    def draw_game_won(self):
        pyglet.text.Label(text="WINNER!",
                          x=self.x + (self.width / 2),
                          y=self.y + (self.height / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=30).draw()
        pyglet.gl.glFlush()

    def draw_boundary(self):
        width = (self.num_squares_width * self.square_size)
        height = self.height
        pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                             ("v2f", (self.x, self.y, self.x, self.y + height,
                                      self.x, self.y + height, self.x + width, self.y + height,
                                      self.x + width, self.y + height, self.x + width, self.y,
                                      self.x + width, self.y, self.x, self.y)))

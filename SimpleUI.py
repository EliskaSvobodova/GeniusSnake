import pyglet
import Snake
import AbstractUI
import Settings
import CommonHelpers


class ControlPaneUI:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = 50
        space_between = 20
        self.graph_x = self.x + space_between
        self.graph_y = self.y + space_between
        self.graph_width = self.width - 2 * space_between
        self.graph_height = self.height - 1.5 * self.font_size - 2 * space_between
        self.point = self.load_point()

    def draw(self, generation):
        height = self.height - self.graph_height
        # plus five because of graph's last label
        CommonHelpers.draw_colored_rectangle(self.x, self.graph_y + self.graph_height + 5,
                                             self.width, self.height - self.graph_height,
                                             0, 0, 0)
        pyglet.text.Label(text=f"Generation: {generation}",
                          x=(self.x + self.width / 2), y=(self.y + self.height - self.font_size / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=self.font_size
                          ).draw()
        self.draw_graph_skeleton()
        pyglet.gl.glFlush()

    def draw_graph(self, values):
        CommonHelpers.draw_colored_rectangle(self.graph_x, self.y,
                                             self.graph_width, self.graph_height + self.graph_y - self.x,
                                             0, 0, 0)
        space = self.graph_width / (len(values) + 1)
        point_scale = self.graph_height / Settings.max_score
        i = 0
        for v in values:
            self.point.x = self.graph_x + i * space + space
            self.point.y = self.graph_y + v * point_scale
            self.point.draw()
            i += 1
        pyglet.gl.glFlush()

    def draw_graph_skeleton(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
                             ("v2f", (self.graph_x, self.graph_y,
                                      self.graph_x, self.graph_y + self.graph_height,
                                      self.graph_x, self.graph_y,
                                      self.graph_x + self.graph_width, self.graph_y)),
                             ("c3B", ((56, 88, 129) * 4)))
        space_between = self.graph_height / (Settings.num_graph_labels - 1)
        difference = Settings.max_score / (Settings.num_graph_labels - 1)
        for i in range(Settings.num_graph_labels):
            pyglet.text.Label(text=f"{round(i * difference)}",
                              x=self.x, y=self.graph_y + i * space_between,
                              anchor_x="center", anchor_y="center",
                              font_size=10).draw()

    def load_point(self):
        point_image = pyglet.resource.image("SimpleUI/point.png")
        CommonHelpers.scale_image(point_image, 10, 10)
        CommonHelpers.center_image(point_image)
        return pyglet.sprite.Sprite(img=point_image)


class SimpleUI(AbstractUI.AbstractUI):
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
        CommonHelpers.draw_colored_rectangle(self.x, self.y,
                                             self.num_squares_width * self.square_size, self.height,
                                             0, 0, 0)
        self.draw_score(0)
        self.draw_bushes()
        self.draw_snake(snake)
        self.draw_boundary()

    def redraw(self, snake: Snake.Snake, score, identifier, num_runs, apple):
        CommonHelpers.draw_colored_rectangle(self.x + self.square_size, self.y + self.square_size,
                                             self.game_width - 2 * self.square_size,
                                             self.game_height - 2 * self.square_size,
                                             0, 0, 0)
        self.draw_score(score)
        self.draw_identifier(identifier, num_runs)
        self.draw_apple(apple[0], apple[1])
        self.draw_snake(snake)

    def draw_snake_eat(self, snake: Snake.Snake):
        CommonHelpers.draw_colored_rectangle(self.x + snake.head.x * self.square_size,
                                             self.y + snake.head.y * self.square_size,
                                             self.square_size, self.square_size,
                                             255, 255, 255)

    def draw_snake_move(self, snake: Snake.Snake, prev_tail):
        CommonHelpers.draw_colored_rectangle(self.x + prev_tail[0] * self.square_size,
                                             self.y + prev_tail[1] * self.square_size,
                                             self.square_size, self.square_size,
                                             0, 0, 0)
        CommonHelpers.draw_colored_rectangle(self.x + snake.head.x * self.square_size,
                                             self.y + snake.head.y * self.square_size,
                                             self.square_size, self.square_size,
                                             255, 255, 255)

    def draw_apple(self, x, y):
        CommonHelpers.draw_colored_rectangle(self.x + x * self.square_size, self.y + y * self.square_size,
                                             self.square_size, self.square_size,
                                             192, 0, 0)

    def draw_snake(self, snake: Snake.Snake):
        for part in snake:
            CommonHelpers.draw_colored_rectangle(self.x + part.x * self.square_size, self.y + part.y * self.square_size,
                                                 self.square_size, self.square_size,
                                                 255, 255, 255)

    def draw_snake_dead(self, snake: Snake.Snake):
        for part in snake:
            CommonHelpers.draw_colored_rectangle(self.x + part.x * self.square_size, self.y + part.y * self.square_size,
                                                 self.square_size, self.square_size,
                                                 65, 51, 101)

    def draw_game_field(self):
        pass  # no need to do anything, game field is supposed to be black

    def draw_bushes(self):
        for i in range(self.num_squares_width):
            CommonHelpers.draw_colored_rectangle(self.x + i * self.square_size,
                                                 self.y,
                                                 self.square_size, self.square_size,
                                                 56, 88, 129)
            CommonHelpers.draw_colored_rectangle(self.x + i * self.square_size,
                                                 self.y + (self.num_squares_height - 1) * self.square_size,
                                                 self.square_size, self.square_size,
                                                 56, 88, 129)
        for i in range(self.num_squares_height):
            CommonHelpers.draw_colored_rectangle(self.x,
                                                 self.y + i * self.square_size,
                                                 self.square_size, self.square_size,
                                                 56, 88, 129)
            CommonHelpers.draw_colored_rectangle(self.x + (self.num_squares_width - 1) * self.square_size,
                                                 self.y + i * self.square_size,
                                                 self.square_size, self.square_size,
                                                 56, 88, 129)

    def draw_score(self, score):
        x = self.x
        y = self.y + self.num_squares_height * self.square_size
        width = (self.num_squares_width * self.square_size) / 2
        height = self.y + self.height - y

        CommonHelpers.draw_colored_rectangle(x, y, width, height, 0, 0, 0)

        pyglet.text.Label(text=f"Score: {score}",
                          x=(x + 5), y=(y + height / 2),
                          anchor_y="center",
                          font_name="Bangers", font_size=height // 2
                          ).draw()
        pyglet.gl.glFlush()

    def draw_identifier(self, identifier, run):
        x = self.x + self.num_squares_width * self.square_size - 1
        y = self.y + self.num_squares_height * self.square_size
        width = (self.num_squares_width * self.square_size) / 2
        height = self.y + self.height - y

        CommonHelpers.draw_colored_rectangle(x - width, y, width, height, 0, 0, 0)

        pyglet.text.Label(text=f"ID: {identifier}, run: {run}",
                          x=(x - 5), y=(y + height / 2),
                          anchor_x="right", anchor_y="center",
                          font_name="Bangers", font_size=height // 2
                          ).draw()
        pyglet.gl.glFlush()

    def draw_background(self):
        CommonHelpers.draw_colored_rectangle(self.x, self.y, self.width, self.height, 0, 0, 0)

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
        pyglet.gl.glFlush()

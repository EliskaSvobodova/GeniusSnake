import pyglet
import Snake
import CommonHelpers
import Constants
from src.ui import AbstractUI


class NiceUI(AbstractUI.AbstractUI):
    def __init__(self, x, y, width, height, square_size):
        super().__init__(x, y, width, height, square_size)
        self.draw_loading_screen()
        self.load_images()
        self.num_squares_height = (self.height - self.score_background.height) // self.square_size
        self.num_squares_width = self.width // self.square_size
        self.game_width = self.square_size * self.num_squares_width
        self.game_height = self.square_size * self.num_squares_height
        self.prepare_cover_squares()
        # enable transparency
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    def draw_loading_screen(self):
        CommonHelpers.draw_colored_rectangle(self.x, self.y, self.width, self.height, 65, 51, 101)
        pyglet.text.Label(text="Loading...",
                          x=(self.x + self.width / 2), y=(self.y + self.height / 2),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=60).draw()
        pyglet.gl.glFlush()

    """ IMAGE LOADING """

    def load_images(self):
        self.load_grass()
        self.load_score_background()
        self.load_snake()
        self.load_bush()
        self.load_apple()

    def load_grass(self):
        grass_image = pyglet.resource.image("NiceUI/grass.jpg")
        CommonHelpers.scale_image(grass_image, self.width - 2,
                                  self.height - 2)  # minus few pixels so the boundary is visible
        CommonHelpers.center_image(grass_image)
        self.grass = pyglet.sprite.Sprite(img=grass_image, x=self.x + (self.width / 2), y=self.y + (self.height / 2))

    def load_score_background(self):
        score_background_image = pyglet.resource.image("NiceUI/score_background.png")
        CommonHelpers.center_image(score_background_image)
        self.score_background = pyglet.sprite.Sprite(img=score_background_image,
                                                     x=self.x + (self.width / 2),
                                                     y=self.y + self.height - (score_background_image.height / 2))

    def load_snake(self):
        snake_head_image = pyglet.resource.image("NiceUI/snake_head.png")
        snake_body_image = pyglet.resource.image("NiceUI/snake_body.png")
        snake_corner_image = pyglet.resource.image("NiceUI/snake_corner.png")
        snake_tail_image = pyglet.resource.image("NiceUI/snake_tail.png")
        snake_head_dead_image = pyglet.resource.image("NiceUI/snake_head_dead.png")

        CommonHelpers.scale_image(snake_head_image, self.square_size, self.square_size)
        CommonHelpers.scale_image(snake_body_image, self.square_size, self.square_size)
        CommonHelpers.scale_image(snake_corner_image, self.square_size, self.square_size)
        CommonHelpers.scale_image(snake_tail_image, self.square_size, self.square_size)
        CommonHelpers.scale_image(snake_head_dead_image, self.square_size, self.square_size)

        CommonHelpers.center_image(snake_head_image)
        CommonHelpers.center_image(snake_body_image)
        CommonHelpers.center_image(snake_corner_image)
        CommonHelpers.center_image(snake_tail_image)
        CommonHelpers.center_image(snake_head_dead_image)

        self.snake_head = pyglet.sprite.Sprite(img=snake_head_image)
        self.snake_body = pyglet.sprite.Sprite(img=snake_body_image)
        self.snake_corner = pyglet.sprite.Sprite(img=snake_corner_image)
        self.snake_tail = pyglet.sprite.Sprite(img=snake_tail_image)
        self.snake_head_dead = pyglet.sprite.Sprite(img=snake_head_dead_image)

    def load_bush(self):
        bush_image = pyglet.resource.image("NiceUI/bush2.png")
        CommonHelpers.scale_image(bush_image, self.square_size, self.square_size)
        CommonHelpers.center_image(bush_image)
        self.bush = pyglet.sprite.Sprite(img=bush_image)

    def load_apple(self):
        apple_image = pyglet.resource.image("NiceUI/apple.png")
        CommonHelpers.scale_image(apple_image, self.square_size, self.square_size)
        CommonHelpers.center_image(apple_image)
        self.apple = pyglet.sprite.Sprite(img=apple_image)

    """ OTHER PREPARATIONS """

    def prepare_cover_squares(self):
        grass = pyglet.image.load("../../resources/NiceUI/grass.png", decoder=pyglet.image.codecs.png.PNGImageDecoder())
        self.cover_squares = []
        for i in range(self.num_squares_height):
            row = []
            for j in range(self.num_squares_width):
                square = grass.get_region(x=(self.x + j * self.square_size), y=(self.y + i * self.square_size),
                                          width=self.square_size, height=self.square_size)
                row.append(pyglet.sprite.Sprite(square,
                                                x=(self.x + j * self.square_size),
                                                y=(self.y + i * self.square_size)))
            self.cover_squares.append(row)

    """ GETTERS """

    def get_num_squares_height(self):
        return self.num_squares_height

    def get_num_squares_width(self):
        return self.num_squares_width

    """ DRAWING """

    def prepare_game(self, snake):
        self.draw_background()
        self.draw_score(0)
        self.draw_game_field()
        self.draw_boundary()
        self.draw_snake(snake)
        pyglet.gl.glFlush()

    def draw_snake_eat(self, snake: Snake.Snake):
        self.draw_square(snake.head.next_n.x, snake.head.next_n.y)
        self.draw_snake_head(snake.head)
        self.draw_snake_part(snake.head.next_n)
        pyglet.gl.glFlush()

    def draw_snake_move(self, snake: Snake.Snake, prev_tail):
        self.draw_square(prev_tail[0], prev_tail[1])
        self.draw_square(snake.tail.x, snake.tail.y)
        self.draw_square(snake.head.next_n.x, snake.head.next_n.y)
        self.draw_snake_head(snake.head)
        self.draw_snake_part(snake.head.next_n)
        self.draw_snake_tail(snake.tail)
        pyglet.gl.glFlush()

    def draw_apple(self, x, y):
        self.apple.x = self.x + x * self.square_size + self.square_size / 2
        self.apple.y = self.y + y * self.square_size + self.square_size / 2
        self.apple.draw()
        pyglet.gl.glFlush()

    def draw_snake(self, snake: Snake.Snake):
        for part in snake:
            self.draw_snake_part(part)
        pyglet.gl.glFlush()

    def draw_snake_dead(self, snake: Snake.Snake):
        self.draw_snake_head_dead(snake.head)
        pyglet.gl.glFlush()

    def draw_snake_part(self, part: Snake.ListNode):
        if Snake.is_head(part):
            self.draw_snake_head(part)
        elif Snake.is_tail(part):
            self.draw_snake_tail(part)
        elif Snake.is_body(part):
            self.draw_snake_body(part)
        elif Snake.is_corner(part):
            self.draw_snake_corner(part)
        pyglet.gl.glFlush()

    def draw_snake_head(self, part: Snake.ListNode):
        self.snake_head.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_head.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.heads_direction(part)
        if direction is Constants.UP:
            self.snake_head.rotation = 0
        elif direction is Constants.RIGHT:
            self.snake_head.rotation = 90
        elif direction is Constants.DOWN:
            self.snake_head.rotation = 180
        elif direction is Constants.LEFT:
            self.snake_head.rotation = 270
        self.snake_head.draw()
        pyglet.gl.glFlush()

    def draw_snake_head_dead(self, part: Snake.ListNode):
        self.snake_head_dead.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_head_dead.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.heads_direction(part)
        if direction is Constants.UP:
            self.snake_head_dead.rotation = 0
        elif direction is Constants.RIGHT:
            self.snake_head_dead.rotation = 90
        elif direction is Constants.DOWN:
            self.snake_head_dead.rotation = 180
        elif direction is Constants.LEFT:
            self.snake_head_dead.rotation = 270
        self.snake_head_dead.draw()
        pyglet.gl.glFlush()

    def draw_snake_tail(self, part: Snake.ListNode):
        self.snake_tail.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_tail.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.rest_direction(part)
        if direction is Constants.UP:
            self.snake_tail.rotation = 0
        elif direction is Constants.RIGHT:
            self.snake_tail.rotation = 90
        elif direction is Constants.DOWN:
            self.snake_tail.rotation = 180
        elif direction is Constants.LEFT:
            self.snake_tail.rotation = 270
        self.snake_tail.draw()
        pyglet.gl.glFlush()

    def draw_snake_body(self, part: Snake.ListNode):
        self.snake_body.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_body.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.heads_direction(part)
        if direction is Constants.UP or direction is Constants.DOWN:
            self.snake_body.rotation = 0
        elif direction is Constants.LEFT or direction is Constants.RIGHT:
            self.snake_body.rotation = 90
        self.snake_body.draw()
        pyglet.gl.glFlush()

    def draw_snake_corner(self, part: Snake.ListNode):
        self.snake_corner.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_corner.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.corner_type(part)
        if direction[0] is Constants.UP and direction[1] is Constants.RIGHT:
            self.snake_corner.rotation = 270
        elif direction[0] is Constants.UP and direction[1] is Constants.LEFT:
            self.snake_corner.rotation = 180
        elif direction[0] is Constants.DOWN and direction[1] is Constants.RIGHT:
            self.snake_corner.rotation = 0
        elif direction[0] is Constants.DOWN and direction[1] is Constants.LEFT:
            self.snake_corner.rotation = 90
        self.snake_corner.draw()
        pyglet.gl.glFlush()

    def draw_game_field(self):
        for i in range(1, self.num_squares_height - 1):
            for j in range(1, self.num_squares_width - 1):
                self.draw_square(j, i)
        self.draw_bushes()
        pyglet.gl.glFlush()

    def draw_square(self, x, y):
        self.cover_squares[y][x].draw()
        x1 = self.x + (x * self.square_size)
        y1 = self.y + (y * self.square_size)
        x2 = x1
        y2 = y1 + self.square_size
        x3 = x1 + self.square_size
        y3 = y1 + self.square_size
        x4 = x1 + self.square_size
        y4 = y1
        if y % 2:
            if x % 2:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                                     ("v2f", (x1, y1, x2, y2, x3, y3, x4, y4)),
                                     ("c4B", ((11, 102, 35, 110) * 4)))
            else:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                                     ("v2f", (x1, y1, x2, y2, x3, y3, x4, y4)),
                                     ("c4B", ((137, 173, 111, 80) * 4)))
        else:
            if x % 2:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                                     ("v2f", (x1, y1, x2, y2, x3, y3, x4, y4)),
                                     ("c4B", ((137, 173, 111, 80) * 4)))
            else:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                                     ("v2f", (x1, y1, x2, y2, x3, y3, x4, y4)),
                                     ("c4B", ((11, 102, 35, 110) * 4)))
        pyglet.gl.glFlush()

    def draw_bushes(self):
        for i in range(self.num_squares_width):
            self.bush.x = self.x + i * self.square_size + self.square_size / 2
            self.bush.y = self.y + self.square_size / 2
            self.bush.draw()
            self.bush.y = self.y + (self.num_squares_height - 1) * self.square_size + self.square_size / 2
            self.bush.draw()
        for i in range(self.num_squares_height):
            self.bush.x = self.x + self.square_size / 2
            self.bush.y = self.y + i * self.square_size + self.square_size / 2
            self.bush.draw()
            self.bush.x = self.x + (self.num_squares_width - 1) * self.square_size + self.square_size / 2
            self.bush.draw()
        pyglet.gl.glFlush()

    def draw_score(self, score):
        self.score_background.draw()
        pyglet.text.Label(text=f"Score: {score}", x=self.score_background.x, y=self.score_background.y,
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=self.score_background.height // 3
                          ).draw()
        pyglet.gl.glFlush()

    def draw_background(self):
        self.grass.draw()
        pyglet.gl.glFlush()

    """ DRAW GAME STATES """

    def redraw(self, snake: Snake.Snake, score, identification, num_runs, apple):
        self.draw_snake(snake)
        self.draw_score(score)
        self.draw_apple(apple[0], apple[1])

    def draw_game_over(self):
        pyglet.text.Label(text="GAME OVER",
                          x=(self.width / 2),
                          y=(self.height / 3) * 2,
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=60).draw()
        pyglet.text.Label(text="[click to go back to menu]",
                          x=(self.width / 2),
                          y=(self.height / 3),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=40).draw()
        pyglet.gl.glFlush()

    def draw_game_won(self):
        pyglet.text.Label(text="YOU WIN! CONGRATULATION!",
                          x=(self.width / 2),
                          y=(self.height / 3) * 2,
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=60).draw()
        pyglet.text.Label(text="[click to go back to menu]",
                          x=(self.width / 2),
                          y=(self.height / 3),
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=40).draw()
        pyglet.gl.glFlush()

    def draw_boundary(self):
        pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                             ("v2f", (self.x, self.y, self.x, self.y + self.height,
                                      self.x, self.y + self.height, self.x + self.width, self.y + self.height,
                                      self.x + self.width, self.y + self.height, self.x + self.width, self.y,
                                      self.x + self.width, self.y, self.x, self.y)))

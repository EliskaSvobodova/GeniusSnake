from abc import ABCMeta, abstractmethod
import pyglet
import CommonHelpers
import Snake


class AbstractUI(metaclass=ABCMeta):
    def __init__(self, x, y, width, height, window):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        CommonHelpers.configure_resources()

    @abstractmethod
    def draw_score(self, score):
        raise NotImplementedError()

    @abstractmethod
    def draw_background(self):
        raise NotImplementedError()

    @abstractmethod
    def draw_game_field(self):
        raise NotImplementedError()

    @abstractmethod
    def draw_boundary(self):
        raise NotImplementedError()

    @abstractmethod
    def get_num_squares_height(self):
        raise NotImplementedError()

    @abstractmethod
    def get_num_squares_width(self):
        raise NotImplementedError()

    @abstractmethod
    def draw_snake(self, snake : Snake):
        raise NotImplementedError()


class NiceUI(AbstractUI):
    def draw_snake(self, snake: Snake.Snake):
        for part in snake:
            self.draw_snake_part(part)

    def draw_snake_part(self, part: Snake.Node):
        if Snake.is_head(part):
            self.draw_snake_head(part)
        elif Snake.is_tail(part):
            self.draw_snake_tail(part)
        elif Snake.is_body(part):
            self.draw_snake_body(part)
        elif Snake.is_corner(part):
            self.draw_snake_corner(part)

    def draw_snake_head(self, part: Snake.Node):
        self.snake_head.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_head.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.heads_direction(part)
        if direction is Snake.UP:
            self.snake_head.rotation = 0
        elif direction is Snake.RIGHT:
            self.snake_head.rotation = 90
        elif direction is Snake.DOWN:
            self.snake_head.rotation = 180
        elif direction is Snake.LEFT:
            self.snake_head.rotation = 270
        self.snake_head.draw()

    def draw_snake_tail(self, part: Snake.Node):
        self.snake_tail.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_tail.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.rest_direction(part)
        if direction is Snake.UP:
            self.snake_tail.rotation = 0
        elif direction is Snake.RIGHT:
            self.snake_tail.rotation = 90
        elif direction is Snake.DOWN:
            self.snake_tail.rotation = 180
        elif direction is Snake.LEFT:
            self.snake_tail.rotation = 270
        self.snake_tail.draw()

    def draw_snake_body(self, part: Snake.Node):
        self.snake_body.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_body.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.heads_direction(part)
        if direction is Snake.UP or direction is Snake.DOWN:
            self.snake_body.rotation = 0
        elif direction is Snake.LEFT or direction is Snake.RIGHT:
            self.snake_body.rotation = 90
        self.snake_body.draw()

    def draw_snake_corner(self, part: Snake.Node):
        self.snake_corner.x = self.x + (part.x * self.square_size) + (self.square_size / 2)
        self.snake_corner.y = self.y + (part.y * self.square_size) + (self.square_size / 2)
        direction = Snake.corner_type(part)
        if direction[0] is Snake.UP and direction[1] is Snake.RIGHT:
            self.snake_corner.rotation = 270
        elif direction[0] is Snake.UP and direction[1] is Snake.LEFT:
            self.snake_corner.rotation = 180
        elif direction[0] is Snake.DOWN and direction[1] is Snake.RIGHT:
            self.snake_corner.rotation = 0
        elif direction[0] is Snake.DOWN and direction[1] is Snake.LEFT:
            self.snake_corner.rotation = 90
        self.snake_corner.draw()

    def get_num_squares_height(self):
        return self.num_squares_height

    def get_num_squares_width(self):
        return self.num_squares_width

    def draw_game_field(self):
        pass

    def __init__(self, x, y, width, height, window):
        super().__init__(x, y, width, height, window)
        self.square_size = 50
        self.load_images()
        self.num_squares_height = (self.height - self.score_background.height) // self.square_size
        self.num_squares_width = self.width // self.square_size

    def draw_score(self, score):
        self.score_background.draw()
        pyglet.text.Label(text=f"Score: {score}", x=self.score_background.x, y=self.score_background.y,
                          anchor_x="center", anchor_y="center",
                          font_name="Bangers", font_size=self.score_background.height // 3
                          ).draw()

    def draw_background(self):
        self.grass.draw()

    def load_images(self):
        self.load_grass()
        self.load_score_background()
        self.load_snake()

    def load_grass(self):
        grass_image = pyglet.resource.image("NiceUI/grass.jpg")
        CommonHelpers.scale_image(grass_image, self.width - 2, self.height - 2)  # minus few pixels so the boundary is visible
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

        CommonHelpers.scale_image(snake_head_image, self.square_size, self.square_size)
        CommonHelpers.scale_image(snake_body_image, self.square_size, self.square_size)
        CommonHelpers.scale_image(snake_corner_image, self.square_size, self.square_size)
        CommonHelpers.scale_image(snake_tail_image, self.square_size, self.square_size)

        CommonHelpers.center_image(snake_head_image)
        CommonHelpers.center_image(snake_body_image)
        CommonHelpers.center_image(snake_corner_image)
        CommonHelpers.center_image(snake_tail_image)
        self.snake_head = pyglet.sprite.Sprite(img=snake_head_image)
        self.snake_body = pyglet.sprite.Sprite(img=snake_body_image)
        self.snake_corner = pyglet.sprite.Sprite(img=snake_corner_image)
        self.snake_tail = pyglet.sprite.Sprite(img=snake_tail_image)

    def draw_boundary(self):
        pyglet.graphics.draw(8, pyglet.gl.GL_LINES,
                             ("v2f", (self.x, self.y, self.x, self.y + self.height,
                                      self.x, self.y + self.height, self.x + self.width, self.y + self.height,
                                      self.x + self.width, self.y + self.height, self.x + self.width, self.y,
                                      self.x + self.width, self.y, self.x, self.y)))

class SimpleUI(AbstractUI):
    def draw_game_field(self):
        pass

    def get_game_board_height(self):
        pass

    def draw_background(self):
        pass

    def draw_score(self, score):
        pass

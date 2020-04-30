import pyglet
import resources


def configure_resources():
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


class Menu:
    def __init__(self):
        self.set_menu_window()
        configure_resources()
        self.load_labels()
        self.load_images()

    def set_menu_window(self):
        display = pyglet.canvas.Display()
        screen = display.get_default_screen()
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.menu_window = pyglet.window.Window(self.screen_width, self.screen_height)
        self.menu_window.on_draw = self.on_menu_window_draw
        self.menu_window.on_mouse_press = self.on_mouse_press
        self.menu_window.on_mouse_motion = self.on_mouse_motion

    def load_images(self):
        snake_image = pyglet.resource.image("snake_background.jpg")
        button_background_image = pyglet.resource.image("button_background.png")
        center_image(snake_image)
        center_image(button_background_image)
        self.snake = pyglet.sprite.Sprite(img=snake_image, x=(self.screen_width // 2), y=(self.screen_height // 2))
        self.button_background = pyglet.sprite.Sprite(img=button_background_image,
                                                      x=self.play_label.x, y=self.play_label.y)
        self.button_background.opacity = 100

    def load_labels(self):
        pyglet.font.add_file("resources/Bangers/Bangers-Regular.ttf")

        self.game_name_label = pyglet.text.Label(text="Genius Snake",
                                                 x=(self.screen_width // 2), y=((self.screen_height // 6) * 5),
                                                 anchor_x="center",
                                                 font_name="Bangers", font_size=80)
        self.game_name_shadow_label = pyglet.text.Label(text="Genius Snake",
                                                        x=(self.screen_width // 2) + 10,
                                                        y=(((self.screen_height // 6) * 5) - 10),
                                                        anchor_x="center", color=(100, 0, 75, 255),
                                                        font_name="Bangers", font_size=80)
        self.play_label = pyglet.text.Label(text="Play",
                                            x=(self.screen_width // 2),
                                            y=((self.screen_height // 6) * 2),
                                            anchor_x="center", anchor_y="center",
                                            font_name="Bangers", font_size=50)

    @classmethod
    def run_application(cls):
        pyglet.app.run()

    def on_menu_window_draw(self):
        self.snake.draw()
        self.game_name_shadow_label.draw()
        self.game_name_label.draw()
        self.button_background.draw()
        self.play_label.draw()

    def mouse_on_play_button(self, x, y):
        if ((self.button_background.x - (self.button_background.width // 2) < x)
                & (x < self.button_background.x + self.button_background.width)
                & (self.button_background.y - (self.button_background.height // 2) < y)
                & (y < self.button_background.y + self.button_background.height)):
            return True
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        # play clicked
        if self.mouse_on_play_button(x, y):
            print("PLAY")  # TODO: play button clicked

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_on_play_button(x, y):
            self.button_background.opacity = 255
        else:
            self.button_background.opacity = 100

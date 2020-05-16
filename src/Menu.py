import pyglet
from src.ui import NiceUI
from src import PlayerController, AStarController, HamiltonController
from src import Constants, Game, CommonHelpers, GeneticProgramming


class Menu:
    """
    Sets up the window, starts the program, displays menu, handles user's input
    """

    def __init__(self):
        """ object properties, initialized in following methods """
        self.controller = None
        self.screen_width = self.screen_height = self.window = None
        self.snake_background = None
        self.button_play_background = self.button_genetic_background = None
        self.button_a_star_background = self.button_hamilton_background = None
        self.game_name_label = self.game_name_shadow_label = None
        self.play_label = self.genetic_label = self.a_star_label = self.hamilton_label = None

        self.set_window()
        CommonHelpers.configure_resources()
        self.load_labels()
        self.load_images()

    @classmethod
    def run_application(cls):
        pyglet.app.run()

    def set_window(self):
        display = pyglet.canvas.Display()
        screen = display.get_default_screen()
        self.screen_width = screen.width
        self.screen_height = screen.height
        config = pyglet.gl.Config(double_buffer=False)
        self.window = pyglet.window.Window(self.screen_width, self.screen_height, config=config)
        self.window.push_handlers(on_draw=self.on_menu_draw,
                                  on_mouse_press=self.on_menu_mouse_press,
                                  on_mouse_motion=self.on_menu_mouse_motion)

    def load_images(self):
        snake_image = pyglet.resource.image("Menu/snake_background.jpg")
        button_background_image = pyglet.resource.image("Menu/button_background.png")
        CommonHelpers.scale_image(button_background_image,
                                  self.genetic_label.content_width + 100, self.genetic_label.content_height + 30)
        CommonHelpers.center_image(snake_image)
        CommonHelpers.center_image(button_background_image)
        self.snake_background = pyglet.sprite.Sprite(img=snake_image, x=(self.screen_width // 2),
                                                     y=(self.screen_height // 2))
        self.button_play_background = pyglet.sprite.Sprite(img=button_background_image,
                                                           x=self.play_label.x, y=self.play_label.y)
        self.button_genetic_background = pyglet.sprite.Sprite(img=button_background_image,
                                                              x=self.genetic_label.x, y=self.genetic_label.y)
        self.button_a_star_background = pyglet.sprite.Sprite(img=button_background_image,
                                                             x=self.a_star_label.x, y=self.a_star_label.y)
        self.button_hamilton_background = pyglet.sprite.Sprite(img=button_background_image,
                                                               x=self.hamilton_label.x, y=self.hamilton_label.y)
        self.button_play_background.opacity = 100
        self.button_genetic_background.opacity = 100
        self.button_a_star_background.opacity = 100
        self.button_hamilton_background.opacity = 100

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
                                            y=((self.screen_height // 8) * 4),
                                            anchor_x="center", anchor_y="center",
                                            font_name="Bangers", font_size=50)
        self.genetic_label = pyglet.text.Label(text="Genetic programming",
                                               x=(self.screen_width // 2),
                                               y=((self.screen_height // 8) * 3),
                                               anchor_x="center", anchor_y="center",
                                               font_name="Bangers", font_size=50)
        self.a_star_label = pyglet.text.Label(text="A* Algorithm",
                                              x=(self.screen_width // 2),
                                              y=((self.screen_height // 8) * 2),
                                              anchor_x="center", anchor_y="center",
                                              font_name="Bangers", font_size=50)
        self.hamilton_label = pyglet.text.Label(text="Hamiltonian cycle",
                                                x=(self.screen_width // 2),
                                                y=(self.screen_height // 8),
                                                anchor_x="center", anchor_y="center",
                                                font_name="Bangers", font_size=50)

    def on_menu_draw(self):
        self.snake_background.draw()
        self.game_name_shadow_label.draw()
        self.game_name_label.draw()
        self.button_play_background.draw()
        self.button_genetic_background.draw()
        self.button_a_star_background.draw()
        self.button_hamilton_background.draw()
        self.play_label.draw()
        self.genetic_label.draw()
        self.a_star_label.draw()
        self.hamilton_label.draw()
        pyglet.gl.glFlush()

    def on_menu_mouse_press(self, x, y, button, modifiers):
        # play clicked
        if CommonHelpers.mouse_on_button(self.button_play_background, x, y):
            self.window.pop_handlers()
            self.button_play_background.opacity = 100
            self.window.push_handlers(on_mouse_press=self.on_back_mouse_press)
            self.window.clear()
            ui = NiceUI.NiceUI(10, 80, self.screen_width - 20, self.screen_height - 90, 50)
            game = Game.Game(ui)
            game.ui.prepare_game(game.snake)
            game.put_apple()
            self.controller = PlayerController.PlayerController(self.window, game)
        if CommonHelpers.mouse_on_button(self.button_genetic_background, x, y):
            self.window.pop_handlers()
            self.button_genetic_background.opacity = 100
            self.window.push_handlers(on_mouse_press=self.on_back_mouse_press)
            self.window.clear()
            self.controller = GeneticProgramming.GeneticProgramming(self.window, self.screen_width, self.screen_height)
        if CommonHelpers.mouse_on_button(self.button_a_star_background, x, y):
            self.window.pop_handlers()
            self.button_a_star_background.opacity = 100
            self.window.push_handlers(on_mouse_press=self.on_back_mouse_press)
            self.window.clear()
            ui = NiceUI.NiceUI(10, 80, self.screen_width - 20, self.screen_height - 90, 50)
            game = Game.Game(ui)
            game.ui.prepare_game(game.snake)
            game.put_apple()
            self.controller = AStarController.AStarController(game)
        if CommonHelpers.mouse_on_button(self.button_hamilton_background, x, y):
            self.window.pop_handlers()
            self.button_hamilton_background.opacity = 100
            self.window.push_handlers(on_mouse_press=self.on_back_mouse_press)
            self.window.clear()
            ui = NiceUI.NiceUI(10, 80, self.screen_width - 20, self.screen_height - 90, 50)
            game = Game.Game(ui)
            game.ui.prepare_game(game.snake)
            game.put_apple()
            self.controller = HamiltonController.HamiltonController(game)

    def on_back_mouse_press(self, x, y, button, modifiers):
        if self.controller.state is not Constants.PLAY:
            self.window.clear()
            self.on_menu_draw()
            self.window.pop_handlers()
            self.window.push_handlers(on_draw=self.on_menu_draw,
                                      on_mouse_press=self.on_menu_mouse_press,
                                      on_mouse_motion=self.on_menu_mouse_motion)

    def on_menu_mouse_motion(self, x, y, dx, dy):
        if CommonHelpers.mouse_on_button(self.button_play_background, x, y):
            self.button_play_background.opacity = 255
        else:
            self.button_play_background.opacity = 100
        if CommonHelpers.mouse_on_button(self.button_genetic_background, x, y):
            self.button_genetic_background.opacity = 255
        else:
            self.button_genetic_background.opacity = 100
        if CommonHelpers.mouse_on_button(self.button_a_star_background, x, y):
            self.button_a_star_background.opacity = 255
        else:
            self.button_a_star_background.opacity = 100
        if CommonHelpers.mouse_on_button(self.button_hamilton_background, x, y):
            self.button_hamilton_background.opacity = 255
        else:
            self.button_hamilton_background.opacity = 100

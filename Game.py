import Controller
import UI
import Snake


class Game:
    def __init__(self, controller: Controller.AbstractController, ui: UI.AbstractUI):
        self.controller = controller
        self.ui = ui
        self.score = 0
        self.game_field_height = self.ui.get_num_squares_height()
        self.game_field_width = self.ui.get_num_squares_width()
        self.snake = Snake.Snake()
        self.prepare_game()

    def prepare_game(self):
        self.ui.draw_boundary()
        self.ui.draw_background()
        self.ui.draw_score(self.score)
        self.ui.draw_game_field()
        self.ui.draw_snake(self.snake)

import Constants
import pyglet


class PlayerController:
    def __init__(self, window, game):
        super().__init__()
        self.window = window
        self.window.push_handlers(on_key_press=self.on_key_press)
        self.game = game
        self.next_move = Constants.SNAKE_MOVE_FORWARD

        pyglet.clock.schedule_interval(self.control, 1/3)

    def control(self, dt):
        self.game.make_next_move(self.next_move)
        self.next_move = Constants.SNAKE_MOVE_FORWARD

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.next_move = self.game.get_move_from_direction(Constants.UP)
        elif symbol == pyglet.window.key.RIGHT:
            self.next_move = self.game.get_move_from_direction(Constants.RIGHT)
        elif symbol == pyglet.window.key.DOWN:
            self.next_move = self.game.get_move_from_direction(Constants.DOWN)
        elif symbol == pyglet.window.key.LEFT:
            self.next_move = self.game.get_move_from_direction(Constants.LEFT)

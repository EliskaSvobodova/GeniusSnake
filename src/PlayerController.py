from src import Constants
import pyglet


class PlayerController:
    def __init__(self, window, game):
        super().__init__()
        self.window = window
        self.window.push_handlers(on_key_press=self.on_key_press)
        self.game = game
        self.speed = self.game.speed
        self.next_move = Constants.SNAKE_MOVE_FORWARD
        self.state = Constants.PLAY
        pyglet.clock.schedule_interval(self.control, self.speed)

    def control(self, dt):
        self.game.make_next_move(self.next_move)
        if self.speed != self.game.speed:
            self.speed = self.game.speed
            pyglet.clock.unschedule(self.control)
            pyglet.clock.schedule_interval(self.control, self.speed)
        if self.game.game_state is Constants.WIN:
            pyglet.clock.unschedule(self.control)
            self.window.pop_handlers()
            self.state = Constants.WIN
        elif self.game.game_state is Constants.LOOSE:
            pyglet.clock.unschedule(self.control)
            self.window.pop_handlers()
            self.state = Constants.LOOSE
        else:
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

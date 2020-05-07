import Constants
import SimpleUI
import NoUI
import Game
import GeneticController
import pyglet

size_of_population = 20


class GeneticProgramming:
    def __init__(self, window, screen_width, screen_height):
        self.state = Constants.PLAY
        self.window = window
        self.screen_width = screen_width - 20  # not to edges, leave some space
        self.screen_height = screen_height - 90
        self.x = 10
        self.y = 80
        self.layout = tuple([2, 4])
        self.game_width = self.screen_width // self.layout[1]
        self.game_height = self.screen_height // self.layout[0]
        self.ui = SimpleUI.ControlPaneUI(self.x, self.y + (self.layout[0] - 1) * self.game_height,
                                         self.game_width, self.game_height)
        self.population = []
        self.randomly_initialize_population()
        self.run()

    def randomly_initialize_population(self):
        # first few individuals which will draw themselves
        for i in range(self.layout[0]):
            for j in range(self.layout[1]):
                if i != (self.layout[0] - 1) or j != 0:
                    ui = SimpleUI.SimpleUI(self.x + j * self.game_width, self.y + i * self.game_height,
                                           self.game_width, self.game_height, 20)
                    game = Game.Game(ui)
                    controller = GeneticController.GeneticController(game)
                    self.population.append(controller)
        # rest of the population that will not draw itself (in the beginning)
        for i in range(size_of_population - ((self.layout[0] * self.layout[1]) - 1)):
            ui = NoUI.NoUI(0, 0,  # some dummy values
                           self.game_width, self.game_height, 20)
            game = Game.Game(ui)
            controller = GeneticController.GeneticController(game)
            self.population.append(controller)

    def run(self):
        self.still_running = self.population
        pyglet.clock.schedule_interval(self.make_next_move_with_all, 1 / 15)

    def make_next_move_with_all(self, dt):
        last_draw_index = (self.layout[0] * self.layout[1]) - 1 - 1
        for individual in self.still_running:
            individual.make_next_move()
            if individual.state is not Constants.PLAY:
                self.still_running.remove(individual)
                if len(self.still_running) >= 7 and isinstance(individual.game.ui, SimpleUI.SimpleUI):
                    self.still_running[last_draw_index].game.ui = SimpleUI.SimpleUI(
                        individual.game.ui.x, individual.game.ui.y,
                        individual.game.ui.width, individual.game.ui.height,
                        individual.game.ui.square_size)
                    game = self.still_running[last_draw_index].game
                    self.still_running[last_draw_index].game.ui.redraw(game.snake, game.score, game.apple)
        if len(self.still_running) == 0:
            self.state = Constants.WIN  # not PLAY
            pyglet.clock.unschedule(self.make_next_move_with_all)

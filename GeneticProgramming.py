import Constants
import SimpleUI
import Game


size_of_population = 7      # MUST be odd number


class GeneticProgramming:
    def __init__(self, window, screen_width, screen_height):
        self.state = Constants.PLAY
        self.window = window
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.population = self.randomly_initialize_pop()

    def randomly_initialize_pop(self):
        ui = SimpleUI.SimpleUI(10, 80, self.screen_width - 20, self.screen_height - 90, 50)
        game = Game.Game(ui)
        return game

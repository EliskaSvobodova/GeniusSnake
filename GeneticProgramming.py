import Constants
import SimpleUI
import Game
import GeneticController


size_of_population = 7


class GeneticProgramming:
    def __init__(self, window, screen_width, screen_height):
        self.state = Constants.PLAY
        self.window = window
        self.screen_width = screen_width - 20       # not to edges, leave some space
        self.screen_height = screen_height - 90
        self.x = 10
        self.y = 80
        self.layout = tuple([2, 4])
        self.game_width = self.screen_width // self.layout[1]
        self.game_height = self.screen_height // self.layout[0]
        self.ui = SimpleUI.ControlPaneUI(self.x, self.y + (self.layout[0] - 1)*self.game_height, self.game_width, self.game_height)
        self.population = []
        self.randomly_initialize_pop()

    def randomly_initialize_pop(self):
        for i in range(self.layout[0]):
            for j in range(self.layout[1]):
                if i != (self.layout[0] - 1) or j != 0:
                    ui = SimpleUI.SimpleUI(self.x + j*self.game_width, self.y + i*self.game_height, self.game_width, self.game_height, 20)
                    game = Game.Game(ui)
                    controller = GeneticController.GeneticController(game)
                    self.population.append(controller)
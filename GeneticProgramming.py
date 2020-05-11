import Constants
import SimpleUI
import NoUI
import Game
import GeneticController
import pyglet
import random
import Settings
from statistics import mean


class GeneticProgramming:
    def __init__(self, window, screen_width, screen_height):
        self.state = Constants.PLAY
        self.window = window
        self.screen_width = screen_width - 20  # not to edges, leave some space
        self.screen_height = screen_height - 90
        self.x = 10
        self.y = 80
        self.layout = Settings.genetic_layout
        self.game_width = self.screen_width // self.layout[1]
        self.game_height = self.screen_height // self.layout[0]
        self.square_size = Settings.genetic_square_size
        self.ui = SimpleUI.ControlPaneUI(self.x + 10, self.y + (self.layout[0] - 1) * self.game_height + 10,
                                         self.game_width - 20, self.game_height - 20)
        self.generation = 0
        self.ui.draw(self.generation)
        self.population = []
        self.randomly_initialize_population()
        self.test_fitness()

    def randomly_initialize_population(self):
        # first few individuals which will draw themselves
        for i in range(self.layout[0]):
            for j in range(self.layout[1]):
                if i != (self.layout[0] - 1) or j != 0:
                    ui = SimpleUI.SimpleUI(self.x + j * self.game_width, self.y + i * self.game_height,
                                           self.game_width, self.game_height, self.square_size)
                    game = Game.Game(ui)
                    controller = GeneticController.GeneticController(game)
                    self.population.append(controller)
        # rest of the population that will not draw itself (in the beginning)
        for i in range(Settings.size_of_population - ((self.layout[0] * self.layout[1]) - 1)):
            ui = NoUI.NoUI(0, 0,  # some dummy values
                           self.game_width, self.game_height, self.square_size)
            game = Game.Game(ui)
            controller = GeneticController.GeneticController(game)
            self.population.append(controller)
        if Settings.print_initial:
            print("Initial population:")
            for i in self.population:
                i.root.print()
                print()
            print()

    def test_fitness(self):
        for individual in self.population:
            individual.game = Game.Game(NoUI.NoUI(0, 0, self.game_width, self.game_height, self.square_size))
        index = 0
        for i in range(self.layout[0]):
            for j in range(self.layout[1]):
                if i != (self.layout[0] - 1) or j != 0:
                    ui = SimpleUI.SimpleUI(self.x + j * self.game_width, self.y + i * self.game_height,
                                           self.game_width, self.game_height, self.square_size)
                    game = self.population[index].game
                    game.ui = ui
                    game.ui.redraw(game.snake, game.score, game.apple)
                    index += 1
        self.still_running = self.population.copy()
        pyglet.clock.schedule(self.make_next_move_with_all)

    def make_next_move_with_all(self, dt):
        last_draw_index = (self.layout[0] * self.layout[1]) - 1 - 1
        for individual in self.still_running:
            individual.make_next_move()
            if individual.state is not Constants.PLAY:
                controller = self.population[self.population.index(individual)]
                controller.num_runs += 1
                controller.scores.append(individual.game.score)
                if controller.num_runs >= Settings.num_runs:
                    controller.average_score = mean(controller.scores)
                    self.still_running.remove(individual)
                    if len(self.still_running) >= 7 and isinstance(individual.game.ui, SimpleUI.SimpleUI):
                        self.still_running[last_draw_index].game.ui = SimpleUI.SimpleUI(
                            individual.game.ui.x, individual.game.ui.y,
                            individual.game.ui.width, individual.game.ui.height,
                            individual.game.ui.square_size)
                        game = self.still_running[last_draw_index].game
                        self.still_running[last_draw_index].game.ui.redraw(game.snake, game.score, game.apple)
                else:
                    individual.game = Game.Game(individual.game.ui)
        if len(self.still_running) == 0:
            pyglet.clock.unschedule(self.make_next_move_with_all)
            self.move_to_next_generation()

    def move_to_next_generation(self):
        self.substitute_population()
        self.population.sort(key=self.get_fitness)
        mutants = []
        for i in self.population:
            if random.random() <= Settings.mutation_rate:
                mutants.append(i.mutate())
        fitness_sum = sum([self.get_fitness(i) for i in self.population])
        index_sum = ((Settings.size_of_population - 1) * Settings.size_of_population) // 2
        offsprings = []
        parent1 = parent2 = None
        for i in range(Settings.num_of_offsprings):
            if Settings.selection_operator == Constants.FITNESS_SELECTION:
                parent1 = self.select_parent_fitness(fitness_sum)
                parent2 = self.select_parent_fitness(fitness_sum)
            elif Settings.selection_operator == Constants.RANK_SELECTION:
                parent1 = self.select_parent_rank(index_sum)
                parent2 = self.select_parent_rank(index_sum)
            else:
                raise ValueError("Wrong selection operator in settings!")
            offs1, offs2 = parent1.crossover(parent2)
            offsprings.append(offs1)
            offsprings.append(offs2)

        self.population += mutants
        self.population += offsprings
        for i in range(Settings.num_of_random):
            ui = NoUI.NoUI(0, 0, self.game_width, self.game_height, self.square_size)
            game = Game.Game(ui)
            controller = GeneticController.GeneticController(game)
            self.population.append(controller)
        self.generation += 1
        self.ui.draw(self.generation)
        self.test_fitness()

    def select_parent_rank(self, index_sum):
        tmp = 0
        r = random.randint(0, index_sum)
        for i in range(Settings.size_of_population - 1, 0, -1):
            tmp += i
            if r <= tmp:
                return self.population[i]

    def select_parent_fitness(self, fitness_sum):
        tmp = 0
        r = random.randint(0, fitness_sum)
        for individual in self.population:
            tmp += self.get_fitness(individual)
            if r <= tmp:
                return individual

    def get_fitness(self, individual):
        return individual.average_score

    def substitute_population(self):
        self.population.sort(key=self.get_fitness, reverse=True)
        if Settings.print_best:
            self.print_best()
        del self.population[Settings.size_of_population:]
        if Settings.print_all:
            print("Population:")
            for i in self.population:
                print("Score: ", i.game.score)
                i.root.print()
                print()
                print()

    def print_best(self):
        print("-----------------------------------------------------------")
        print(f"Generation {self.generation}")
        print("Best individual: ", end="")
        best = self.population[0]
        best.root.print()
        print()
        print("Scores: ", best.scores)
        print("Average score: ", best.average_score)

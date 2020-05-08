import Constants
import SimpleUI
import NoUI
import Game
import GeneticController
import pyglet
import random

size_of_population = 20
num_of_offsprings = 20
mutation_rate = 0.1


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
        self.square_size = 20
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
                    controller = GeneticController.GeneticController(game, GeneticController.generate_test_tree(game))
                    self.population.append(controller)
        # rest of the population that will not draw itself (in the beginning)
        for i in range(size_of_population - ((self.layout[0] * self.layout[1]) - 1)):
            ui = NoUI.NoUI(0, 0,  # some dummy values
                           self.game_width, self.game_height, self.square_size)
            game = Game.Game(ui)
            controller = GeneticController.GeneticController(game)
            self.population.append(controller)

    def test_fitness(self):
        self.still_running = self.population.copy()
        #pyglet.clock.schedule_interval(self.make_next_move_with_all, 1 / 20)
        pyglet.clock.schedule(self.make_next_move_with_all)

    def make_next_move_with_all(self, dt):
        last_draw_index = (self.layout[0] * self.layout[1]) - 1 - 1
        for individual in self.still_running:
            individual.make_next_move()
            if individual.state is not Constants.PLAY:
                self.population[self.population.index(individual)].game.score = individual.game.score
                self.still_running.remove(individual)
                if len(self.still_running) >= 7 and isinstance(individual.game.ui, SimpleUI.SimpleUI):
                    self.still_running[last_draw_index].game.ui = SimpleUI.SimpleUI(
                        individual.game.ui.x, individual.game.ui.y,
                        individual.game.ui.width, individual.game.ui.height,
                        individual.game.ui.square_size)
                    game = self.still_running[last_draw_index].game
                    self.still_running[last_draw_index].game.ui.redraw(game.snake, game.score, game.apple)
        if len(self.still_running) == 0:
            pyglet.clock.unschedule(self.make_next_move_with_all)
            self.move_to_next_generation()

    def move_to_next_generation(self):
        index_sum = ((size_of_population - 1) * size_of_population) // 2
        self.population.sort(key=self.get_fitness)
        self.substitute_population()
        offsprings = []
        for i in range(num_of_offsprings):
            parent1 = self.select_parent(index_sum)
            parent2 = self.select_parent(index_sum)
            offs1, offs2 = parent1.crossover(parent2)
            if random.random() <= mutation_rate:
                offs1.mutate()
            if random.random() <= mutation_rate:
                offs2.mutate()
            offsprings.append(offs1)
            offsprings.append(offs2)
        self.population += offsprings
        self.generation += 1
        self.ui.draw(self.generation)
        self.test_fitness()

    def select_parent(self, index_sum):
        tmp = 0
        r = random.randint(0, index_sum)
        for i in range(size_of_population - 1, 0, -1):
            tmp += i
            if r <= tmp:
                return self.population[i]

    def get_fitness(self, individual):
        return individual.game.score

    def substitute_population(self):
        print("-----------------------------------------------------------")
        print(f"Generation {self.generation}")
        i = 0
        next_population = []
        self.population.reverse()
        for individual in self.population:
            print("Score: ", individual.game.score)
            individual.game = Game.Game(NoUI.NoUI(0, 0, self.game_width, self.game_height, self.square_size))
            next_population.append(individual)
            individual.root.print()
            print()
            print()
            i += 1
            if i >= size_of_population:
                break
        self.population = next_population

        # first few individuals which will draw themselves
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


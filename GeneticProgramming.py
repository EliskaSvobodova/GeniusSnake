import Constants
import SimpleUI
import NoUI
import Game
import GeneticController
import pyglet
import random
import Settings
from statistics import mean
import FinalUI


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
        self.best_average_in_generations = []
        self.ui.draw(self.generation)
        self.winners = []
        self.still_running = []
        self.population = []
        if Settings.initialization_operator is Constants.GROW_INIT:
            self.initialize_grow()
        elif Settings.initialization_operator is Constants.FULL_INIT:
            self.initialize_full()
        elif Settings.initialization_operator is Constants.RAMPED_HALF_AND_HALF_INIT:
            self.initialize_ramped_half_and_half()
        else:
            raise ValueError("Wrong initialization operator in settings!")
        if Settings.print_initial:
            self.print_initial()
        self.draw_initial()
        self.test_fitness()

    def initialize_ramped_half_and_half(self):
        for i in range(1, Settings.max_depth + 1):
            for j in range(0, (Settings.size_of_population // (2 * Settings.max_depth)) + 1):
                # grow initialization method
                ui = NoUI.NoUI(0, 0, self.game_width, self.game_height, self.square_size)
                tree, num_nodes = GeneticController.generate_tree(0, 1, i)
                controller = GeneticController.GeneticController(Game.Game(ui), tree, num_nodes)
                self.population.append(controller)
                # full initialization method
                ui = NoUI.NoUI(0, 0, self.game_width, self.game_height, self.square_size)
                tree, num_nodes = GeneticController.generate_tree(0, i, i)
                controller = GeneticController.GeneticController(Game.Game(ui), tree, num_nodes)
                self.population.append(controller)

    def initialize_grow(self):
        self.initialize_population_with_min_max_depth(1, Settings.max_depth)

    def initialize_full(self):
        self.initialize_population_with_min_max_depth(Settings.max_depth, Settings.max_depth)

    def initialize_population_with_min_max_depth(self, min_depth, max_depth):
        for i in range(Settings.size_of_population):
            ui = NoUI.NoUI(0, 0,  # some dummy values
                           self.game_width, self.game_height, self.square_size)
            tree, num_nodes = GeneticController.generate_tree(0, min_depth, max_depth)
            controller = GeneticController.GeneticController(Game.Game(ui), tree, num_nodes)
            self.population.append(controller)

    def draw_initial(self):
        index = 0
        for i in range(self.layout[0]):
            for j in range(self.layout[1]):
                if i != (self.layout[0] - 1) or j != 0:
                    ui = SimpleUI.SimpleUI(self.x + j * self.game_width, self.y + i * self.game_height,
                                           self.game_width, self.game_height, self.square_size)
                    individual = self.population[index]
                    individual.game.ui = ui
                    individual.game.ui.prepare_game(individual.game.snake)
                    individual.game.ui.draw_identifier(individual.id, individual.num_runs + 1)
                    index += 1

    def test_fitness(self):
        for individual in self.population:
            individual.game = Game.Game(NoUI.NoUI(0, 0, self.game_width, self.game_height, self.square_size))
        index = 0
        for i in range(self.layout[0]):
            for j in range(self.layout[1]):
                if i != (self.layout[0] - 1) or j != 0:
                    ui = SimpleUI.SimpleUI(self.x + j * self.game_width, self.y + i * self.game_height,
                                           self.game_width, self.game_height, self.square_size)
                    individual = self.population[index]
                    individual.game.ui = ui
                    individual.game.ui.redraw(individual.game.snake, individual.game.score,
                                              individual.id, individual.num_runs, individual.game.apple)
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
                    if individual.average_score == Settings.max_score:
                        self.winners.append(individual)
                    self.still_running.remove(individual)
                    if len(self.still_running) >= 7 and isinstance(individual.game.ui, SimpleUI.SimpleUI):
                        self.still_running[last_draw_index].game.ui = SimpleUI.SimpleUI(
                            individual.game.ui.x, individual.game.ui.y,
                            individual.game.ui.width, individual.game.ui.height,
                            individual.game.ui.square_size)
                        game = self.still_running[last_draw_index].game
                        self.still_running[last_draw_index].game.ui.redraw(game.snake, game.score,
                                                                           self.still_running[last_draw_index].id,
                                                                           self.still_running[last_draw_index].num_runs,
                                                                           game.apple)
                else:
                    individual.game = Game.Game(individual.game.ui)
                    individual.game.ui.redraw(individual.game.snake, individual.game.score,
                                              individual.id, individual.num_runs, individual.game.apple)
        if len(self.still_running) == 0:
            pyglet.clock.unschedule(self.make_next_move_with_all)
            if len(self.winners) != 0:
                self.genetic_programming_successful()
            else:
                self.move_to_next_generation()

    def move_to_next_generation(self):
        self.generation += 1
        if self.generation > Settings.max_generations:
            self.max_num_generations_reached()
            return
        self.substitute_population()
        self.population.sort(key=get_fitness)
        # first produce all new individuals, then add them
        mutants = self.produce_mutants()
        offsprings = self.produce_offsprings()
        rand_individuals = self.produce_additional_random_individuals()
        self.population += mutants
        self.population += offsprings
        self.population += rand_individuals
        self.ui.draw(self.generation)
        self.test_fitness()

    def produce_additional_random_individuals(self):
        rand_individuals = []
        for i in range(Settings.num_of_random):
            ui = NoUI.NoUI(0, 0, self.game_width, self.game_height, self.square_size)
            game = Game.Game(ui)
            controller = GeneticController.GeneticController(game)
            rand_individuals.append(controller)
        return rand_individuals

    def produce_offsprings(self):
        fitness_sum = sum([get_fitness(i) for i in self.population])
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
        return offsprings

    def produce_mutants(self):
        mutants = []
        for i in self.population:
            if random.random() <= Settings.mutation_rate:
                mutants.append(i.mutate())
        return mutants

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
            tmp += get_fitness(individual)
            if r <= tmp:
                return individual

    def substitute_population(self):
        self.population.sort(key=get_fitness, reverse=True)
        self.best_average_in_generations.append(self.population[0].average_score)
        self.ui.draw_graph(self.best_average_in_generations)
        if Settings.print_best:
            self.print_best()
        del self.population[Settings.size_of_population:]
        if Settings.print_all:
            print("Population:")
            for i in self.population:
                print("Score: ", i.scores, " - ", i.average_score)
                i.root.print()
                print()
                print()

    def print_best(self):
        print("-----------------------------------------------------------")
        print(f"Generation {self.generation}")
        best = self.population[0]
        print(f"Best individual: {best.id}")
        best.root.print()
        print()
        print("Scores: ", best.scores)
        print("Average score: ", best.average_score)

    def print_results(self):
        print("-----------------------------------------------------------")
        print("-----------------------------------------------------------")
        print(f"Final Generation {self.generation}")

        for individual in self.winners:
            print(f"Individual {individual.id}:")
            individual.root.print()
            print()
            print("Scores: ", individual.scores)
            print("Average score: ", individual.average_score)
            print()
            print()

    def print_initial(self):
        print("Initial population:")
        for i in self.population:
            print(f"Individual {i.id}:")
            i.root.print()
            print()
        print()

    def final_generation_move(self, dt):
        for individual in self.still_running:
            individual.make_next_move()
            if individual.state is not Constants.PLAY:
                controller = self.population[self.population.index(individual)]
                controller.scores.append(individual.game.score)
                controller.average_score = mean(controller.scores)
                self.still_running.remove(individual)
        if len(self.still_running) == 0:
            pyglet.clock.unschedule(self.final_generation_move)
            self.state = Constants.WIN

    def max_num_generations_reached(self):
        self.population.sort(key=get_fitness, reverse=True)
        self.still_running = self.population[:(self.layout[0] * self.layout[1] - 1)]
        self.winners = self.population[:(self.layout[0] * self.layout[1] - 1)]
        self.prepare_final_run()

    def genetic_programming_successful(self):
        self.still_running = self.winners[:(self.layout[0] * self.layout[1] - 1)]
        self.prepare_final_run()

    def prepare_final_run(self):
        self.print_best()
        index = 0
        for i in range(self.layout[0]):
            for j in range(self.layout[1]):
                if i != (self.layout[0] - 1) or j != 0:
                    ui = FinalUI.FinalUI(self.x + j * self.game_width, self.y + i * self.game_height,
                                         self.game_width, self.game_height, self.square_size)
                    self.still_running[index].game = Game.Game(ui)
                    self.still_running[index].game.ui.prepare_game(self.still_running[index].game.snake)
                    index += 1
                if index == len(self.still_running):
                    break
        pyglet.clock.schedule(self.final_generation_move)


def get_fitness(individual):
    return individual.average_score

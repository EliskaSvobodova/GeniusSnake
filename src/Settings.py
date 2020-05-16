from src import Constants

""" COMMON SETTINGS """
# score required to win the game
max_score = 1000
# how long is the snake on the beginning
snake_start_length = 5
# how long snake survives without food
snake_stamina = 300


""" PLAYER MODE """
# on which speed the player starts in game mode, (ex.: snake moves each 1/3 fraction of a second)
player_snake_start_speed = 1/3
# what is the maximum speed for the player (so that the game is playable)
player_snake_max_speed = 1/15
# what score snake must reach to win the game


""" A* MODE """
a_star_snake_speed = 1/100


""" GENETIC PROGRAMMING MODE """
# number of individuals in each generation before breeding
size_of_population = 100
# number of offsprings produced in each generation
num_of_offsprings = 85
# number of additional randomly generated individuals (for diversity of genome)
num_of_random = 10
# chance that an individual will produce a mutant
mutation_rate = 0.1
# chance that mutation alters only one random node
mutate_terminal = 0.2
# chance of picking a terminal node for crossover
crossover_terminal_rate = 0.2

# limits number of generations
max_generations = 500

# max depth of the decision tree in snake's "brain"
max_depth = 6
# max number of nodes in the decision tree in snake's "brain", limited by max depth
max_nodes = sum([2**i for i in range(max_depth + 1)])
# when generating snake's decision tree randomly,
# what chance is tha the newly generated node will be a function and not a terminal
chance_new_node_function = 0.6
# how many attempts does an individual have in each generation
# the fitness is calculated as average from all runs
num_runs = 1


# printing functions, what information should be printed in the terminal
# prints best individual in each generation, its decision tree, all scores and their average
print_best = True
# prints all individuals in each generation, its decision tree, all scores and their average
print_all = False
# prints initial population, all its individual's decision trees, all scores and their averages
print_initial = False

# which selection operator should be used, for available operators look into Constants
selection_operator = Constants.RANK_SELECTION
# which initialization operator should be used, for available operators look into Constants
initialization_operator = Constants.RAMPED_HALF_AND_HALF_INIT

# number and layout of visible individuals on the screen
genetic_layout = tuple([2, 4])
# size of one square in snake's game field, with genetic_layout determines the size of game_field
genetic_square_size = 20
# how many labels should be on the y axis of the gen. programming graph
num_graph_labels = 10

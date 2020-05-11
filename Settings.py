import Constants

size_of_population = 100
num_of_offsprings = 80
num_of_random = 10
mutation_rate = 0.1

max_depth = 4
max_nodes = sum([2**i for i in range(max_depth + 1)])

genetic_layout = tuple([2, 4])
genetic_square_size = 20
chance_new_node_function = 0.6
num_runs = 3

player_snake_start_speed = 1/3
player_snake_max_speed = 1/15

max_score = 100
snake_start_length = 5

print_best = True
print_all = True
print_initial = True

selection_operator = Constants.RANK_SELECTION

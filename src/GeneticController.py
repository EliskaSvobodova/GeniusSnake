from src import Constants, Game, Settings
from src.ui import NoUI
import random
import copy


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __call__(self, game):
        if callable(self.value):
            return self.value(game, self.left(game), self.right(game))
        else:
            return self.value

    def equal(self, other):
        return self.value == other.value \
               and (self.left is None or self.left.equal(other.left)) \
               and (self.right is None or self.right.equal(other.right))

    def print(self):
        if callable(self.value):
            print("[", self.value.__name__, ":", end=" ")
        else:
            print("[", end=" ")
            Constants.print_constant(self.value)
            print(":", end=" ")
        if self.left is not None:
            self.left.print()
        else:
            print("_", end=" ")
        print(",", end=" ")
        if self.right is not None:
            self.right.print()
        else:
            print("_", end=" ")
        print("]", end="")


class GeneticController:
    id = -1

    @classmethod
    def next_id(cls):
        cls.id += 1
        return cls.id

    @classmethod
    def reset_id(cls):
        cls.id = -1

    def __init__(self, game: Game.Game, root=None, num_nodes=None):
        self.game = game
        if root is None:
            self.root, self.num_nodes = generate_tree(0, 1, Settings.max_depth)
        else:
            self.root = root
            if num_nodes is None:
                self.num_nodes = count_nodes(self.root)
            else:
                self.num_nodes = num_nodes
        self.state = Constants.PLAY
        self.num_runs = 0
        self.scores = []
        self.average_score = 0
        self.id = self.next_id()

    def make_next_move(self):
        self.game.make_next_move(self.root(self.game))
        self.state = self.game.game_state

    def __eq__(self, other):
        return self.id == other.id

    def crossover(self, other):
        r1 = random.randint(0, self.num_nodes - 1)
        new_subtree1, dummy = find_node(self.root, 0, r1)
        while True:
            if new_subtree1.left is None:
                if random.random() < Settings.crossover_terminal_rate:
                    break
                else:
                    r1 = random.randint(0, self.num_nodes - 1)
                    new_subtree1, dummy = find_node(self.root, 0, r1)
                    break
            else:
                break

        r2 = random.randint(0, other.num_nodes - 1)
        new_subtree2, dummy = find_node(other.root, 0, r2)
        while True:
            if new_subtree2.left is None:
                if random.random() < 0.2:
                    break
                else:
                    r2 = random.randint(0, other.num_nodes - 1)
                    new_subtree2, dummy = find_node(other.root, 0, r2)
                    break
            else:
                break

        offs1, dummy = replace_subtree(self.root, copy.deepcopy(new_subtree2), 0, r1)
        offs2, dummy = replace_subtree(other.root, copy.deepcopy(new_subtree1), 0, r2)
        num_nodes1 = count_nodes(new_subtree1)
        num_nodes2 = count_nodes(new_subtree2)

        offspring1 = GeneticController(
            Game.Game(NoUI.NoUI(0, 0, self.game.ui.width, self.game.ui.height, self.game.ui.square_size)), offs1)
        offspring1.num_nodes = self.num_nodes - num_nodes1 + num_nodes2
        if offspring1.num_nodes > Settings.max_nodes:
            cut_individual(offspring1)

        offspring2 = GeneticController(
            Game.Game(NoUI.NoUI(0, 0, self.game.ui.width, self.game.ui.height, self.game.ui.square_size)), offs2)
        offspring2.num_nodes = other.num_nodes - num_nodes2 + num_nodes1
        if offspring2.num_nodes > Settings.max_nodes:
            cut_individual(offspring2)

        return offspring1, offspring2

    def mutate(self):
        mutant_genome = None
        if random.random() < Settings.mutate_terminal:
            mutant_genome, dummy = replace_one_node_with_random(self.root, 0, random.randint(0, self.num_nodes))
        else:
            new_subtree, dummy = generate_tree(0, 0, Settings.max_depth)
            mutant_genome, dummy = replace_subtree(self.root,
                                                   new_subtree,
                                                   0,
                                                   random.randint(0, self.num_nodes))
        mutant = GeneticController(
            Game.Game(
                NoUI.NoUI(0, 0, self.game.ui.width, self.game.ui.height, self.game.ui.square_size)),
            mutant_genome)
        mutant.num_nodes = count_nodes(mutant_genome)
        if mutant.num_nodes > Settings.max_nodes:
            cut_individual(mutant)
        return mutant


def generate_tree(depth, min_depth, max_depth):
    if depth == max_depth:
        return TreeNode(get_random_terminal()), 1

    if depth < min_depth:
        fnc = TreeNode(get_random_function())
        fnc.left, num_nodes_left = generate_tree(depth + 1, min_depth, max_depth)
        fnc.right, num_nodes_right = generate_tree(depth + 1, min_depth, max_depth)
        return fnc, (num_nodes_left + num_nodes_right + 1)

    if random.random() < Settings.chance_new_node_function:
        fnc = TreeNode(get_random_function())
        fnc.left, num_nodes_left = generate_tree(depth + 1, min_depth, max_depth)
        fnc.right, num_nodes_right = generate_tree(depth + 1, min_depth, max_depth)
        return fnc, (num_nodes_left + num_nodes_right + 1)
    else:
        return TreeNode(get_random_terminal()), 1


def get_random_function():
    return random.choice([Game.if_food_forward,
                          Game.if_food_left,
                          Game.if_food_right,
                          Game.if_wall_forward,
                          Game.if_wall_left,
                          Game.if_wall_right,
                          Game.if_body_forward,
                          Game.if_body_left,
                          Game.if_body_right,
                          Game.if_obstacle_two_forward,
                          Game.if_is_moving_left,
                          Game.if_is_moving_up])


def get_random_terminal():
    return random.choice([Constants.SNAKE_MOVE_RIGHT, Constants.SNAKE_MOVE_LEFT, Constants.SNAKE_MOVE_FORWARD])


def count_nodes(tree):
    if tree is None:
        return 0
    count = 1
    count += count_nodes(tree.left)
    count += count_nodes(tree.right)
    return count


def cut_individual(individual):
    num_nodes = cut_tree(0, individual.root)
    individual.num_nodes = num_nodes


def cut_tree(depth, tree):
    nodes = 1
    if depth == Settings.max_depth - 1:
        if tree.left is not None:
            if tree.left.left is not None:
                tree.left = TreeNode(get_random_terminal())
            if tree.right.right is not None:
                tree.right = TreeNode(get_random_terminal())
            nodes += 2
        return nodes
    if tree.left is None:
        return 1
    nodes += cut_tree(depth + 1, tree.left)
    nodes += cut_tree(depth + 1, tree.right)
    return nodes


def find_node(tree, node_current, node_number):
    if node_number == node_current:
        return tree, node_current
    if tree.left is None:
        return None, node_current
    res, node_current = find_node(tree.left, node_current + 1, node_number)
    if res is not None:
        return res, node_current
    res, node_current = find_node(tree.right, node_current + 1, node_number)
    return res, node_current


def replace_subtree(tree, new_subtree, node_current, node_number):
    """
    Produces new tree, same as tree with node_number node replaced with new_subtree
    If node_number is bigger than total number of nodes, new is the same as tree
    """
    if node_current == node_number:
        return new_subtree, node_current
    if tree.left is None:  # it is terminal
        return TreeNode(tree.value), node_current
    # it is a function
    res_left, node_current = replace_subtree(tree.left, new_subtree, node_current + 1, node_number)
    res_right, node_current = replace_subtree(tree.right, new_subtree, node_current + 1, node_number)
    return TreeNode(tree.value, res_left, res_right), node_current


def replace_one_node_with_random(tree, current, node_number):
    node = TreeNode(tree.value)
    if current == node_number:
        orig = tree
        if tree.left is None:
            while node.value == orig.value:
                node = TreeNode(get_random_terminal())
        else:
            while node.value == orig.value:
                node = TreeNode(get_random_function())
    if tree.left is None:
        return node, current
    node.left, current = replace_one_node_with_random(tree.left, current + 1, node_number)
    node.right, current = replace_one_node_with_random(tree.right, current + 1, node_number)
    return node, current

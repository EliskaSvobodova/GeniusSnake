import Game
import Constants
import random
import copy
import NoUI


max_depth = 10


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            return self.value(self.left(), self.right())
        else:
            return self.value

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

    def __init__(self, game: Game.Game, root=None):
        self.game = game
        if root is None:
            self.root, self.num_nodes = generate_tree(0, self.game)
        else:
            self.root = root
            self.num_nodes = count_nodes(self.root)
        self.state = Constants.PLAY
        self.id = self.next_id()

    def make_next_move(self):
        self.game.make_next_move(self.root())
        self.state = self.game.game_state

    def __eq__(self, other):
        return self.id == other.id

    def crossover(self, other):
        offs1 = copy.deepcopy(self.root)
        offs2 = copy.deepcopy(other.root)
        r1 = random.randint(0, self.num_nodes - 1)
        r2 = random.randint(0, other.num_nodes - 1)
        parent_node1, son_type1 = self.find_parent_node(r1, 0, offs1)
        parent_node2, son_type2 = self.find_parent_node(r2, 0, offs2)
        # -1:root, 0:left, 1:right
        if son_type1 == -1:
            tmp = offs1
            if son_type2 == -1:
                pass  # we switch hole offsprings, no effect
            elif son_type2 == 0:
                offs1 = parent_node2.left
                offs2 = tmp
            elif son_type2 == 1:
                offs1 = parent_node2.right
                offs2 = tmp
        elif son_type1 == 0:
            tmp = parent_node1.left
            if son_type2 == -1:
                parent_node1.left = offs2
                offs2 = tmp
            elif son_type2 == 0:
                parent_node1.left = parent_node2.left
                parent_node2.left = tmp
            elif son_type2 == 1:
                parent_node1.left = parent_node2.right
                parent_node2.right = tmp
        elif son_type1 == 1:
            tmp = parent_node1.right
            if son_type2 == -1:
                parent_node1.right = offs2
                offs2 = tmp
            elif son_type2 == 0:
                parent_node1.right = parent_node2.left
                parent_node2.left = tmp
            elif son_type2 == 1:
                parent_node1.right = parent_node2.right
                parent_node2.right = tmp
        offspring1 = GeneticController(
            Game.Game(
                NoUI.NoUI(0, 0, self.game.ui.width, self.game.ui.height, self.game.ui.square_size)),
            offs1)
        offspring1.num_nodes = count_nodes(offspring1.root)
        offspring2 = GeneticController(
            Game.Game(
                NoUI.NoUI(0, 0, self.game.ui.width, self.game.ui.height, self.game.ui.square_size)),
            offs2)
        offspring2.num_nodes = count_nodes(offspring2.root)
        return offspring1, offspring2

    def find_parent_node(self, index, current, tree):
        if index == current:
            return tree, -1
        if tree.left is None:
            return None, current
        res, current = self.find_parent_node(index, current + 1, tree.left)
        if current == -1:
            return tree, 0
        if res is not None:
            return res, current
        res, current = self.find_parent_node(index, current + 1, tree.right)
        if current == -1:
            return tree, 1
        return res, current

    def find_node(self, index, current, tree):
        if index == current:
            return tree, current
        if tree.left is None:
            return None, current
        res, current = self.find_parent_node(index, current + 1, tree.left)
        if res is not None:
            return res, current
        res, current = self.find_parent_node(index, current + 1, tree.right)
        return res, current

    def mutate(self):
        r = random.randint(0, self.num_nodes - 1)
        node, dummy = self.find_node(r, 0, self.root)
        if node.left is None:
            node.value = get_random_terminal()
        else:
            node.value = get_random_function(self.game)


def generate_tree(depth, game):
    if depth == max_depth:
        return get_random_terminal_tree_node(), 1
    if random.random() < 0.5:
        fnc = get_random_function_tree_node(game)
        fnc.left, left_nodes = generate_tree(depth + 1, game)
        fnc.right, right_nodes = generate_tree(depth + 1, game)
        return fnc, (left_nodes + right_nodes + 1)
    else:
        return get_random_terminal_tree_node(), 1


def generate_test_tree_1(game):
    return TreeNode(game.if_obstacle_forward, TreeNode(Constants.SNAKE_MOVE_LEFT),
                    TreeNode(Constants.SNAKE_MOVE_FORWARD))


def generate_test_tree(game):
    return TreeNode(game.if_food_forward,
                    TreeNode(game.if_obstacle_left,
                             TreeNode(Constants.SNAKE_MOVE_RIGHT),
                             TreeNode(game.if_obstacle_right,
                                      TreeNode(Constants.SNAKE_MOVE_LEFT),
                                      TreeNode(game.if_food_left,
                                               TreeNode(Constants.SNAKE_MOVE_LEFT),
                                               TreeNode(Constants.SNAKE_MOVE_RIGHT)))),
                    TreeNode(game.if_obstacle_left,
                             TreeNode(game.if_obstacle_right,
                                      TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                      TreeNode(game.if_food_forward,
                                               TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                               TreeNode(Constants.SNAKE_MOVE_RIGHT))),
                             TreeNode(game.if_food_forward,
                                      TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                      TreeNode(Constants.SNAKE_MOVE_LEFT))))


def get_random_terminal():
    return random.choice([Constants.SNAKE_MOVE_RIGHT, Constants.SNAKE_MOVE_LEFT, Constants.SNAKE_MOVE_FORWARD])


def get_random_terminal_tree_node():
    return TreeNode(get_random_terminal())


def get_random_function(game):
    choice = random.randint(0, 5)
    if choice == 0:
        return game.if_food_forward
    elif choice == 1:
        return game.if_food_left
    elif choice == 2:
        return game.if_food_right
    elif choice == 3:
        return game.if_obstacle_forward
    elif choice == 4:
        return game.if_obstacle_left
    else:
        return game.if_obstacle_right


def get_random_function_tree_node(game):
    return TreeNode(get_random_function(game))


def count_nodes(tree):
    count = 1
    if tree.left is None:
        return count
    count += count_nodes(tree.left)
    count += count_nodes(tree.right)
    return count

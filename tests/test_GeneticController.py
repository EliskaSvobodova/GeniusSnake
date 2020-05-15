from src import Game, Constants, Settings
from src import GeneticController as gc
from src.ui import NoUI


def test_tree_node():
    s_length = 5
    Settings.snake_start_length = s_length
    game = Game.Game(NoUI.NoUI(100, 100, 10, 11, 1))
    game.apple = tuple([s_length + 1, 2])
    root = gc.TreeNode(Game.if_food_left,
                       gc.TreeNode(Constants.SNAKE_MOVE_LEFT),
                       gc.TreeNode(Game.if_wall_right,
                                   gc.TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                   gc.TreeNode(Constants.SNAKE_MOVE_RIGHT)))
    assert root(game) is Constants.SNAKE_MOVE_FORWARD
    game.make_next_move(root(game))
    assert root(game) is Constants.SNAKE_MOVE_LEFT
    game.make_next_move(root(game))
    game.apple = tuple([0, 0])
    assert root(game) is Constants.SNAKE_MOVE_RIGHT


def test_genetic_controller():
    game = Game.Game(NoUI.NoUI(100, 100, 10, 11, 1))
    root = gc.TreeNode(Game.if_food_left,
                       gc.TreeNode(Constants.SNAKE_MOVE_LEFT),
                       gc.TreeNode(Game.if_wall_right,
                                   gc.TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                   gc.TreeNode(Constants.SNAKE_MOVE_RIGHT)))
    c1 = gc.GeneticController(game)
    assert c1.id == 0
    c2 = gc.GeneticController(game, root)
    assert c2.id == 1
    assert c2.num_nodes == 5


def test_replace_subtree():
    root1 = gc.TreeNode(Game.if_food_left,
                        gc.TreeNode(Constants.SNAKE_MOVE_LEFT),
                        gc.TreeNode(Game.if_wall_right,
                                    gc.TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                    gc.TreeNode(Constants.SNAKE_MOVE_RIGHT)))
    root2 = gc.TreeNode(Game.if_wall_left,
                        gc.TreeNode(Constants.SNAKE_MOVE_RIGHT),
                        gc.TreeNode(Constants.SNAKE_MOVE_LEFT))
    root3 = gc.TreeNode(Constants.SNAKE_MOVE_FORWARD)

    replaced, dummy = gc.replace_subtree(root1, root2, 0, 1)
    correct = gc.TreeNode(Game.if_food_left,
                          gc.TreeNode(Game.if_wall_left,
                                      gc.TreeNode(Constants.SNAKE_MOVE_RIGHT),
                                      gc.TreeNode(Constants.SNAKE_MOVE_LEFT)),
                          gc.TreeNode(Game.if_wall_right,
                                      gc.TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                      gc.TreeNode(Constants.SNAKE_MOVE_RIGHT)))
    assert replaced.equal(correct)

    replaced, dummy = gc.replace_subtree(root1, root2, 0, 0)
    correct = gc.TreeNode(Game.if_wall_left,
                          gc.TreeNode(Constants.SNAKE_MOVE_RIGHT),
                          gc.TreeNode(Constants.SNAKE_MOVE_LEFT))
    assert replaced.equal(correct)

    replaced, dummy = gc.replace_subtree(root2, root3, 0, 3)
    assert replaced.equal(root2)


def test_replace_one_node_with_random():
    root = gc.TreeNode(Game.if_food_left,
                       gc.TreeNode(Constants.SNAKE_MOVE_LEFT),
                       gc.TreeNode(Game.if_wall_right,
                                   gc.TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                   gc.TreeNode(Constants.SNAKE_MOVE_RIGHT)))

    replaced, dummy = gc.replace_one_node_with_random(root, 0, 3)
    assert replaced.value == root.value
    assert replaced.left.equal(root.left)
    assert replaced.right.value == root.right.value
    assert not replaced.right.left.equal(root.right.left)
    assert replaced.right.right.equal(root.right.right)

    replaced, dummy = gc.replace_one_node_with_random(root, 0, 2)
    assert replaced.value == root.value
    assert replaced.left.equal(root.left)
    assert replaced.right.value != root.right.value
    assert replaced.right.left.equal(root.right.left)
    assert replaced.right.right.equal(root.right.right)


def test_find_node():
    root = gc.TreeNode(Game.if_food_left,
                       gc.TreeNode(Constants.SNAKE_MOVE_LEFT),
                       gc.TreeNode(Game.if_wall_right,
                                   gc.TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                   gc.TreeNode(Constants.SNAKE_MOVE_RIGHT)))

    node, dummy = gc.find_node(root, 0, 2)
    assert node.value == Game.if_wall_right

    node, dummy = gc.find_node(root, 0, 3)
    assert node.value == Constants.SNAKE_MOVE_FORWARD

    node, dummy = gc.find_node(root, 0, 1000)
    assert node is None


def test_count_nodes():
    root1 = gc.TreeNode(Game.if_food_left,
                        gc.TreeNode(Constants.SNAKE_MOVE_LEFT),
                        gc.TreeNode(Game.if_wall_right,
                                    gc.TreeNode(Constants.SNAKE_MOVE_FORWARD),
                                    gc.TreeNode(Constants.SNAKE_MOVE_RIGHT)))
    root2 = gc.TreeNode(Constants.SNAKE_MOVE_FORWARD)
    root3 = None

    assert gc.count_nodes(root1) == 5
    assert gc.count_nodes(root2) == 1
    assert gc.count_nodes(root3) == 0

import random

import numpy as np


def robot_epoch(robot):
    # Get the possible values (dirty/clean) of the tiles we can end up at after a move:
    # This is limited by the vision of the robot
    possible_tiles = robot.possible_tiles_after_move()

    columns = robot.grid.cells

    # policy = {}
    # for s in actions.keys():
    #     policy[s] = np.random.choice(actions[s])



    actions = {}
    # for column in columns:
    #     if
    #     for cell in column:
    #         policy[cell]:



    # # Define an initial policy
    # policy = {}
    # for s in possible_tiles.keys():
    #     policy[s] = np.random.choice(actions[s])


    # Hyperparameters
    SMALL_ENOUGH = 0.005
    GAMMA = 0.9
    NOISE = 0.1


    test = {
        (0, -1): -1.0,
        (1, 0): 0.0,
        (0, 1): 0.0,
        (-1, 0): -1.0,
        (2, 0): -2.0,
        (0, 2): 1.0,
        (3, 0): 1.0,
        (0, 3): 1.0,
        (4, 0): 1.0,
        (0, 4): 1.0
    }

    # test2 = [[-1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    #          [-1. -3.  1.  1.  1.  1. -2.  1. -2.  1.  1. -1.]
    #          [-1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1.]
    #          [-1. -2. -2. -2. -2. -2. -2.  1. -2. -2. -2. -1.]
    #          [-1.  1.  1.  1.  1.  1. -2.  1. -2.  1.  1. -1.]
    #          [-1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1.]
    #          [-1. -2. -2. -2. -2. -2. -2.  1. -2. -2. -2. -1.]
    #          [-1.  1.  1.  1.  1.  1. -2.  1. -2.  1.  1. -1.]
    #          [-1.  1.  1.  1.  1.  1.  1.  1.  1.  1.  1. -1.]
    #          [-1. -2. -2. -2. -2. -2. -2.  1. -2. -2. -2. -1.]
    #          [-1.  1.  1.  1.  1.  1. -2.  1. -2.  1.  1. -1.]
    #          [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]]

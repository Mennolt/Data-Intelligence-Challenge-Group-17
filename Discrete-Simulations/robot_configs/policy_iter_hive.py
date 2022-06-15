import random
import numpy as np
import sys
sys.path.append("../Discrete-Simulations")
from Rewards import get_rewards

max_iter = 100
discount = 0.5
other_robot_value = -1.0


def calculate_policies(robots):
    # Initialisation
    grid = robots[0].grid

    # Fix rewards for all robots. For each robot, the tiles on which
    # the other robots are chilling get a negative score
    all_rewards = []
    rewards = {}

    cell_rewards = grid.cells.copy()

    # But now, for each robot, we will create their own rewards data structure.
    # The difference is that for robot x, all other robots (and their surroundings)
    # will get certain values on the grid, to ensure they avoid each other.
    for robot_i, robot in enumerate(robots): # Current robot
        # This line is deprecated; we are using the get_rewards()
        # function from
        #all_rewards.append(rewards.copy())
        all_rewards.append(get_rewards(grid, robot))

        for robot_j, other_robot in enumerate(robots): # Other robot
            if robot_i != robot_j: # Only do something if they are not the same
                other_robot_i, other_robot_j = other_robot.pos
                # Give the whole 3x3 grid surrounding the other robot
                # a punishing value
                for neighbour_i in range(other_robot_i-1, other_robot_i+2):
                    for neighbour_j in range(other_robot_j-1, other_robot_j+2):
                        all_rewards[robot_i][(neighbour_i,neighbour_j)] = other_robot_value

    # Define a central actions dictionary that indicates what all
    # the possible actions are on the grid. Same for every robot
    actions = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            possible_actions = get_possible_actions(grid, (i, j))
            # Ensure only keys get added when there are actions
            if len(possible_actions) != 0:
                actions[(i, j)] = possible_actions

    # Define an initial policy for each robot
    policies = []

    # Define the random policy for a robot as usual
    for _ in robots:
        policy = {}
        for s in actions.keys():
            try:
                policy[s] = np.random.choice(actions[s])
            except: pass
        policies.append(policy)

    all_values = all_rewards.copy()
    # Policy iteration, but now takes all robots into account
    policies = policy_iteration(robots, policies, all_values, all_rewards, actions)

    return policies


def policy_iteration(robots, policies, all_values, all_rewards, actions):
    '''
    Policy iteration, where we go over all the robots.
    '''
    for i, robot in enumerate(robots):
        policy, values, rewards = policies[i].copy(), all_values[i].copy(), all_rewards[i].copy()
        for _ in range(max_iter):
            policy_prev = policy.copy()
            values = policy_evaluation(robot, policy, values, rewards)

            policy = policy_improvement(robot, policy, values, rewards, actions)
            policies[i] = policy

            # Early stopping
            if policy_prev == policy:
                #print('stopped early convergence (main)')
                break
    return policies


def policy_evaluation(robot, policy, values, rewards):
    '''
    Evaluation of policy

    Input:
    robot - a Robot object used to interact with the environment
    '''
    for _ in range(max_iter):
        V_prev = values.copy()
        # Calculate weighted score of state after each possible action
        for s in policy.keys():
            a = policy[s]
            values[s] = rewards[s] + discount * V_prev[get_next_state(s, a)]
        # Early stopping
        if V_prev == values:
            #print('stopped early convergence (eval)')
            break
    return values


def policy_improvement(robot, policy, values, rewards, actions):
    '''
    Improvement update pass in policy

    Input:
    robot - a Robot object used to interact with the environment
    '''
    # Calculate Q value
    Q = {}
    # Calculate weighted score of each possible action
    for i in range(robot.grid.n_cols):
        for j in range(robot.grid.n_rows):
            s = (i,j)
            Q = {}
            try:
                for a in actions[s]:
                    Q[a] = rewards[s] + discount * values[get_next_state(s, a)]
                try:
                    policy[s] = max(Q, key=Q.get)
                except: pass
            except: pass
    return policy


def get_next_state(s, a):
    if a == 'e':
        try: return (s[0]+1, s[1])
        except IndexError: return (s[0], s[1])
    if a == 's':
        try: return (s[0], s[1]+1)
        except IndexError: return (s[0], s[1])
    if a == 'w':
        try: return (s[0]-1, s[1])
        except IndexError: return (s[0], s[1])
    if a == 'n':
        try: return (s[0], s[1]-1)
        except IndexError: return (s[0], s[1]) 


def get_possible_actions(grid, s):
    possible_actions = []
    try:
        if grid.cells[s[0]+1, s[1]] >= 0:
            possible_actions.append("e")
    except IndexError: pass
    try:
        if grid.cells[s[0], s[1]+1] >= 0:
            possible_actions.append("s")
    except IndexError: pass
    try:
        if grid.cells[s[0]-1, s[1]] >= 0:
            possible_actions.append("w")
    except IndexError: pass
    try:
        if grid.cells[s[0], s[1]-1] >= 0:
            possible_actions.append("n")
    except IndexError: pass
    return possible_actions
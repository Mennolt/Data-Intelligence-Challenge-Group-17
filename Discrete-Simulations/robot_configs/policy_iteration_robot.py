import random
import numpy as np

max_iter = 100
discount = 0.5

def robot_epoch(robot):
    # Initialisation
    grid = robot.grid

    rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            rewards[(i,j)] = grid.cells[i, j]

    values = rewards.copy()

    actions = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            possible_actions = get_possible_actions(grid, (i, j))
            # Ensure only keys get added when there are actions
            if len(possible_actions) != 0:
                actions[(i, j)] = possible_actions
            

    # Define an initial policy
    policy = {}

    for s in actions.keys():
        try:
            policy[s] = np.random.choice(actions[s])
        except: pass
    # Policy iteration
    policy = policy_iteration(robot, policy, values, rewards, actions)
    # Randomly select where to go based on policy
    best_direction = policy[robot.pos]
    while robot.orientation != best_direction:
        robot.rotate('r')
    robot.move()
    print('moved', best_direction)


def policy_iteration(robot, policy, values, rewards, actions):
    '''
    Policy iteration

    Input:
    robot - a Robot object used to interact with the environment
    '''
    # print('Policy iteration')
    for _ in range(max_iter):
        policy_prev = policy.copy()

        values = policy_evaluation(robot, policy, values, rewards)

        policy = policy_improvement(robot, policy, values, rewards, actions)

        # Early stopping
        if policy_prev == policy:
            print('stopped early convergence')
            break
    return policy


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
            print('stopped early convergence')
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
    #adjust for bigger robots?
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
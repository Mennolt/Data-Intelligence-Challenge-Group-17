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

            val = grid.cells[i, j]
            if val < -2:
                rewards[(i,j)] = 0
            elif val == -1 or val == -2:
                rewards[(i,j)] = -1
            elif val == 3:
                rewards[(i, j)] = -10
            elif val == 2:
                rewards[(i, j)] = 5
            elif val == 1:
                rewards[(i, j)] = 1
            elif val == 4:
                rewards[(i, j)] = 100/robot.battery_lvl
            else:
                rewards[(i, j)] = grid.cells[(i,j)]

    clean_rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            clean_rewards[(i,j)] = cleaning_rewards(rewards, (i,j), robot)

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
    policy = policy_iteration(robot, policy, values, clean_rewards, actions)
    # Randomly select where to go based on policy
    best_direction = policy[robot.pos]
    while robot.orientation != best_direction:
        robot.rotate('r')
    robot.move()
    print('moved', best_direction)


def policy_iteration(robot, policy, values, clean_rewards, actions):
    '''
    Policy iteration

    Input:
    robot - a Robot object used to interact with the environment
    '''
    # print('Policy iteration')
    for _ in range(max_iter):
        policy_prev = policy.copy()

        values = policy_evaluation(robot, policy, values, clean_rewards)

        policy = policy_improvement(robot, policy, values, clean_rewards, actions)

        # Early stopping
        if policy_prev == policy:
            print('stopped early convergence')
            break
    return policy


def policy_evaluation(robot, policy, values, clean_rewards):
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
            #print(s, _)
            #use cleaning hitbox to get rewards for cleaning
            reward = clean_rewards[s]
            #print("r", reward)
            values[s] = reward + discount * V_prev[get_next_state(s, a, robot)]
        # Early stopping
        if V_prev == values:
            print('stopped early convergence')
            break
    return values

def cleaning_rewards(rewards, s, robot):
    """
    Gets the cleaning rewards for all tiles that will be cleaned by this state
    """
    sum_reward = 0
    for cleanable in robot.cleanable:
        #print("c", cleanable)
        coord = tuple([i+j for i,j in zip(s, cleanable)])

        #only count rewards inside playing field
        try:
            sum_reward += rewards[coord]
        except:
            pass
    return sum_reward

def policy_improvement(robot, policy, values, clean_rewards, actions):
    '''
    Improvement update pass in policy

    Input:
    robot - a Robot object used to interact with the environment
    '''
    # Calculate weighted score of each possible action
    for i in range(robot.grid.n_cols):
        for j in range(robot.grid.n_rows):
            s = (i,j)
            Q = {}
            try:
                for a in actions[s]:
                    Q[a] = clean_rewards[s] + discount * values[get_next_state(s, a, robot)]
                try:
                    policy[s] = max(Q, key=Q.get)
                except: pass
            except: pass

    return policy


def get_next_state(s, a, robot):
    """
    Inputs:
    s: State, location of robot
    a: action to be taken
    robot: Robot of which hitbox must be checked
    """
    #adjust for bigger robots?
    if a == 'e':
        nxt = (s[0]+1, s[1])

    elif a == 's':
        nxt = (s[0], s[1]+1)

    elif a == 'w':
        nxt =  (s[0]-1, s[1])
    elif a == 'n':
        nxt = (s[0], s[1]-1)
    else:
        print(f"Invalid action {a}")
        nxt = (s[0], s[1])
    if robot.check_hitbox(nxt):
        return nxt
    else:
        return (s[0], s[1])


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
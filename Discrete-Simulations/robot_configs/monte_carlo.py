from random import random, randint, randrange
import numpy as np
from robot_configs.policy_iteration_robot import get_next_state

Q_low, Q_high = -11, 11
e_soft = True
epsilon = 0.1
epochs = 50
discount_factor = 0.1
episode_steps = 50

look_forward = 20

conversion = {'n': 0, 'e': 1, 's': 2, 'w': 3}


def robot_epoch(robot, epsilon, epochs, episode_steps, discount_factor):
    Q, policy, Returns = initialize(robot, Q_low, Q_high, e_soft)
    invalid_moves_cols = {0: 3, robot.grid.n_cols - 1: 1}  # west, east
    invalid_moves_rows = {0: 0, robot.grid.n_rows - 1: 2}  # north, south

    for epoch in range(epochs):
        # Generate an episode for current epoch, given policy & number of steps
        episode = episode_generation(robot, policy, episode_steps)

        for index, step in enumerate(episode):
            # Location + direction
            (i_step, j_step), direction_step = step

            # G will contain all the future rewards given the current location
            G = []
            # Go over future steps
            # TO DO: think about computational complexity and if it's even needed to
            # check ALL of them. Will be diminished quite soon given the discount factor
            for future_index, future_step in enumerate(episode[i_step:i_step+look_forward]):
                # We actually start at the current step, then future ones
                (i_future_step, j_future_step), direction_future_step = future_step
                value = robot.grid.cells[i_future_step, j_future_step]
                G.append(value * discount_factor ** future_index)

            Returns[(i_step, j_step)][direction_step].append(sum(G))

        for i in range(0, robot.grid.n_cols):
            for j in range(0, robot.grid.n_rows):
                # Here we will average all the returns for a given location, and the four directions
                for direction in conversion:
                    current_Return = Returns[(i, j)][direction]
                    # Can be that we didn't encounter this location+direction in the episode yet
                    if len(current_Return) > 0:
                        avg_Returns = sum(current_Return) / len(current_Return)
                        Q[(i, j)][direction] = avg_Returns

                # The direction with the highest return so far will get the highest policy value
                # the rest a lower value, or 0 if not a legal move
                policies = np.ones(4) * epsilon / 4
                a_star = max(Q[(i, j)], key=Q[(i, j)].get)
                policies[conversion[a_star]] = 1 - epsilon + epsilon / 4

                # Illegal moves (outside of border)
                if i in invalid_moves_cols:
                    policies[invalid_moves_cols[i]] = 0
                if j in invalid_moves_rows:
                    policies[invalid_moves_rows[j]] = 0

                # Re-normalize
                policies = (1 / sum(policies)) * policies

                policy[(i,j)] = {'n': policies[0], 'e': policies[1],
                                 's': policies[2], 'w': policies[3]}

    best_direction = max(policy[robot.pos], key=policy[robot.pos].get)
    #print(robot.pos, best_direction)
    while robot.orientation != best_direction:
        robot.rotate('r')
    robot.move()



def initialize(robot, Q_low : int, Q_high : int, e_soft: bool) -> tuple:
    '''
    Initialze Q, policy and returns.
    
    For all s in S and a in A:
        - arbitrary values for Q(s, a) and (epsilon-)soft for policy (a|s)
        - Returns(s, a): an empty list
    
    Input: 
        robot - Robot object
        Q_low - int, lowest Q value
        Q_high - int, highest Q value
        e_soft - bool, whether to use e-soft policy (True) or soft policy (False)
    Output:
        Q - dict, arbitrary values for s, a
        policy - dict, (epsilon-)soft policy for a|s
        Returns - dict, an empty list for each action in each state
    '''
    Q = {}
    policy = {}
    Returns = {}

    invalid_moves_cols = {0: 3, robot.grid.n_cols-1: 1}  # west, east
    invalid_moves_rows = {0: 0, robot.grid.n_rows-1: 2}  # north, south

    for i in range(0, robot.grid.n_cols):
        for j in range(0, robot.grid.n_rows):
            if e_soft: # Epsilon soft policy
                randoms = np.array([random() + epsilon for i in range(4)])
            else: # Genral soft policy
                randoms = np.array([random() for i in range(4)])
            # Policy normalization
            policies = randoms / sum(randoms)

            if i in invalid_moves_cols:
                policies[invalid_moves_cols[i]] = 0
            if j in invalid_moves_rows:
                policies[invalid_moves_rows[j]] = 0

            policies = (1 / sum(policies)) * policies

            # Set values of return variables
            Q[(i,j)] = {'n': randint(Q_low, Q_high), 'e': randint(Q_low, Q_high),
                        's': randint(Q_low, Q_high), 'w': randint(Q_low, Q_high)}

            policy[(i,j)] = {'n': policies[0], 'e': policies[1],
                         's': policies[2], 'w': policies[3]}

            Returns[(i,j)] = {'n': [], 'e': [],
                              's': [], 'w': []}

    return Q, policy, Returns


def episode_generation(robot, policy : dict, num_steps : int) -> list:
    '''
    Choose s0 and a0 s.t. all pairs have probability > 0
    Generate an episode from (s0. a0) following pi

    Input:
        - robot - Robot object
        - policy - dict, current policy

    Output:
        - episode - list of states and actions
    '''
    episode = []

    # Choose s0
    while True:
        s0 = (randrange(robot.grid.n_cols), randrange(robot.grid.n_rows))
        if all(value > 0 for value in policy[s0].values()):
            break
    # Pick a0 from s0
    a0 = choose_policy_action(policy, s0)
    episode.append((s0, a0))
    # Choose actions
    for _ in range(num_steps-1):
        s_i = get_next_state(episode[-1][0], episode[-1][1])
        a_i = choose_policy_action(policy, s_i)
        episode.append((s_i, a_i))
    
    return episode

    
    
def choose_policy_action(policy : dict, state : tuple) -> str:
    '''
    From: https://stackoverflow.com/questions/40927221/how-to-choose-keys-from-a-python-dictionary-based-on-weighted-probability
    Choose action based on policy probability distribution

    Input:
        - state - dict of probability actions
    
    Output:
        - action - str of pick action
    '''
    choice = random()
    total = 0
    for action, prob in policy[state].items():
        total += prob
        if choice <= total:
            return action
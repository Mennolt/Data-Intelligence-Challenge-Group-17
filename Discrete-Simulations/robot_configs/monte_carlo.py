from random import random, randint
import numpy as np
from robot_configs.policy_iteration_robot import get_next_state

"""
Questions/comments/whatever:
- What values does Q normally have? Assumption now: [-10, 10]
- What is the range of epsilon? 
    - Assumption now: (0, 1)
    - Also, assumption that sum over all actions for one state is 1
"""

Q_low, Q_high = -11, 11
e_soft = True
epsilon = 0.2
epochs = 10

def robot_epoch(robot):
    
    Q, pi, Returns = initialize(robot, Q_low, Q_high, e_soft)

    for epoch in range(epochs):
        episode = episode_generation(robot, pi, 100)

        for index, occurrence in enumerate(episode):
            (i_occurrence, j_occurrence), direction_occurrence = occurrence

            G = []
            for co_index, co_occurrence in enumerate(episode[i_occurrence:]):
                (i_co_occurrence, j_co_occurrence), direction_co_occurrence = co_occurrence
                new_i = i_co_occurrence + robot.dirs[direction_co_occurrence][0]
                new_j = j_co_occurrence + robot.dirs[direction_co_occurrence][1]
                value = robot.grid.cells[new_i, new_j]
                G.append(value * discount_factor ** co_index)

            Returns[(i_occurrence, j_occurrence)][direction_occurrence].append(sum(G))
            current_Return = Returns[(i_occurrence, j_occurrence)][direction_occurrence]
            avg_Returns = sum(current_Return) / len(current_Return)
            Q[(i_occurrence, j_occurrence)] = avg_Returns

        for i in range(0, robot.grid.n_cols):
            for j in range(0, robot.grid.n_rows):
                directions = ['n', 'e', 's', 'w']
                a_star = max(Q[i, j], key=Q[i, j].get)

                for direction in directions:
                    if direction == a_star:
                        pi[(i,j)][direction] = 1 - epsilon + epsilon/4
                    else:
                        pi[(i,j)][direction] = epsilon/4



def initialize(robot, Q_low : float, Q_high : float, e_soft: bool) -> tuple:
    '''
    Initialze Q, pi and returns.
    
    For all s in S and a in A:
        - arbitrary values for Q(s, a) and (e-)soft for pi (a|s)
        - Returns(s, a): an empty list
    
    Input: 
        robot - Robot object
        Q_low - float, lowest Q value
        Q_high - float, highest Q value
        e_soft - bool, whether to use e-soft policy (True) or soft policy (False)

    '''
    Q = {}
    pi = {}
    Returns = {}

    for i in range(0, robot.grid.n_cols):
        for j in range(0, robot.grid.n_rows):
            if e_soft: 
                randoms = np.array([random() + epsilon for i in range(4)])
            else:
                randoms = np.array([random() for i in range(4)])
            policies = randoms / sum(randoms)

            Q[(i,j)] = {'n': randint(Q_low, Q_high), 'e': randint(Q_low, Q_high),
                        's': randint(Q_low, Q_high), 'w': randint(Q_low, Q_high)}

            pi[(i,j)] = {'n': policies[j], 'e': policies[j],
                         's': policies[j], 'w': policies[j]}

            Returns[(i, j)] = {'n': 0, 'e': 0,
                               's': 0, 'w': 0}

    return Q, pi, Returns


def episode_generation(robot, policy : dict, num_steps : int) -> list:
    '''
    Choose s0 and a0 s.t. all pairs have probability > 0
    Generate an episode from (s0. a0) following pi

    Input:
        - robot - Robot object
        - policy - dict, current policy

    Output:
        - episode
    '''
    episode = []

    # Choose s0
    while True:
        s0 = (randrange(robot.grid.n_cols), randrange(robot.grid.n_rows))
        if all(value > 0 for value in policy[s0]):
            break
    # Pick a0 from s0
    a0 = choose_policy_action(s0)
    episode.append((s0, a0))
    # Choose actions
    for _ in range(num_steps-1):
        s_i = get_next_state(episode[-1][0], episode[-1][1])
        a_i = choose_policy_action(s_i)
        episode.append((s_i, a_i))
    
    return episode

    
    
def choose_policy_action(state : dict) -> str:
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
    for action, prob in state.items():
        total += prob
        if choice <= total:
            return action
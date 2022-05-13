from random import random, randint
import numpy as np

"""
Questions/comments/whatever:
- What values does Q normally have? Assumption now: [-10, 10]
- What is the range of epsilon? 
    - Assumption now: (0, 1)
    - Also, assumption that sum over all actions for one state is 1
"""

Q_low, Q_high = -11, 11
e_soft = True

def robot_epoch(robot):
    
    Q, pi, Returns = initialize(robot, Q_low, Q_high, e_soft)

    for epoch in range(epochs):
        episode = []


        if



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

    Output:
        Tuple of:
        - Q[(i,j)] - dict, probability distributions for actions a in state (i, j)
        - pi[(i,j)] - dict, policy for state (i, j)
        - Returns[(i, j)] - dict, empty returns
    '''
    Q = {}
    pi = {}
    Returns = {}

    epsilon = 0.2
    epochs = 10

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
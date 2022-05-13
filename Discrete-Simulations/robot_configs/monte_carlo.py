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

def robot_epoch(robot):
    Q = {}
    pi = {}
    Returns = {}

    epsilon = 0.2
    epochs = 10

    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            randoms = np.array([random() + epsilon for i in range(4)])
            policies = randoms / sum(randoms)

            Q[(i,j)] = {'n': randint(Q_low, Q_high), 'e': randint(Q_low, Q_high),
                        's': randint(Q_low, Q_high), 'w': randint(Q_low, Q_high)}

            pi[(i,j)] = {'n': policies[j], 'e': policies[j],
                         's': policies[j], 'w': policies[j]}

            Returns[(i, j)] = {'n': 0, 'e': 0,
                               's': 0, 'w': 0}

    for epoch in range(epochs):
        episode = []


        if


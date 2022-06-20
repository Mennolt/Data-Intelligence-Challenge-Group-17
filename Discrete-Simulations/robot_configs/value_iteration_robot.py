import numpy as np

def robot_epoch(robot):
    # Hyperparameters
    SMALL_ENOUGH = 0.05
    GAMMA = 0.9
    NOISE = robot.p_move

    # Initialisation
    grid = robot.grid

    rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            rewards[(i,j)] = grid.cells[i, j]

    V = rewards.copy()

    actions = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):

            possible_actions = []

            try:
                if grid.cells[i+1, j] >= 0:
                    possible_actions.append("e")
            except IndexError: pass
            try:
                if grid.cells[i, j+1] >= 0:
                    possible_actions.append("s")
            except IndexError: pass
            try:
                if grid.cells[i-1, j] >= 0:
                    possible_actions.append("w")
            except IndexError: pass
            try:
                if grid.cells[i, j-1] >= 0:
                    possible_actions.append("n")
            except IndexError: pass

            # Ensure only keys get added when there are actions
            if len(possible_actions) != 0:
                actions[(i, j)] = possible_actions

    # Define an initial policy
    policy = {}

    for s in actions.keys():
        policy[s] = np.random.choice(actions[s])

    # Value Iteration

    print("===== BEGIN VALUE ITERATION =====")

    iteration = 0
    while True:
        biggest_change = 0
        for i in range(0, grid.n_cols):
            for j in range(0, grid.n_rows):
                s = (i, j)
                if s in policy:
                    old_v = V[s]
                    new_v = 0

                    for a in actions[s]:
                        if a == 'e':
                            nxt = (s[0]+1, s[1])
                        if a == 's':
                            nxt = (s[0], s[1]+1)
                        if a == 'w':
                            nxt = (s[0]-1, s[1])
                        if a == 'n':
                            nxt = (s[0], s[1]-1)


                        if len(actions[s]) > 1:
                            # Choose a new random action to do (transition probability)
                            random_1 = np.random.choice([i for i in actions[s] if i != a])
                            if random_1 == 'e':
                                act = (s[0]+1, s[1])
                            if random_1 == 's':
                                act = (s[0], s[1]+1)
                            if random_1 == 'w':
                                act = (s[0]-1, s[1])
                            if random_1 == 'n':
                                act = (s[0], s[1]-1)
                        else:
                            act = nxt

                        # Calulate the value
                        v = rewards[s] + (GAMMA * ((1-NOISE)*V[nxt] + (NOISE * V[act])))

                        if v > new_v:  # Is this the best action so far? If so, keep it
                            new_v = v
                            policy[s] = a

                    V[s] = new_v
                    biggest_change = max(biggest_change, np.abs(old_v - V[s]))
        if biggest_change < SMALL_ENOUGH:
            robot.grid.policy = policy
            break
        iteration +=1
        #print(f"===== ITERATION {iteration} =====")

    best_direction = policy[robot.pos]
    while robot.orientation != best_direction:
        robot.rotate('r')
    robot.move()

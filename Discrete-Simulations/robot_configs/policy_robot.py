import random

max_iter = 50000

def robot_epoch(robot):
    # Get the possible tiles after move
    possible_tiles = robot.possible_tiles_after_move()
    # Initialization
    policy = [[{'n': 0.25, 'e': 0.25, 's': 0.25, 'w': 0.25} for col in range(robot.grid.n_rows)] for row in range(robot.grid.n_rows)]
    values = [[0 for col in range(robot.grid.n_cols)] for row in range(robot.grid.n_rows)]
    rewards = {}
    for i in range(0, robot.grid.n_rows):
        for j in range(0, robot.grid.n_cols):
            rewards[(i,j)] = robot.grid.cells[i, j]
    # Policy iteration
    policy = policy_iteration(robot, policy, values, rewards)
    # Randomly select where to go based on policy
    rand_val = random.random()
    total = 0
    for k, v in policy[robot.pos[0]][robot.pos[1]].items():
        total += v
        if rand_val <= total:
            des_dir = k
    while robot.orientation != des_dir:
        robot.rotate('r')
    robot.move()


def policy_iteration(robot, policy, values, rewards):
    '''
    Policy iteration

    Input:
    robot - a Robot object used to interact with the environment
    '''
    print('Policy iteration')
    for _ in range(max_iter):
        policy_prev = policy.copy()

        values = policy_evaluation(robot, policy, values, rewards)

        policy = policy_improvement(robot, policy, values, rewards)

        # Early stopping
        # if all(policy_prev[row][col] == policy[row][col] for row, col in robot.grid.cells):
        #     break
    return policy


def policy_evaluation(robot, policy, values, rewards):
    '''
    Evaluation of policy

    Input:
    robot - a Robot object used to interact with the environment
    '''
    print('    Policy evaluation')
    for _ in range(max_iter):
        V_prev = values.copy()
        # Calculate weighted score of state after each possible action
        look_ahead_values = []
        for k, v in policy[robot.pos[0]][robot.pos[1]].items():
            if k == 'n':
                try:
                    look_ahead_values.append(v * V_prev[robot.pos[0]-1][robot.pos[1]])
                except IndexError: # If not able to move, stay in the same spot
                    look_ahead_values.append(v * V_prev[robot.pos[0]][robot.pos[1]])
            if k == 'e':
                try:
                    look_ahead_values.append(v * V_prev[robot.pos[0]][robot.pos[1]+1])
                except IndexError: 
                    look_ahead_values.append(v * V_prev[robot.pos[0]][robot.pos[1]])
            if k == 's':
                try:
                    look_ahead_values.append(v * V_prev[robot.pos[0]+1][robot.pos[1]])
                except IndexError: 
                    look_ahead_values.append(v * V_prev[robot.pos[0]][robot.pos[1]])
            if k == 'w':
                try:
                    look_ahead_values.append(v * V_prev[robot.pos[0]][robot.pos[1]-1])
                except IndexError: 
                    look_ahead_values.append(v * V_prev[robot.pos[0]][robot.pos[1]])
        values[robot.pos[0]][robot.pos[1]] = rewards[(robot.pos[0], robot.pos[1])] + sum(look_ahead_values)
            
        # Early stopping
        # if all(V_prev[s] == values[s] for s in robot.grid.cells):
        #     break
    return values


def policy_improvement(robot, policy, values, rewards):
    '''
    Improvement update pass in policy

    Input:
    robot - a Robot object used to interact with the environment
    '''
    print('    Policy improvement')
    # Calculate Q value
    Q = {}
    # Calculate weighted score of each possible action
    look_ahead_values = []
    for k, v in policy[robot.pos[0]][robot.pos[1]].items():
        if k == 'n':
            try:
                look_ahead_values.append(v * values[robot.pos[0]-1][robot.pos[1]])
            except IndexError: # If not able to move, stay in the same spot
                look_ahead_values.append(v * values[robot.pos[0]][robot.pos[1]])
        if k == 'e':
            try:
                look_ahead_values.append(v * values[robot.pos[0]][robot.pos[1]+1])
            except IndexError: 
                look_ahead_values.append(v * values[robot.pos[0]][robot.pos[1]])
        if k == 's':
            try:
                look_ahead_values.append(v * values[robot.pos[0]+1][robot.pos[1]])
            except IndexError: 
                look_ahead_values.append(v * values[robot.pos[0]][robot.pos[1]])
        if k == 'w':
            try:
                look_ahead_values.append(v * values[robot.pos[0]][robot.pos[1]-1])
            except IndexError: 
                look_ahead_values.append(v * values[robot.pos[0]][robot.pos[1]])
    # Select action with highest Q value
    for k, v in policy[robot.pos[0]][robot.pos[1]].items():
        Q[k] = rewards[(robot.pos[0], robot.pos[1])] + sum(look_ahead_values)
    best_action = max(Q, key=Q.get)
    # Update policy
    for k, v in policy[robot.pos[0]][robot.pos[1]].items():
        if k == best_action:
            policy[robot.pos[0]][robot.pos[1]][k] = 1.0
        else:
            policy[robot.pos[0]][robot.pos[1]][k] = 0.0
    return policy
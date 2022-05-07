import random

max_iter = 50000

def robot_epoch(robot):
    # Get the possible tiles after move
    possible_tiles = robot.possible_tiles_after_move()
    # Policy iteration
    policy_iteration(robot)
    # Randomly select where to go based on policy
    des_dir = ''
    rand_val = random.random()
    total = 0
    for k, v in robot.policy[robot.pos[0]][robot.pos[1]]:
        total += v
        if rand_val <= total:
            selection = k
    while robot.orientation != des_dir:
        robot.rotate('r')
    robot.move()


def policy_iteration(robot):
    '''
    Policy iteration

    Input:
    robot - a Robot object used to interact with the environment
    '''
    for _ in range(max_iter):
        policy_prev = robot.grid.policy.copy()

        policy_evaluation(robot.grid.policy, robot.pos)

        robot.grid.policy = policy_improvement()

        if all(policy_prev[s] == robot.grid.policy[s] for s in robot.pos):
            break


def policy_evaluation(robot):
    '''
    Evaluation of policy

    Input:
    robot - a Robot object used to interact with the environment
    '''
    for _ in range(max_iter):
        V_prev = robot.grid.values.copy()
        for row in range(len(robot.grid.cells)):
            for col in range(len(robot.grid.cells[row])):
                # Calculate weighted score of state after each possible action
                look_ahead_values = []
                for k, v in robot.grid.policy[row][col]:
                    if k == 'n':
                        try:
                            look_ahead_values.append(v * V_prev[row-1][col])
                        except IndexError: # If not able to move, stay in the same spot
                            look_ahead_values.append(v * V_prev[row][col])
                    if k == 'e':
                        try:
                            look_ahead_values.append(v * V_prev[row][col+1])
                        except IndexError: 
                            look_ahead_values.append(v * V_prev[row][col])
                    if k == 's':
                        try:
                            look_ahead_values.append(v * V_prev[row+1][col])
                        except IndexError: 
                            look_ahead_values.append(v * V_prev[row][col])
                    if k == 'w':
                        try:
                            look_ahead_values.append(v * V_prev[row][col-1])
                        except IndexError: 
                            look_ahead_values.append(v * V_prev[row][col])
                robot.grid.values[row][col] = robot.grid.rewards[row][col] + sum(look_ahead_values)
            
        if all(V_prev[s] == robot.grid.values[s] for s in robot.grid.cells):
            break


def policy_improvement(robot):
    '''
    Improvement update pass in policy

    Input:
    robot - a Robot object used to interact with the environment
    '''
    # Iterate over each state
    for row in range(len(robot.grid.cells)):
        for col in range(len(robot.grid.cells[row])):
            # Calculate Q value
            Q = {}
            # Calculate weighted score of each possible action
            look_ahead_values = []
            for k, v in robot.grid.policy[row][col]:
                if k == 'n':
                    try:
                        look_ahead_values.append(v * robot.grid.values[row-1][col])
                    except IndexError: # If not able to move, stay in the same spot
                        look_ahead_values.append(v * robot.grid.values[row][col])
                if k == 'e':
                    try:
                        look_ahead_values.append(v * robot.grid.values[row][col+1])
                    except IndexError: 
                        look_ahead_values.append(v * robot.grid.values[row][col])
                if k == 's':
                    try:
                        look_ahead_values.append(v * robot.grid.values[row+1][col])
                    except IndexError: 
                        look_ahead_values.append(v * robot.grid.values[row][col])
                if k == 'w':
                    try:
                        look_ahead_values.append(v * robot.grid.values[row][col-1])
                    except IndexError: 
                        look_ahead_values.append(v * robot.grid.values[row][col])
            # Select action with highest Q value
            for k, v in robot.grid.policy[row][col]:
                Q[k] = robot.grid.rewards[row][col] + sum(look_ahead_values)
            best_action = max(Q, key=Q.get)
            # Update policy
            for k, v in robot.grid.policy[row][col]:
                if k == best_action:
                    robot.grid.policy[row][col][k] = 1.0
                else:
                    robot.grid.policy[row][col][k] = 0.0
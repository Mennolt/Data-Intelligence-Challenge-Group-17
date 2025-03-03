import numpy as np

def robot_epoch(robot):
    # Initialisation
    grid = robot.grid.copy()
    grid = custom_rewards_grid(grid)

    actions = {}
    for i in range(0, grid.n_rows):
        for j in range(0, grid.n_cols):

            possible_actions = []

            try:
                grid.cells[no_neg(i + 1), no_neg(j)]
            except IndexError:
                pass
            else:
                possible_actions.append("e")

            try:
                grid.cells[no_neg(i), no_neg(j + 1)]
            except IndexError:
                pass
            else:
                possible_actions.append("s")

            try:
                grid.cells[no_neg(i), no_neg(j - 1)]
            except IndexError:
                pass
            else:
                possible_actions.append("n")

            try:
                grid.cells[no_neg(i - 1), no_neg(j)]
            except IndexError:
                pass
            else:
                possible_actions.append("w")

            # Ensure only keys get added when there are actions
            if len(possible_actions) != 0:
                actions[(i, j)] = possible_actions



    rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            rewards[(i, j)] = grid.cells[i, j]

    #parameters and counters
    total_iterations = 20
    iteration_count = 0
    total_episodes = 25
    episode_count = 0
    current_position = robot.pos
    learning_rate = 0.1
    gamma = 0.95

    if not robot.q_values_calculated:
        try:
            # Initialise Q values
            robot.init_q_values(actions)
            while episode_count <= total_episodes:


                while not return_true_if_terminal(grid, current_position) and iteration_count <= total_iterations:


                    action = get_random_action(actions, current_position)


                    next_position = get_next_position(action, current_position, actions)
                    next_position_reward = get_state_reward(rewards, next_position)

                    # Next-Next Rewards * 4
                    surrounding_q_values = get_surrounding_q_values(robot.q_values, next_position)

                    robot.q_values[current_position][action] += learning_rate * (next_position_reward + gamma + np.max(
                        surrounding_q_values) - robot.q_values[current_position][action])

                    iteration_count += 1

                # Reset iteration count for each new episode + Increase episode count
                iteration_count = 0
                episode_count += 1


            robot.q_values_calculated = True

        except Exception as e:
            print(f"Main error: {e}")
            raise e

    best_direction = get_max_surrounding_direction(robot.q_values, current_position)

    while robot.orientation != best_direction:
        robot.rotate('r')
    robot.move()

def no_neg(value):
    if value >= 0:
        return value
    else:
        raise IndexError

def get_surrounding_q_values(q_values, position):
    try:
        pos_directions = list(q_values[position].keys())
        q = []
        for dirs in pos_directions:
            q.append(q_values[position][dirs])
    except Exception as e:
        print(f"get_surrounding_q_values_error: {e}")
        raise e

    return q


def get_max_surrounding_direction(q_values, position):
    try:
        max_direction = max(q_values[position], key=q_values[position].get)
    except Exception as e:
        print(f"get_surrounding_direction_values_error: {e}")
        raise e

    return max_direction


def return_true_if_terminal(grid, state: ()) -> bool:
    # Check for death cell
    if grid.cells[state] == -20:
        return True
    else:
        # Check if there are any tiles yet to be cleaned
        if not (5 or 10 in grid[:, :]):
            return True
        else:
            return False


def get_random_action(actions, s):
    # Choose a new random action to do (transition probability)
    return np.random.choice(actions[s])


def get_max_reward(rewards, s):
    reward_list = []
    # Append the reward list with every possible next state
    reward_list.append(get_state_reward(rewards, (s[0], s[1] + 1)))
    reward_list.append(get_state_reward(rewards, (s[0] + 1, s[1])))
    reward_list.append(get_state_reward(rewards, (s[0], s[1] - 1)))
    reward_list.append(get_state_reward(rewards, (s[0] - 1, s[1])))

    return np.max(reward_list)


def get_next_position(action, s, actions):
    nxt = None
    if action in actions[s]:
        # Changed
        if action == 'e':
            nxt = (s[0] + 1, s[1])
        if action == 's':
            nxt = (s[0], s[1] + 1)
        if action == 'w':
            nxt = (s[0] - 1, s[1])
        if action == 'n':
            nxt = (s[0], s[1] - 1)

        if nxt is None:
            print("get_next_position_valueError")
            raise ValueError
        else:
            return nxt
    else:
        print("get_next_position_indexError")
        raise IndexError



def get_state_reward(rewards, s):
    return rewards[s]


def custom_rewards_grid(grid):
    if grid.cells[0, 0] not in [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, -3.0]:
        return grid
    else:
        for i in range(0, grid.n_cols):
            for j in range(0, grid.n_rows):

                # Inner wall
                if grid.cells[i, j] == -2:
                    grid.cells[i, j] = -10
                # Outer wall
                elif grid.cells[i, j] == -1:
                    grid.cells[i, j] = -10
                # Clean
                elif grid.cells[i, j] == 0:
                    grid.cells[i, j] = -10
                # Dirty
                elif grid.cells[i, j] == 1:
                    grid.cells[i, j] = 5
                # Goal
                elif grid.cells[i, j] == 2:
                    grid.cells[i, j] = 10
                # Death
                elif grid.cells[i, j] == 3:
                    grid.cells[i, j] = -20
                # Self/Robot
                elif grid.cells[i, j] in [-3, -4, -5, -6]:
                    grid.cells[i, j] = 0
                else:
                    raise ValueError(f"value: {grid.cells[i, j]}")
    return grid

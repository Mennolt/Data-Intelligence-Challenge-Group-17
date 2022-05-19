import numpy as np


def robot_epoch(robot):
    # Hyperparameters
    SMALL_ENOUGH = 0.05
    GAMMA = 0.9
    NOISE = robot.p_move

    # Initialisation
    grid = robot.grid.copy()
    grid = custom_rewards_grid(grid)

    actions = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):

            possible_actions = []
            try:
                if i != grid.n_rows - 1:
                    possible_actions.append("e")
            except IndexError:
                pass
            try:
                if j != grid.n_cols - 1:
                    possible_actions.append("s")
            except IndexError:
                pass
            try:
                if i != 0:
                    possible_actions.append("w")
            except IndexError:
                pass
            try:
                if j != 0:
                    possible_actions.append("n")
            except IndexError:
                pass

            # Ensure only keys get added when there are actions
            if len(possible_actions) != 0:
                actions[(i, j)] = possible_actions


    rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            rewards[(i, j)] = grid.cells[i, j]

    # V = rewards.copy()
    #
    # # Define an initial policy
    # policy = {}
    #
    # for s in actions.keys():
    #     policy[s] = np.random.choice(actions[s])

    # try:
    total_iterations = 10
    iteration_count = 0
    total_episodes = 10
    episode_count = 0
    current_position = robot.pos

    # What to do
    learning_rate = 1
    gamma = 1
    if not robot.q_values_calculated:
        try:
            # Initialise Q values
            robot.init_q_values(actions)
            while episode_count <= total_episodes:
                print(f"Episode_count: {episode_count}")

                # print(f'return_true_if_terminal: {return_true_if_terminal(grid, current_position)} ')

                # ToDo: Random starting pos
                while not return_true_if_terminal(grid, current_position) and iteration_count <= total_iterations:
                    # print(f"Iteration_count: {iteration_count}")
                    # print(f"total_iterations: {total_iterations}")

                    action = get_random_action(actions, current_position)

                    # ToDo: Possibly greedy
                    next_position = get_next_position(action, current_position, actions)
                    next_position_reward = get_state_reward(rewards, next_position)

                    # Next-Next Rewards * 4
                    surrounding_q_values = get_surrounding_q_values(robot.q_values, next_position)

                    print(
                        f'\n'
                        f'Qvalues update values\n'
                        f'current_position: {current_position} \n'
                        f'action: {action} \n'
                        f'learning_rate: {learning_rate} \n'
                        f' next_position_reward: {next_position_reward} \n'
                        f' gamma: {gamma} \n'
                        f' np.max(surrounding_q_values): {np.max(surrounding_q_values)} \n'
                        f' robot.q_values[current_position][action] : {robot.q_values[current_position][action]}'
                        f'\n'
                    )

                    robot.q_values[current_position][action] += learning_rate * (next_position_reward + gamma + np.max(
                        surrounding_q_values) - robot.q_values[current_position][action])

                    # print(
                    #     f"update Q value: {learning_rate * (next_position_reward + gamma * np.max(surrounding_q_values) - robot.q_values[current_position][action])}")

                    # # set next action and state to current action and state
                    # if grid.cells[next_position] == -10:
                    #     # collision detection: only move if not a wall
                    #     current_position = next_position
                    # else:
                    #     current_position = current_position
                    iteration_count += 1

                # Reset iteration count for each new episode + Increase episode count
                iteration_count = 0
                episode_count += 1
                # update policy & rewards
                # rewards[nex] = 0
                # policy = get_greedy_policy(actions, rewards)
                # current_position = next_position

            robot.q_values_calculated = True
            print()
            print('Finished iterating \n')
            print(f"q-values: {robot.q_values}")
            print()
        except Exception as e:
            print(f"Main error: {e}")
            raise e

    best_direction = get_max_surrounding_direction(robot.q_values, current_position)

    print()
    # print("Calculate best direction")
    # print(f'best_direction: {best_direction}')
    # print(f'robot.orientation: {robot.orientation}')
    # print(f"q-values: {robot.q_values}")
    # print(f"grid: {grid.cells.T}")
    print()

    while robot.orientation != best_direction:
        robot.rotate('r')
    robot.move()


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
    # Changed
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
        # print(f"action: {action}")
        # print(f"state: {s}")
        # print(f"actions: {actions}")

        print("get_next_position_indexError")
        raise IndexError


#
# def get_max_reward_of_surrounding_states(state, rewards):
#     actions = ['n', 'w', 's', 'e']
#     surrounding_states = []
#     surrounding_states.append(get_next_state())


def get_state_reward(rewards, s):
    return rewards[s]


def custom_rewards_grid(grid):
    # TODO: Maybe change by using grid.copy
    if grid.cells[0, 0] not in [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, -3.0]:
        print(f" 0,0 : {grid.cells[0, 0] in [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, -3.0]}")
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

# def chooseAction(self):
#     # choose action with most expected value
#     mx_nxt_reward = 0
#     action = ""
#
#     if np.random.uniform(0, 1) <= self.exp_rate:
#         action = np.random.choice(self.actions)
#     else:
#         # greedy action
#         for a in self.actions:
#             current_position = self.State.state
#             nxt_reward = self.Q_values[current_position][a]
#             if nxt_reward >= mx_nxt_reward:
#                 action = a
#                 mx_nxt_reward = nxt_reward
#     return action


# def make_actions():
#     # Actions
#     actions = {}
#     for i in range(0, grid.n_rows):
#         for j in range(0, grid.n_cols):
#             possible_actions = []
#
#             try:
#                 i = grid.cells[i + 1, j]
#             except Exception as e:
#                 print(e)
#                 print('e')
#                 pass
#             else:
#                 possible_actions.append("e")
#
#             try:
#                 i = grid.cells[ i, j + 1]
#             except IndexError:
#                 print('s')
#                 pass
#             else:
#                 possible_actions.append("s")
#
#             try:
#                 i = grid.cells[i - 1, j]
#             except IndexError:
#                 print('w')
#                 pass
#             else:
#                 possible_actions.append("w")
#
#             try:
#                 i = grid.cells[ i, j - 1]
#             except IndexError:
#                 print('n')
#                 pass
#             else:
#                 possible_actions.append("n")
#
#             print(possible_actions)
#             # Ensure only keys get added when there are actions
#             if len(possible_actions) > 0:
#                 actions[( i, j)] = possible_actions

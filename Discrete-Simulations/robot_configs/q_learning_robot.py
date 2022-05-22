import random

import numpy as np


def no_neg(value):
    if value >= 0:
        return value
    else:
        raise IndexError


def robot_epoch(robot):
    current_position = robot.pos
    grid = robot.grid.copy()

    if not robot.q_values_calculated:
        print('Training Q Values')

        # Initialisation
        grid = custom_rewards_grid(grid)

        actions = {}
        for i in range(0, grid.n_cols):
            for j in range(0, grid.n_rows):

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
                else:
                    pass

        # print(f'actions: {actions}')

        rewards = {}
        for i in range(0, grid.n_cols):
            for j in range(0, grid.n_rows):
                rewards[(i, j)] = grid.cells[i, j]

        total_iterations = 1000
        iteration_count = 0
        total_episodes = 5
        episode_count = 0

        # Hyperparameters
        learning_rate = 1
        gamma = 0.5

        try:
            # Initialise Q values
            robot.init_q_values(actions, rewards)

            print(robot.q_values)
            while episode_count <= total_episodes:

                current_position = robot.pos
                action = get_random_action(actions, current_position)
                print(f"Episode_count: {episode_count}, {current_position, action}")

                current_position = current_position
                action = action
                update_value = 0

                while iteration_count <= total_iterations:
                    # print(f"Iteration_count/total_iterations: {iteration_count}/{total_iterations}")

                    # ToDo: Possibly greedy
                    next_position = get_next_position(action, current_position, actions)
                    next_position_reward = get_state_reward(rewards, next_position)

                    # Next-Next Rewards * 4
                    surrounding_q_values = get_surrounding_q_values(robot.q_values, next_position)

                    # print(
                    #     f'\n'
                    #     f'Qvalues update values\n'
                    #     f'current_position: {current_position} \n'
                    #     f'action: {action} \n'
                    #     f'learning_rate: {learning_rate} \n'
                    #     f' next_position_reward: {next_position_reward} \n'
                    #     f' gamma: {gamma} \n'
                    #     f' np.max(surrounding_q_values): {np.max(surrounding_q_values)} \n'
                    #     f' robot.q_values[current_position][action] : {robot.q_values[current_position][action]}'
                    #     f'\n'
                    # )

                    robot.q_values[current_position][action] += learning_rate * (next_position_reward * gamma * np.max(
                        surrounding_q_values) - robot.q_values[current_position][action])

                    # set next action and state to current action and state
                    if grid.cells[current_position] >= 0:
                        current_position = next_position
                    action = get_random_action(actions, current_position)
                    iteration_count += 1
                    if return_true_if_terminal(grid, current_position):
                        break
                # Reset iteration count for each new episode + Increase episode count
                iteration_count = 0
                episode_count += 1

            robot.q_values_calculated = True
            print()
            print('Finished iterating \n')
            # print(f"q-values: {robot.q_values}\n")
            print()
        except Exception as e:
            print(f"Main error: {e}")
            raise e

    best_direction = get_best_action(robot.q_values, current_position)

    print("\nCalculate best direction")
    print(f'best_direction: {best_direction}')
    print(f'Current Pos: {current_position}')
    print(f"q-values for current pos: {robot.q_values[current_position]}")
    print(f"grid: {grid.cells.T} \n")

    while robot.orientation != best_direction:
        robot.rotate('r')
    robot.move()


def get_surrounding_q_values(q_values, position):
    try:
        pos_actions = list(q_values[position].keys())
        q = []
        for action in pos_actions:
            q.append(q_values[position][action])
    except Exception as e:
        print(f"get_surrounding_q_values_error: {e}")
        raise e

    return q


def get_best_action(q_values, position):
    try:
        best_action = max(q_values[position], key=q_values[position].get)
    except Exception as e:
        print(f"get_surrounding_direction_values_error: {e}")
        raise e

    return best_action


def return_true_if_terminal(grid, state: ()) -> bool:
    # Check for death cell
    if grid.cells[state] == -2:
        return True
    else:
        # Check if there are any tiles yet to be cleaned
        if 1 in grid.cells:
            return False
        else:
            return True


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
        print(action, s)
        raise IndexError


def get_state_reward(rewards, s):
    return rewards[s]


def custom_rewards_grid(grid):
    # TODO: Maybe change by using grid.copy
    if grid.cells[0, 0] not in [-2,-1, 0.0, -1.0]:
        return grid
    else:
        for i in range(0, grid.n_cols):
            for j in range(0, grid.n_rows):

                # Inner wall
                if grid.cells[i, j] == -2:
                    grid.cells[i, j] = -1 #-10
                # Outer wall
                elif grid.cells[i, j] == -1:
                    grid.cells[i, j] = -1 #-10
                # # Clean
                # elif grid.cells[i, j] == 0:
                #     grid.cells[i, j] =
                # Dirty
                elif grid.cells[i, j] == 1:
                    grid.cells[i, j] = 1 #5
                # # Goal
                # elif grid.cells[i, j] == 2:
                #     grid.cells[i, j] = 10
                # Death
                elif grid.cells[i, j] == 3:
                    grid.cells[i, j] = -2 #-20
                # Self/Robot
                elif grid.cells[i, j] in [-3, -4, -5, -6]:
                    grid.cells[i, j] = 0
                else:

                    print(f'custom_rewards_grid_error, i,j: {i, j}. Value: {grid.cells[i, j]}')
                    raise ValueError()
    return grid

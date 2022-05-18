import numpy as np


def robot_epoch(robot):
    # Hyperparameters
    SMALL_ENOUGH = 0.05
    GAMMA = 0.9
    NOISE = robot.p_move

    # Initialisation
    grid = robot.grid.copy()
    print()
    print(grid.cells)
    grid = custom_rewards_grid(grid)
    print(grid.cells)
    print()

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

    print(f"actions: {actions}")

    print("==========actions===============")
    print(range(0, grid.n_rows))

    # initial Q values
    try:
        Q_values = {}
        for i in range(0, grid.n_rows):
            for j in range(0, grid.n_cols):
                Q_values[(i, j)] = {}
                for a in actions[(i, j)]:
                    Q_values[(i, j)][a] = 0  # Q value is a dict of dict
    except Exception as e:
        # print(f"Q_values: {Q_values}")
        print(f"Q_value_error: {e}")
        raise e

    print("==========Qvalues===============")

    rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            rewards[(i, j)] = grid.cells[i, j]
    print("==========rewards===============")

    # V = rewards.copy()
    #
    # # Define an initial policy
    # policy = {}
    #
    # for s in actions.keys():
    #     policy[s] = np.random.choice(actions[s])

    print("===== BEGIN Q LEARNING =====")

    # try:
    episode_size = 20
    total_episodes = 50
    current_position = robot.pos

    # What to do
    learning_rate = 1
    gamma = 1
    try:
        for episode in range(total_episodes):
            # print(f"Episode: {episode}")
            episode_count = 1

            # ToDo: Random starting pos
            while not return_true_if_terminal(grid, current_position) and episode_count <= episode_size:
                # print(f"Episode_count: {episode_count}")

                action = get_random_action(actions, current_position)

                # ToDo: Possibly greedy
                next_position = get_next_position(action, current_position, actions)
                next_position_reward = get_state_reward(rewards, next_position)

                # Next-Next Rewards * 4
                surrounding_q_values = get_surrounding_q_values(Q_values, next_position)

                Q_values[current_position][action] += learning_rate * (next_position_reward + gamma * np.max(
                    surrounding_q_values) - Q_values[current_position][action])
                episode_count += 1

                # set next action and state to current action and state
                if grid.cells[next_position] > -2:
                    # collision detection: only move if not a wall
                    current_position = next_position
                elif grid.cells[next_position] == 5:
                    grid.cells[next_position] = -10
                    current_position = current_position
                else:
                    current_position = current_position

                # update policy & rewards
                # rewards[position_prime] = 0
                # policy = get_greedy_policy(actions, rewards)
                # current_position = next_position
        # print('Finished iterating \n')
        # print(f"q-values: {Q_values}")
        # print(f"grid: {grid.cells}")
        # print('\n')


        best_direction = get_max_surrounding_direction(Q_values, current_position)
        print("BEST DIRECTION")
        print(best_direction)
        print(robot.orientation)
        while robot.orientation != best_direction:
            robot.rotate('r')
        robot.move()

    except Exception as e:
        print(f"Main error: {e}")
        raise e


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
    if grid.cells[state] == 5:
        return True
    else:
        if not (1 or 2 in grid[:, :]):
            return True
        else:
            return False


def get_random_action(actions, s):
    # Choose a new random action to do (transition probability)
    return np.random.choice(actions[s])


def get_max_reward(rewards, s):
    reward_list = []

    # Append the reward list with every possible next state
    reward_list.append(get_state_reward(rewards, (s[0] + 1, s[1])))
    reward_list.append(get_state_reward(rewards, (s[0], s[1] + 1)))
    reward_list.append(get_state_reward(rewards, (s[0] - 1, s[1])))
    reward_list.append(get_state_reward(rewards, (s[0], s[1] - 1)))

    return np.max(reward_list)


def get_next_position(action, s, actions):
    nxt = None
    if action in actions[s]:
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
                elif grid.cells[i, j] == -3:
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
#                 i = grid.cells[i, j + 1]
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
#                 i = grid.cells[i, j - 1]
#             except IndexError:
#                 print('n')
#                 pass
#             else:
#                 possible_actions.append("n")
#
#             print(possible_actions)
#             # Ensure only keys get added when there are actions
#             if len(possible_actions) > 0:
#                 actions[(i, j)] = possible_actions

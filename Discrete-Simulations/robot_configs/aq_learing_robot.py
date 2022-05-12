import numpy as np


def robot_epoch(robot):
    # Hyperparameters
    SMALL_ENOUGH = 0.05
    GAMMA = 0.9
    NOISE = robot.p_move

    # Initialisation
    grid = robot.grid

    actions = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):

            possible_actions = []
            if i == 0 and j == 0:
                possible_actions.append("e")
                possible_actions.append("s")
            elif i == 0 and j == grid.n_cols-1:
                possible_actions.append("e")
                possible_actions.append("n")
            elif j == 0 and i == grid.n_rows-1:
                possible_actions.append("s")
                possible_actions.append("w")
            elif j == grid.n_cols-1 and i == grid.n_rows-1:
                possible_actions.append("w")
                possible_actions.append("n")
            elif i == 0:
                possible_actions.append("e")
                possible_actions.append("s")
                possible_actions.append("w")
            elif j == grid.n_cols-1:
                possible_actions.append("e")
                possible_actions.append("w")
                possible_actions.append("n")
            elif i == grid.n_rows-1:
                possible_actions.append("s")
                possible_actions.append("w")
                possible_actions.append("n")
            elif j == 0:
                possible_actions.append("e")
                possible_actions.append("s")
                possible_actions.append("n")
            else:
                possible_actions.append("e")
                possible_actions.append("s")
                possible_actions.append("w")
                possible_actions.append("n")





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
            print(f"Episode: {episode}")
            episode_count = 1

            # ToDo: Random starting pos
            while not return_true_if_terminal(grid, current_position) and episode_count <= episode_size:
                print(f"Episode_count: {episode_count}")

                action = get_random_action(actions, current_position)

                # ToDo: Possibly greedy
                next_position = get_next_position(action, current_position, actions)
                next_position_reward = get_state_reward(rewards, next_position)

                # Next-Next Rewards * 4
                surrounding_q_values = get_surrounding_q_values(Q_values, next_position)

                Q_values[current_position][action] += learning_rate * (next_position_reward + gamma * np.max(
                    surrounding_q_values) - Q_values[current_position][action])
                episode_count += 1
                print(f"Episode_count: {episode_count}")

                current_position = next_position

        best_direction = np.max(get_surrounding_q_values(Q_values, current_position))
        while robot.orientation != best_direction:
            robot.rotate('r')
        robot.move()

    except Exception as e:
        print(f"Main error: {e}")
        raise e


def get_surrounding_q_values(q_values, position):
    try:
        q_values
        q = [q_values[position]['n'],
                q_values[position]['e'],
                q_values[position]['s'],
                q_values[position]['w'],
                ]
    except Exception as e:
        print(f"get_surrounding_q_values_error: {e}")
        raise e

    return q


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
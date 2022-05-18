import numpy as np
import random

def robot_epoch (robot):
    #Hyperparameters
    SMALL_ENOUGH = 0.05
    GAMMA = 0.9
    NOISE = robot.p_move

    # Initialisation
    grid = robot.grid

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

    # # initial Q values
    # # ToDo: read from robot if there #done
    # try:
    #     Q_values = {}
    #     for i in range(0, grid.n_rows):
    #         for j in range(0, grid.n_cols):
    #             Q_values[(i, j)] = {}
    #             for a in actions[(i, j)]:
    #                 Q_values[(i, j)][a] = 0  # Q value is a dict of dict

    # except Exception as e:
    #     # print(f"Q_values: {robot.q_values}")
    #     print(f"Q_value_error: {e}")
    #     raise e
    #



    try:
        Q_values = robot.q_values
        # for i in range(0, grid.n_rows):
        #     for j in range(0, grid.n_cols):
        #         robot.q_values[(i, j)] = {}
        #         for a in actions[(i, j)]:
        #             robot.q_values[(i, j)][a] = 0
    except:
        Q_values = {}
        for i in range(0, grid.n_rows):
            for j in range(0, grid.n_cols):
                Q_values[(i, j)] = {}
                for a in actions[(i, j)]:
                    Q_values[(i, j)][a] = 0


    #previous line is from SARSA_bot but next we're making the Q-values robot.Q_values
    robot.q_values = Q_values

    print("==========Qvalues===============")



    rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            rewards[(i, j)] = grid.cells[i, j]
    print("==========rewards===============")


    policy = get_greedy_policy(actions, rewards)
    print("===== BEGIN Q/SARSA LEARNING =====")

    # try:
    episode_size = 20
    total_episodes = 50

    # What to do
    learning_rate = 0.1
    gamma = 0.95
    e = 0.1

    try:
        for episode in range(total_episodes):
            print(f"Episode: {episode}")
            episode_count = 1

            #reset to current state s
            current_position = robot.pos

            #choose a from s using policy derived from Q (e.g., ϵ-greedy)
            action = e_greedy_action(e, actions, current_position, policy)

            while not return_true_if_terminal(grid, current_position) and episode_count <= episode_size:
                position_prime = get_next_position(action, current_position, actions)
                next_position_reward = get_state_reward(rewards, position_prime)

                #get next action a' from s', using policy (e-greedy)
                #so take gamma chance to get random action, 1-gamma to get action with max reward
                action_prime = e_greedy_action(e, actions, position_prime, policy)

                Q_values[current_position][action] += learning_rate * (next_position_reward + gamma * Q_values[position_prime][action_prime]
                                                                       - Q_values[current_position][action])

#set            #set next action and state to current action and state
                if grid.cells[position_prime] >=0:
                    #collision detection: only move if not a wall
                    current_position = position_prime
                action = action_prime

                # update policy & rewards
                rewards[position_prime] = 0
                policy = get_greedy_policy(actions, rewards)

                episode_count += 1

        best_direction = get_max_surrounding_direction(Q_values, current_position)
        print("BEST DIRECTION")
        print(best_direction)
        print(robot.orientation)
        while robot.orientation != best_direction:
            robot.rotate('r')
        robot.move()
        # ToDo: Save Q_values into robot
        robot.q_values = Q_values

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


def e_greedy_action(e, actions, position, policy):
    """
    e-greedily picks an action to take next:
    chance of e to take a random possible action
    otherwise take an action according to greedy policy

    e: chance for random action
    actions: what actions are possible for each state
    position: current position/state
    policy: policy of what action is best in each position
    """
    if random.random() < e:
        #take random action
        return random.choice(actions[position])
    else:
        #take greedy action
        return policy[position]

#
# def get_max_reward_of_surrounding_states(state, rewards):
#     actions = ['n', 'w', 's', 'e']
#     surrounding_states = []
#     surrounding_states.append(get_next_state())


def get_state_reward(rewards, s):
    return rewards[s]

def get_greedy_policy(actions, rewards):
    """Creates a greedy policy"""
    policy = {}
    for s in actions.keys():
        local_rewards = {}
        for action in actions[s]:
            local_rewards[action] = rewards[get_next_position(action, s, actions)]

        policy[s] = max(local_rewards, key=local_rewards.get)
    return policy






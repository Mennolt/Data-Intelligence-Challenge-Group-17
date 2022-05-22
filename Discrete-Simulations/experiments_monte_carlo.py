# Import our robot algorithm to use in this simulation:
#from robot_configs.greedy_random_robot import robot_epoch as greedy_epoch
#from robot_configs.infinite_view_robot import robot_epoch as infinite_view_epoch
#from robot_configs.other.rotatorinator import robot_epoch as rotator_epoch
from robot_configs.monte_carlo import robot_epoch as monte_carlo_epoch

import pickle
from environment import Robot
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

experiment_file_name = 'test_experiments_monte_carlo'
runs = 1
battery_drainage_lambda = 1

# All variables we can change for our experiments

# Each grid has a certain number of tiles, but in some cases only a selected number of these tiles can
# be visite (because of walls). We want to know whether we cleaned all reachable walls, therefore we
# have a cleanliness criterion for each grid. Later we can adjust our percentage, to be relative to
# this current percentage.
grid_files = {'death_room': 96.83, 'empty_small_room': 100,
              'empty_big_room': 100, 'example-random-house-0': 100,
              'example-random-house-4': 84.04, 'house': 100}

battery_drainages_p = [0.2]
robot_epoch = (monte_carlo_epoch, 'monte_carlo')

epsilon_settings = [0.05, 0.1, 0.2]
epochs_settings = [10, 30, 50]
episode_steps_settings = [20, 50, 100]
discount_factor_settings = [0.05, 0.1, 0.2]

# In the lists below, we gather data.
robot_per_setting = []
grid_per_setting = []
battery_per_setting = []
epsilon_per_setting = []
epochs_per_setting = []
episode_steps_per_setting = []
discount_factor_per_setting = []

cleaned = []
efficiencies = []
time_taken = []

# Counter to keep track of how far we are in our experiments (relative to total_count).
counter = 1
total_count = len(grid_files)*len(epsilon_settings)*len(epochs_settings)*len(episode_steps_settings)*len(discount_factor_settings)

for grid_file, stopping_criterion in grid_files.items(): #6
    for epsilon in epsilon_settings: #3
        for epochs in epochs_settings: #3
            for episode_steps in episode_steps_settings: #3
                for discount_factor in discount_factor_settings: #3
                    # Only usable when we do multiple runs per settings
                    #efficiencies = []
                    #n_moves = []
                    deaths = 0
                    #cleaned = []
                    #times = []

                    start = time.time()
                    # Open the grid file.
                    # (You can create one yourself using the provided editor).

                    with open(f'grid_configs/{grid_file}.grid', 'rb') as f:
                        grid = pickle.load(f)

                    # Calculate the total visitable tiles:
                    n_total_tiles = (grid.cells >= 0).sum()
                    # Spawn the robot at (1,1) facing north with battery drainage enabled:
                    robot = Robot(grid, (1, 1), orientation='n', battery_drain_p=0.15,
                                  battery_drain_lam=battery_drainage_lambda)
                    # Keep track of the number of robot decision epochs:
                    n_epochs = 0

                    while True:
                        n_epochs += 1
                        # Do a robot epoch (basically call the robot algorithm once):
                        robot_epoch[0](robot, epsilon, epochs, episode_steps, discount_factor)
                        # Stop this simulation instance if robot died :( :
                        if not robot.alive:
                            deaths += 1
                            break
                        # Calculate some statistics:
                        clean = (grid.cells == 0).sum()
                        dirty = (grid.cells >= 1).sum()
                        goal = (grid.cells == 2).sum()
                        # Calculate the cleaned percentage:
                        clean_percent = (clean / (dirty + clean)) * 100
                        # See if the room can be considered clean, if so, stop the simulation instance:
                        if clean_percent >= stopping_criterion-0.01 and goal == 0:
                            # Here we divide by the threshold, because there are more tiles considered
                            # in the equation than there are dirty tiles. We want our score relative to
                            # the number of initially dirty tiles.
                            clean_percent = clean_percent / grid_files[grid_file] * 100
                            break
                        # Calculate the effiency score:
                        moves = [(x, y) for (x, y) in zip(robot.history[0], robot.history[1])]
                        u_moves = set(moves)
                        n_revisted_tiles = len(moves) - len(u_moves)
                        efficiency = (100 * n_total_tiles) / (n_total_tiles + n_revisted_tiles)

                        # Only usable when we do multiple runs per settings
                        # Keep track of the last statistics for each simulation instance:
                        #efficiencies.append(float(efficiency))
                        #n_moves.append(len(robot.history[0]))
                        #cleaned.append(clean_percent)

                    print(f'{counter} done out of {total_count}')
                    counter += 1

                    end = time.time()

                    grid_per_setting.append(grid_file)
                    epsilon_per_setting.append(epsilon)
                    epochs_per_setting.append(epochs)
                    episode_steps_per_setting.append(episode_steps)
                    discount_factor_per_setting.append(discount_factor)

                    cleaned.append(clean_percent)
                    #std_cleaned.append(np.std(cleaned))
                    efficiencies.append(float(efficiency))
                    #std_efficiency.append(np.std(efficiencies))
                    time_taken.append(end-start)
                    #std_time_taken.append(np.std(times))


data_matrix =  list(zip(grid_per_setting, epsilon_per_setting, epochs_per_setting,
                        episode_steps_per_setting, discount_factor_per_setting,
                        cleaned, efficiencies, time_taken))
column_names = ['grid', 'epsilon', 'epochs',
                'steps_per_episode', 'discount_factor',
                'cleaned', 'efficiency', 'time_taken']

results_df = pd.DataFrame(data_matrix, columns=column_names)
results_df.to_csv(f'experiment_results/{experiment_file_name}.csv', index=False)
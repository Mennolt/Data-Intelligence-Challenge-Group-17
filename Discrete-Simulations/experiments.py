# Import our robot algorithm to use in this simulation:
from robot_configs.greedy_random_robot import robot_epoch as greedy_epoch
from robot_configs.rotatorinator import robot_epoch as rotator_epoch

import pickle
from environment import Robot
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

experiment_file_name = 'test_experiments_more_levels'
runs = 30
stopping_criterion = 100
battery_drainage_lambda = 1

# All variables we can change for our experiments
"""grid_files = ['house', 'example-random-house-0', 'example-random-house-1',
              'example-random-house-2', 'example-random-house-3',
              'example-random-house-4', 'example-random-level']"""

grid_files = ['death', 'death_room', 'empty_small_room',
              'empty_big_room', 'example-random-house-0',
              'example-random-house-1', 'example-random-house-2',
              'example-random-house-3', 'example-random-house-4',
              'goal_room', 'house', 'snake', 'obstacle_room',
              'no_obstacle_room', 'example-random-level']

#death_tiles_bools = [True, False]
battery_drainages_p = [0.1, 0.3, 0.5]
robots_epoch = [(greedy_epoch, 'greedy_random'), (rotator_epoch, 'rotator')]

robot_per_setting = []
grid_per_setting = []
battery_per_setting = []

mean_cleaned = []
std_cleaned = []
mean_efficiency = []
std_efficiency = []
mean_time_taken = []
std_time_taken = []

counter = 1
total_count = len(grid_files)*len(battery_drainages_p)*len(robots_epoch)*runs

for grid_file in grid_files:  # 7 different grids
    for battery_drainage_p in battery_drainages_p: # 3 different settings
        for robot_epoch in robots_epoch: # 2 different robots
            efficiencies = []
            n_moves = []
            deaths = 0
            cleaned = []
            times = []

            for i in range(runs): # ? runs
                start = time.time()
                # Open the grid file.
                # (You can create one yourself using the provided editor).

                with open(f'grid_configs/{grid_file}.grid', 'rb') as f:
                    grid = pickle.load(f)

                #with open(f'grid_configs/{grid_files[-2]}', 'rb') as f:
                #    grid = pickle.load(f)

                # Calculate the total visitable tiles:
                n_total_tiles = (grid.cells >= 0).sum()
                # Spawn the robot at (1,1) facing north with battery drainage enabled:
                robot = Robot(grid, (1, 1), orientation='n', battery_drain_p=battery_drainage_p,
                              battery_drain_lam=battery_drainage_lambda)
                # Keep track of the number of robot decision epochs:
                n_epochs = 0

                while True:
                    n_epochs += 1
                    # Do a robot epoch (basically call the robot algorithm once):
                    robot_epoch[0](robot)
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
                    if clean_percent >= stopping_criterion and goal == 0:
                        break
                    # Calculate the effiency score:
                    moves = [(x, y) for (x, y) in zip(robot.history[0], robot.history[1])]
                    u_moves = set(moves)
                    n_revisted_tiles = len(moves) - len(u_moves)
                    efficiency = (100 * n_total_tiles) / (n_total_tiles + n_revisted_tiles)

                # Keep track of the last statistics for each simulation instance:
                efficiencies.append(float(efficiency))
                n_moves.append(len(robot.history[0]))
                cleaned.append(clean_percent)

                print(f'{counter} done out of {total_count}')
                counter += 1

                end = time.time()
                times.append(end-start)


            robot_per_setting.append(robot_epoch[1])
            grid_per_setting.append(grid_file)
            battery_per_setting.append(battery_drainage_p)

            mean_cleaned.append(np.mean(cleaned))
            std_cleaned.append(np.std(cleaned))
            mean_efficiency.append(np.mean(efficiencies))
            std_efficiency.append(np.std(efficiencies))
            mean_time_taken.append(np.mean(times))
            std_time_taken.append(np.std(times))



data_matrix =  list(zip(robot_per_setting, grid_per_setting, battery_per_setting,
                        mean_cleaned, std_cleaned, mean_efficiency, std_efficiency,
                        mean_time_taken, std_time_taken))
column_names = ['robot', 'grid', 'battery_p', 'mean_cleaned', 'std_cleaned',
                'mean_efficiency', 'std_efficiency', 'mean_time_taken',
                'std_time_taken']

results_df = pd.DataFrame(data_matrix, columns=column_names)
results_df.to_csv(f'experiment_results/{experiment_file_name}.csv', index=False)
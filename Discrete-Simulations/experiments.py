# Import our robot algorithm to use in this simulation:
from robot_configs.greedy_random_robot import robot_epoch
import pickle
from environment import Robot
import pandas as pd
import matplotlib.pyplot as plt

# All variables we can change for our experiments
experiment_file_name = 'test_experiments'
grid_files = ['death.grid', 'empty.grid', 'example-random-house-0.grid', 'example-random-house-1.grid',
              'example-random-house-2.grid', 'example-random-house-3.grid', 'example-random-house-4.grid',
              'example-random-level.grid', 'house.grid', 'snake.grid']
stopping_criteria = [100] # Cleaned tile percentage at which the room is considered 'clean'
runs = 100

# Keep track of some statistics:
efficiencies = []
n_moves = []
deaths = 0
cleaned = []

# Run 100 times:
for i in range(runs):
    # Open the grid file.
    # (You can create one yourself using the provided editor).
    with open(f'grid_configs/{grid_files[-2]}', 'rb') as f:
        grid = pickle.load(f)
    # Calculate the total visitable tiles:
    n_total_tiles = (grid.cells >= 0).sum()
    # Spawn the robot at (1,1) facing north with battery drainage enabled:
    robot = Robot(grid, (1, 1), orientation='n', battery_drain_p=0.5, battery_drain_lam=2)
    # Keep track of the number of robot decision epochs:
    n_epochs = 0

    while True:
        n_epochs += 1
        # Do a robot epoch (basically call the robot algorithm once):
        robot_epoch(robot)
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
        if clean_percent >= stopping_criteria[0] and goal == 0:
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


results_df = pd.DataFrame(list(zip(efficiencies, n_moves, cleaned)), columns=['efficiencies', 'n_moves', 'cleaned'])
results_df.to_csv(f'experiment_results/{experiment_file_name}.csv', index=False)


# Make some plots:
plt.hist(cleaned)
plt.title('Percentage of tiles cleaned.')
plt.xlabel('% cleaned')
plt.ylabel('count')
plt.show()

plt.hist(efficiencies)
plt.title('Efficiency of robot.')
plt.xlabel('Efficiency %')
plt.ylabel('count')
plt.show()

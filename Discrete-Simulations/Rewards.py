def get_rewards(grid, robot = None, return_battery = 20):
    """
    Gets rewards for each tile based on what is in it and the robot battery level.
    inputs:
    Grid: Grid of cells for which rewards are made
    Robot: Robot for which rewards are made
    return_battery: value indicating when robot should go into return to charger mode

    Output: Dict{Tuple(x,y) : int}"""
    rewards = {}
    for i in range(0, grid.n_cols):
        for j in range(0, grid.n_rows):
            val = grid.cells[i, j]
            if robot == None:
                if val < -2:
                    rewards[(i, j)] = 0
                elif val == -1 or val == -2:
                    rewards[(i, j)] = -1
                elif val == 3:
                    rewards[(i, j)] = -10
                elif val == 2:
                    rewards[(i, j)] = 5
                elif val == 1:
                    rewards[(i, j)] = 1
                elif val == 4:
                    rewards[(i, j)] = 0
                elif val == 0:
                    rewards[(i, j)] = 0
                else:
                    rewards[(i, j)] = grid.cells[(i, j)]
            elif robot.battery_lvl > return_battery:
                if val < -2:
                    rewards[(i, j)] = 0
                elif val == -1 or val == -2:
                    rewards[(i, j)] = -1
                elif val == 3:
                    rewards[(i, j)] = -10
                elif val == 2:
                    rewards[(i, j)] = 5
                elif val == 1:
                    rewards[(i, j)] = 1
                elif val == 4:
                    rewards[(i, j)] = 100 / robot.battery_lvl
                elif val == 0:
                    rewards[(i, j)] = 0
                else:
                    rewards[(i, j)] = grid.cells[(i, j)]
            else:
                if val == 4:
                    rewards[(i, j)] = 1000
                elif val == -1 or val == -2:
                    rewards[(i, j)] = -1
                else:
                    rewards[(i, j)] = 0
    return rewards
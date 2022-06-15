import numpy as np


def robot_epoch(robot):
    # Hyperparameters

    # Initialisation
    copy_grid = robot.grid.copy()
    custom_grid = custom_rewards_grid(copy_grid)

    # print(f'Grid: \n {copy_grid.cells.T}')
    # print(f'Custom Grid: \n {custom_grid.cells.T}')

    x, y = robot.pos
    print(x,y)

    e = custom_grid.cells[x + 1, y]
    s = custom_grid.cells[x, y + 1]
    n = custom_grid.cells[x, y - 1]
    w = custom_grid.cells[x - 1, y]

    arr = [e, s, n, w]
    print(f'array: {arr}')
    max_index = arr.index(max(arr))
    print(f'max_indes: {max_index}')

    if max_index == 0:
        print('e')
        while robot.orientation != 'e':
            robot.rotate('r')
        robot.move()
    elif max_index == 1:
        print('s')
        while robot.orientation != 's':
            robot.rotate('r')
        robot.move()
    elif max_index == 2:
        print('n')
        while robot.orientation != 'n':
            robot.rotate('r')
        robot.move()
    elif max_index == 3:
        print('w')
        while robot.orientation != 'w':
            robot.rotate('r')
        robot.move()
    else:
        print('else')
        while robot.orientation != 'e':
            robot.rotate('r')
        robot.move()



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
                    grid.cells[i, j] = 1
                # Self/Robot
                elif grid.cells[i, j] in [-3, -4, -5, -6]:
                    grid.cells[i, j] = 0
                else:
                    raise ValueError(f"value: {grid.cells[i, j]}")
    return grid

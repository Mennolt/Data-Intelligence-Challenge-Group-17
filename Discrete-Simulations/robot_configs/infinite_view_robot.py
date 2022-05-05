import numpy as np


def robot_epoch(robot):
    """
    Idea:
    :param robot:
    :return:
    """
    print(robot.grid.cells, len(robot.grid.cells[0]), robot.grid.n_cols, robot.grid.n_rows)
    # Get the possible values (dirty/clean/wall) of the 4 tiles we can end up at after a move:
    possible_tiles = robot.possible_tiles_after_move()
    #print(possible_tiles)

    #step 1: get value of entire grid
    #try to get value from robot, if not init it
    try:
        values = robot.val_grid
    except:
        values = np.zeros((robot.grid.n_cols+5, robot.grid.n_rows+5))#way too large to prevent index eror
    #get the value of the grid
    values = value_update(robot.grid, values)
    robot.val_grid = values

    #step 2: move to thing with highest value
    #check each neighbour, determine desired direction
    max_val = -1
    des_dir = "n"
    pos = robot.pos
    if pos[0] > 0:

        if values[pos[0] - 1, pos[1]] > max_val:
            des_dir = 'w'#(-1,0)
            max_val = values[pos[0] - 1, pos[1]]
    if pos[0] < robot.grid.n_cols-1:
        if values[pos[0] + 1, pos[1]] > max_val:
            des_dir = 'e' #(1,0)
            max_val = values[pos[0] + 1, pos[1]]

    if pos[1] > 0:
        if values[pos[0], pos[1] - 1] > max_val:
            des_dir = 'n'#(0,-1)
            max_val = values[pos[0], pos[1] - 1]
    if pos[1] < robot.grid.n_rows - 1:
        if values[pos[0], pos[1] + 1] > max_val:
            des_dir = 's'#(0,1)
            max_val = values[pos[0], pos[1] + 1]

    print(robot.orientation, des_dir)
    while robot.orientation != des_dir:
        robot.rotate('r')
    robot.move()

    print(values)
    #print(des_dir)
    #get to desired direction or move




def value_update(grid, values):
    """
    Takes a grid and its values and updates the value of each square in it according to the following rules:
    target: 10
    dirty: 2 or 0.5*highest neighbour
    clean: 0.5*highest neighbour
    """
    new_values = values.copy()
    for j in range(grid.n_cols):
        for i in range(grid.n_rows):
            #get item:
            try:
                square = grid.cells[i,j]
                #get value of each neighbour
                neighbour_vals = []
                if i>0:

                    neighbour_vals.append(values[i-1,j])
                if i < grid.n_rows-1:
                    neighbour_vals.append(values[i + 1, j])

                if j>0:
                    neighbour_vals.append(values[i,j-1])
                if j<grid.n_cols-1:
                    neighbour_vals.append(values[i, j + 1])
                #determine new value of item
                if square == 2:
                    #goals
                    new_values[i,j] = 5
                elif square == -1 or square == -2:
                    #walls and obstacles
                    new_values[i,j] = -1
                elif square == 1:
                    #dirty square
                    new_values[i,j] = max(0.5*max(neighbour_vals),2)
                elif square == 0:
                    #cleaned square
                    new_values[i,j] = 0.5*max(neighbour_vals)
                else:
                    #contains robot
                    new_values[i,j] = 0
            except IndexError:
                print(f"{i},{j} out of range for grid.")
    #print(new_values)
    return new_values

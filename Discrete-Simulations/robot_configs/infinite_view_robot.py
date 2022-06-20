import numpy as np

np.set_printoptions(precision=3, suppress = True)

def robot_epoch(robot):
    """
    Robot using simple algorithm to clean, used as baseline
    Robot gives each tile a value at start of cleaning. For each move, updates values once using simple rules then makes a move.
    :param robot:
    :return: None
    """

    #step 1: get value of entire grid
    #try to get value from robot, if not init it
    try:
        values = robot.val_grid
    except:
        values = np.zeros((robot.grid.n_rows, robot.grid.n_cols))
    #get the value of the grid
    values = value_update(robot.grid, values)
    robot.val_grid = values

    #step 2: move to thing with highest value
    #check each neighbour, determine desired direction
    max_val = -1
    des_dir = "n"
    pos = robot.pos


    if pos[1] > 0: #not against top

        if values[pos[1]-1, pos[0]] > max_val:
            des_dir = 'n'#(-1,0)
            max_val = values[pos[1]-1 , pos[0]]
    if pos[1] < values.shape[0]-1: #robot.grid.n_rows-1: #not against bottom
        if values[pos[1]+1, pos[0]] > max_val:
            des_dir = 's' #(1,0)
            max_val = values[pos[1]+1, pos[0]]

    if pos[0] > 0: #not against left end
        if values[pos[1], pos[0]-1] > max_val:
            des_dir = 'w'#(0,-1)
            max_val = values[pos[1], pos[0]-1]
    if pos[0] < values.shape[1]-1:#robot.grid.n_rows - 1:#not against right end
        if values[pos[1], pos[0]+1] > max_val:
            des_dir = 'e'#(0,1)


    while robot.orientation != des_dir:
        robot.rotate('r')
    robot.move()


def value_update(grid, values):
    """
    Takes a grid and its values and updates the value of each square in it according to the following rules:
    target: 10
    dirty: 2 or 0.5*highest neighbour
    clean: 0.5*highest neighbour
    """
    new_values = values.copy()
    # remember that in values we are working transposed compared to grid visible in app
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            #get item:
            try:
                square = grid.cells[j,i]
                #get value of each neighbour
                neighbour_vals = []
                if i>0:

                    neighbour_vals.append(values[i-1,j])
                if i < values.shape[0]-1:
                    neighbour_vals.append(values[i + 1, j])

                if j>0:
                    neighbour_vals.append(values[i,j-1])
                if j<values.shape[1]-1:
                    neighbour_vals.append(values[i, j + 1])
                #determine new value of item
                if square == 2:
                    #goals
                    new_values[i,j] = 10
                elif square == -1 or square == -2:
                    #walls and obstacles
                    new_values[i,j] = -1
                elif square == 1: #or square == 3:
                    #dirty square #or death square
                    new_values[i,j] = max(0.5*max(neighbour_vals),2)
                elif square == 0:
                    #cleaned square
                    new_values[i,j] = 0.5*max(neighbour_vals)
                else:
                    #contains robot, 1000 is easy to find in the prints
                    new_values[i,j] = -1000
            except IndexError:
                pass
    return new_values

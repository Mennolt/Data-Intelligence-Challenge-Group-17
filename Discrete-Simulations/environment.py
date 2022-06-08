import numpy as np
import random


class Robot:
    def __init__(self, grid, pos: tuple, orientation: dict, p_move=0, battery_drain_p=0, battery_drain_lam=0, vision=1):
        # hitbox values relative to robot positions
        self.hitbox = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        #locations the robot can clean, relative to robot position
        #must contain (0,0)
        self.cleanable = [(0,0), (-1,0), (1,0)]
        self.pos = pos
        self.grid = grid
        # this is the grid value under the robot
        # used to make robots not eat chargers
        self.under_val = grid.cells[pos[0], pos[1]]

        if not self.check_hitbox(pos):
            raise ValueError
        self.orientation = orientation
        self.orients = {'n': -3, 'e': -4, 's': -5, 'w': -6}
        self.dirs = {'n': (0, -1), 'e': (1, 0), 's': (0, 1), 'w': (-1, 0)}
        self.grid.cells[pos] = self.orients[self.orientation]
        self.history = [[], []]
        self.p_move = p_move
        self.battery_drain_p = battery_drain_p
        self.battery_drain_lam = battery_drain_lam
        self.battery_lvl = 100
        self.alive = True
        self.vision = vision

        self.q_values = {}
        self.q_values_calculated = False




    def init_q_values(self, actions):
        #print(actions)

        # initial Q values
        try:
            self.q_values = {}
            for i in range(0, self.grid.n_cols):
                for j in range(0, self.grid.n_rows):
                    self.q_values[(i, j)] = {}
                    for a in actions[(i, j)]:
                        self.q_values[(i, j)][a] = 0  # Q value is a dict of dict
        except Exception as e:
            # print(f"Q_values: {Q_values}")
            print(f"Q_value_error: {e}")
            raise e

    def possible_tiles_after_move(self):
        moves = list(self.dirs.values())
        # Fool the robot and show a death tile as normal (dirty)
        data = {}
        for i in range(self.vision):
            for move in moves:
                to_check = tuple(np.array(self.pos) + (np.array(move) * (i + 1)))
                if to_check[0] < self.grid.cells.shape[0] and to_check[1] < self.grid.cells.shape[1] and to_check[
                    0] >= 0 and to_check[1] >= 0:
                    data[tuple(np.array(move) * (i + 1))] = self.grid.cells[to_check]
                    # Show death tiles as dirty:
                    if data[tuple(np.array(move) * (i + 1))] == 3:
                        data[tuple(np.array(move) * (i + 1))] = 1
        return data

    def move(self):
        # Can't move if we're dead now, can we?
        if not self.alive:
            return False
        random_move = np.random.binomial(1, self.p_move)
        do_battery_drain = np.random.binomial(1, self.battery_drain_p)
        if do_battery_drain == 1 and self.battery_lvl > 0:
            self.battery_lvl -= np.random.exponential(self.battery_drain_lam)
        # Handle empty battery:
        if self.battery_lvl <= 0:
            self.alive = False
            return False
        if random_move == 1:
            moves = self.possible_tiles_after_move()
            random_move = random.choice([move for move in moves if moves[move] >= 0])
            new_pos = tuple(np.array(self.pos) + random_move)
            # Only move to non-blocked tiles:
            if self.check_hitbox(new_pos):
                new_orient = list(self.dirs.keys())[list(self.dirs.values()).index(random_move)]
                tile_after_move = self.grid.cells[new_pos]
                # clean cleanable tiles, if goal or dirty
                for loc in self.cleanable:
                    if loc == (0,0):
                        #clean the tile under the robot,
                        if self.under_val == 1 or self.under_val == 2:
                            # only clean dirty and goal tiles
                            self.grid.cells[self.pos] = 0
                        else:
                            self.grid.cells[self.pos] = self.under_val
                    else:
                        coord = tuple([i+j for i,j in zip(loc, self.pos)])
                        if self.grid.cells[coord] in [1,2]:
                            self.grid.cells[coord] = 0


                # replace tile under robot
                self.under_val = self.grid.cells[new_pos]
                #change robot location
                self.grid.cells[new_pos] = self.orients[new_orient]
                self.pos = new_pos
                self.history[0].append(self.pos[0])
                self.history[1].append(self.pos[1])
                #Death:
                if tile_after_move == 3:
                    self.alive = False
                    return False
                return True
            else:
                return False
        else:
            new_pos = tuple(np.array(self.pos) + self.dirs[self.orientation])
            # Only move to non-blocked tiles:
            if self.check_hitbox(new_pos):
                tile_after_move = self.grid.cells[new_pos]
                #clean cleanable tiles, if goal or dirty
                for loc in self.cleanable:
                    if loc == (0, 0):
                        # clean the tile under the robot,
                        if self.under_val == 1 or self.under_val == 2:
                            # only clean dirty and goal tiles
                            self.grid.cells[self.pos] = 0
                        else:
                            self.grid.cells[self.pos] = self.under_val
                    else:
                        coord = tuple([i + j for i, j in zip(loc, self.pos)])
                        if self.grid.cells[coord] in [1, 2]:
                            self.grid.cells[coord] = 0
                #replace tile under robot
                self.under_val = self.grid.cells[new_pos]
                #change robot location
                self.grid.cells[new_pos] = self.orients[self.orientation]
                self.pos = new_pos
                self.history[0].append(self.pos[0])
                self.history[1].append(self.pos[1])
                # Death:
                if tile_after_move == 3:
                    self.alive = False
                    return False
                return True
            else:
                return False

    def rotate(self, dir: dict):
        current = list(self.orients.keys()).index(self.orientation)
        if dir == 'r':
            self.orientation = list(self.orients.keys())[(current + 1) % 4]
        elif dir == 'l':
            self.orientation = list(self.orients.keys())[current - 1]
        self.grid.cells[self.pos] = self.orients[self.orientation]

    def check_hitbox(self, pos):
        """Checks whether the hitbox allows the robot to stand in this position
        by checking if all grid cells inside the hitbox are non-negative
        Returns True if robot can be here, False otherwise"""
        for location in self.hitbox:
            coord = tuple([i+j for i,j in zip(location, pos)])
            if self.grid.cells[coord] == -1 or self.grid.cells[coord] == -2:
                return False
        return True

    def plot_hitbox(self, temp_grid):
        """
        Replaces values of grid that are within hitbox with those for a robot hitbox
        """
        for location in self.hitbox:
            if location != (0,0):
                coord = tuple([i + j for i, j in zip(location, self.pos)])
                temp_grid.cells[coord] = -10
        return temp_grid

class Grid:
    def __init__(self, n_cols: int, n_rows: int):
        self.n_rows = n_rows
        self.n_cols = n_cols
        # Building the boundary of the grid:
        self.cells = np.ones((n_cols, n_rows))
        self.cells[0, :] = self.cells[-1, :] = -1
        self.cells[:, 0] = self.cells[:, -1] = -1

    def put_obstacle(self, x0, x1, y0, y1, from_edge=1):
        self.cells[max(x0, from_edge):min(x1 + 1, self.n_cols - from_edge),
        max(y0, from_edge):min(y1 + 1, self.n_rows - from_edge)] = -2

    def put_singular_obstacle(self, x, y):
        self.cells[x][y] = -2

    def put_singular_goal(self, x, y):
        self.cells[x][y] = 2

    def put_singular_death(self, x, y):
        self.cells[x][y] = 3

    def copy(self):
        grid = Grid(self.n_cols, self.n_rows)
        grid.cells = self.cells.copy()
        return grid


def generate_grid(n_cols: int, n_rows: int):
    # Placeholder function used to generate a grid.
    # Select an empty grid file in the user interface and add code her to automatically fill it.
    # Look at grid_generator.py for inspiration.
    grid = Grid(n_cols, n_rows)
    return grid

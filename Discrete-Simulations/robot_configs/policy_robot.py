import random


def robot_epoch(robot):
    # Get the possible tiles after move
    possible_tiles = robot.possible_tiles_after_move()
    # Randomly select where to go based on policy
    des_dir = ''
    rand_val = random.random()
    total = 0
    for k, v in robot.policy[robot.pos[0]][robot.pos[1]]:
        total += v
        if rand_val <= total:
            selection = k
    while robot.orientation != des_dir:
        robot.rotate('r')
    robot.move()
import numpy as np

def robot_epoch(robot, policy):
    """
    A robot_epoch function for each actual robot, so that the environment still works.
    This function basically only picks the best policy for its robot.

    Input:
    Robot - a Robot class instance
    Policy - the overall policy for this particular robot
    """
    best_direction = policy[robot.pos]

    while robot.orientation != best_direction:
        robot.rotate('r')

    robot.move()
    # print('moved', best_direction)
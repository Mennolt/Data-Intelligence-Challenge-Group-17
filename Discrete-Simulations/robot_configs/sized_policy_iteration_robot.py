import robot_configs.policy_iteration_robot as policy_iteration_epoch


def robot_epoch(robot):
    size = [(0, 0), (0, -1), (0, 1)]
    robot.set_size_option(size)
    policy_iteration_epoch.robot_epoch(robot)

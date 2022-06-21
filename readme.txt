# Cleaning robot simulator group 17

This project simulates a robot or group of robots cleaning rooms or houses.
It is made to have some versatility, allowing different robot sizes and allowing robots to work together.


## User Guide:
### Running basic simulations
To run the most basic version of the program, run the file app.py using a python 3.7 or up.
Install any modules it asks for. If you have all modules a message will pop up saying where the app is running.
By default this is http://127.0.0.1:5000/. Go to this address using a browser.
Then select the desired grid and robot. Choose the robot "policy_iteration_robot".
This is the only robot that works for different sizes of robot correctly. The next line allows changing further settings.
Now use the button "Load grid" to actually load the chosen grid, and "Get robot" to put your robots on the grid.
Run the simulation by pressing "Start simulation"

### Running simulations with a hivemind
To run simulations that use a hivemind to have multiple robots work together better, run the file app_hive.py with python 3.7 or up.
Install any modules it asks for. If you have all modules a message will pop up saying where the app is running.
By default this is http://127.0.0.1:5000/. Go to this address using a browser.
Then select the desired grid and robot. Choose the robot "policy_iter_unit".
On the line with the settings, make sure to have at least 2 robots. Also make sure to change their starting locations to not overlap.
Then use the button "Load grid" to actually load the chosen grid, and "Get robot" to put your robots on the grid.
Run the simulation by pressing "Start simulation"

### Adjusting robot sizes
To change the sizes of robots, some changes in code are required. Go to the file used for the simulation you are using.
In the file app.py, go to line 196. In the file app_hive.py, go to line 193. There, change the parameter "hitbox" to create the hitbox you desire.
The hitbox is made by making a list of locations relative to the robot. For example, [(-1,0), (0,0), (1,0)] creates a line shaped robot.
Make sure the hitbox contains the value (0,0). After this is edited, run the file and spawn the robots.
Make sure their locations are set so they do not overlap any walls while spawning.

### Recreating experiments
All experiments were done in files which have "experiments" in their name,
to recreate experiment results run these files with python 3.7 or higher.






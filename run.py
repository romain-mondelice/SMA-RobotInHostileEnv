from core.model import RobotMissionModel
from visualization.server import server

# Set the model parameters
width = 20
height = 20
num_green_robots = 5
num_yellow_robots = 3
num_red_robots = 2
num_green_wastes = 10
num_yellow_wastes = 5
num_red_wastes = 3

# Create a new instance of the RobotMissionModel
model = RobotMissionModel(
    width=width,
    height=height,
    num_green_robots=num_green_robots,
    num_yellow_robots=num_yellow_robots,
    num_red_robots=num_red_robots,
    num_green_wastes=num_green_wastes,
    num_yellow_wastes=num_yellow_wastes,
    num_red_wastes=num_red_wastes
)

# Run the simulation
server.launch()
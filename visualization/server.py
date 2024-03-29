from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from core.model import RobotMissionModel
from agents.agents import GreenRobotAgent, YellowRobotAgent, RedRobotAgent
from agents.object_agents import Waste, Radioactivity, WasteDisposalZone

def agent_portrayal(agent):
    if isinstance(agent, GreenRobotAgent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "green",
                     "r": 0.5}
    elif isinstance(agent, YellowRobotAgent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "yellow",
                     "r": 0.5}
    elif isinstance(agent, RedRobotAgent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "red",
                     "r": 0.5}
    elif isinstance(agent, Waste):
        if agent.waste_type == "green":
            color = "green"
        elif agent.waste_type == "yellow":
            color = "yellow"
        else:
            color = "red"
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": color,
                     "w": 0.8,
                     "h": 0.8}
    elif isinstance(agent, Radioactivity):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "gray",
                     "w": 1,
                     "h": 1}
    elif isinstance(agent, WasteDisposalZone):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "black",
                     "w": 1,
                     "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

model_params = {
    "width": 20,
    "height": 20,
    "num_green_robots": Slider("Number of Green Robots", 5, 1, 10, 1),
    "num_yellow_robots": Slider("Number of Yellow Robots", 3, 1, 10, 1),
    "num_red_robots": Slider("Number of Red Robots", 2, 1, 10, 1),
    "num_wastes": Slider("Number of Initial Wastes", 10, 1, 20, 1),
}

server = ModularServer(RobotMissionModel,
                       [grid],
                       "Robot Mission Model",
                       model_params)
server.port = 8521
server.launch()
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from core.model import RobotMissionModel
from agents.agents import GreenRobotAgent, YellowRobotAgent, RedRobotAgent
from agents.object_agents import Waste, Radioactivity, WasteDisposalZone

def agent_portrayal(agent):
    if isinstance(agent, GreenRobotAgent):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "green",
                     "w": 0.5,
                     "h": 0.5,
                     "text": str(len(agent.wastes_carried)),
                     "text_color": "white"}
    elif isinstance(agent, YellowRobotAgent):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "yellow",
                     "w": 0.5,
                     "h": 0.5,
                     "text": str(len(agent.wastes_carried)),
                     "text_color": "white"}
    elif isinstance(agent, RedRobotAgent):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "red",
                     "w": 0.5,
                     "h": 0.5,
                     "text": str(len(agent.wastes_carried)),
                     "text_color": "white"}
    elif isinstance(agent, Waste):
        if agent.waste_type == "green":
            color = "green"
        elif agent.waste_type == "yellow":
            color = "yellow"
        else:
            color = "red"
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": color,
                     "r": 0.5}
    elif isinstance(agent, Radioactivity):
        level = agent.level
        original_color = (int(255 * level), int(255 * (1 - level)), 0)

        white = (255, 255, 255)
        pastel_factor = 0.7
        pastel_color = tuple(int(original * (1 - pastel_factor) + white * pastel_factor) for original, white in zip(original_color, white))
        
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "#{:02x}{:02x}{:02x}".format(*pastel_color),
                    "w": 1,
                    "h": 1}
    elif isinstance(agent, WasteDisposalZone):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "black",
                     "w": 0.8,
                     "h": 0.8}
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

model_params = {
    "width": 20,
    "height": 20,
    "num_green_robots": Slider("Number of Green Robots", 5, 1, 10, 1),
    "num_yellow_robots": Slider("Number of Yellow Robots", 3, 1, 10, 1),
    "num_red_robots": Slider("Number of Red Robots", 2, 1, 10, 1),
    "num_wastes": Slider("Number of Initial Wastes", 10, 1, 20, 1)
}

server = ModularServer(RobotMissionModel,
                       [grid],
                       "Robot Mission Model",
                       model_params)
server.port = 8521
server.launch()
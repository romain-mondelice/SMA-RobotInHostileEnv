from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents.agents import GreenRobotAgent, YellowRobotAgent, RedRobotAgent
from agents.object_agents import Radioactivity, WasteDisposalZone, Waste
from core.schedule import RandomActivationByType
from communication.message import MessageService

class RobotMissionModel(Model):
    def __init__(self, width, height, num_green_robots, num_yellow_robots, num_red_robots, num_wastes):
        self.num_green_robots = num_green_robots
        self.num_yellow_robots = num_yellow_robots
        self.num_red_robots = num_red_robots
        self.num_wastes = num_wastes
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivationByType(self)
        self.running = True
        self.current_id = 0
        self._steps = 0
        self._time = 0
        self.datacollector = DataCollector(
            model_reporters={"Wastes": lambda m: self.count_wastes()},
            agent_reporters={}
        )

        self.messages_service = MessageService()
        MessageService.get_instance().set_instant_delivery(False)

        # Create radioactivity agents
        for cell in self.grid.coord_iter():
            x, y = cell[1][0], cell[1][1]
            if x < width // 3:
                radioactivity = Radioactivity("Low", self, "z1")
            elif x < 2 * width // 3:
                radioactivity = Radioactivity("Medium", self, "z2")
            else:
                radioactivity = Radioactivity("High", self, "z3")
            self.grid.place_agent(radioactivity, (x, y))
            self.schedule.add(radioactivity)

        # Create waste disposal zone
        waste_disposal_x, waste_disposal_y = self.grid.width - 1, self.random.randrange(self.grid.height)
        waste_disposal_zone = WasteDisposalZone(self.next_id(), self)
        self.grid.place_agent(waste_disposal_zone, (waste_disposal_x, waste_disposal_y))
        self.schedule.add(waste_disposal_zone)

        # Create wastes
        for _ in range(self.num_wastes):
            x, y = self.random.randrange(self.grid.width // 3), self.random.randrange(self.grid.height)
            waste = Waste(self.next_id(), self, "Green")
            self.grid.place_agent(waste, (x, y))
            self.schedule.add(waste)

        # Create robots
        for _ in range(self.num_green_robots):
            x, y = self.random.randrange(self.grid.width // 3), self.random.randrange(self.grid.height)
            robot = GreenRobotAgent(self.next_id(), self)
            self.grid.place_agent(robot, (x, y))
            self.schedule.add(robot)

        for _ in range(self.num_yellow_robots):
            x, y = self.random.randrange(2 * self.grid.width // 3), self.random.randrange(self.grid.height)
            robot = YellowRobotAgent(self.next_id(), self)
            self.grid.place_agent(robot, (x, y))
            self.schedule.add(robot)

        for _ in range(self.num_red_robots):
            x, y = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)
            robot = RedRobotAgent(self.next_id(), self)
            self.grid.place_agent(robot, (x, y))
            self.schedule.add(robot)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.messages_service.dispatch_messages()

    def do(self, agent, action):
        if action["action"] == "move":
            self.grid.move_agent(agent, action["next_move"])
            percepts = self.get_percepts(agent)
            return percepts
        elif action["action"] == "pick_up":
            waste = self.get_waste_at(agent.pos)
            if waste:
                self.grid.remove_agent(waste)
                self.schedule.remove(waste)
                agent.carrying.append(waste)
                percepts = self.get_percepts(agent)
                return percepts
        # elif action["action"] == "transform":
        #     if len(agent.carrying) == 2 and all(waste.type == "Green" for waste in agent.carrying):
        #         new_waste = Waste(self.next_id(), self, "Yellow") 
        #         agent.carrying = [new_waste]
        #         percepts = self.get_percepts(agent)
        #         return percepts
        #     elif len(agent.carrying) == 2 and all(waste.type == "Yellow" for waste in agent.carrying):
        #         new_waste = Waste(self.next_id(), self, "Red")
        #         agent.carrying = [new_waste]
        #         percepts = self.get_percepts(agent)
        #         return percepts
        # elif action["action"] == "put_down":
        #     if agent.carrying:
        #         waste = agent.carrying.pop()
        #         self.grid.place_agent(waste, agent.pos)
        #         self.schedule.add(waste)
        #         percepts = self.get_percepts(agent)
        #         return percepts

    def is_move_possible(self, agent, destination):
        print("destination >>> ", destination, "this cell is empty >>> ", self.grid.is_cell_empty(destination))
        if not self.grid.is_cell_empty(destination):
            return False
        if isinstance(agent, GreenRobotAgent) and destination[0] >= self.grid.width // 3:
            return False
        if isinstance(agent, YellowRobotAgent) and destination[0] >= 2 * self.grid.width // 3:
            return False
        return True

    def get_waste_at(self, pos):
        agents = self.grid.get_cell_list_contents(pos)
        for agent in agents:
            if isinstance(agent, Waste):
                return agent
        return None

    def get_percepts(self, agent):
        percepts = {}
        for neighbor in self.grid.iter_neighbors(agent.pos, moore=True, include_center=True):
            percepts[neighbor.pos] = neighbor
        return percepts

    def count_wastes(self):
        waste_count = 0
        for agent in self.schedule.agents:
            if isinstance(agent, Waste):
                waste_count += 1
        return waste_count
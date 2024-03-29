from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents.agents import GreenRobotAgent, YellowRobotAgent, RedRobotAgent
from agents.object_agents import Radioactivity, WasteDisposalZone, Waste
from core.schedule import RandomActivationByType

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
            waste = Waste(self.next_id(), self, "green")
            self.grid.place_agent(waste, (x, y))
            self.schedule.add(waste)

        # Create robots
        for _ in range(self.num_green_robots):
            x, y = self.random.randrange(self.grid.width // 3), self.random.randrange(self.grid.height)
            robot = GreenRobotAgent(self.next_id(), self)
            self.grid.place_agent(robot, (x, y))
            self.schedule.add(robot)

        # for _ in range(self.num_yellow_robots):
        #     x, y = self.random.randrange(2 * self.grid.width // 3), self.random.randrange(self.grid.height)
        #     robot = YellowRobotAgent(self.next_id(), self)
        #     self.grid.place_agent(robot, (x, y))
        #     self.schedule.add(robot)

        # for _ in range(self.num_red_robots):
        #     x, y = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)
        #     robot = RedRobotAgent(self.next_id(), self)
        #     self.grid.place_agent(robot, (x, y))
        #     self.schedule.add(robot)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def do(self, agent, action):
        print(action)
        if action["action"] == "move":
            self.grid.move_agent(agent, action["next_move"])
            percepts = self.get_percepts(agent)
            return percepts
        
        elif action["action"] == "pick_up":
            if isinstance(agent, GreenRobotAgent):
                agent_pos = agent.pos
                waste_agent = None
                for cell_content in self.grid.get_cell_list_contents(agent_pos):
                    if isinstance(cell_content, Waste):
                        waste_agent = cell_content
                        break
                if waste_agent:
                    agent.wastes_carried.append(waste_agent)
                    agent.carried_color = "green"
                    self.grid.remove_agent(waste_agent)
                    self.schedule.remove(waste_agent)
                    percepts = self.get_percepts(agent)
                    return percepts
                else:
                    percepts = self.get_percepts(agent)
                    return percepts
        
        elif action["action"] == "transform":
            if isinstance(agent, GreenRobotAgent) and len(agent.wastes_carried) == 2:
                new_waste = Waste(self.next_id(), self, "yellow") # Create the new waste
                agent.wastes_carried = [] # Reset what agent carry
                agent.wastes_carried.append(new_waste) # Add the new yellow waste
                agent.carried_color = "yellow"
                percepts = self.get_percepts(agent)
                return percepts
            # TODO: Yellow transform action
        
        elif action["action"] == "bring_east":
            if isinstance(agent, GreenRobotAgent) and not agent.full_east and agent.carried_color == "yellow":
                current_pos = agent.pos
                next_pos = (current_pos[0] + 1, current_pos[1])
                if next_pos[0] < (self.grid.width // 3):
                    self.grid.move_agent(agent, next_pos)
                if next_pos[0] >= (self.grid.width // 3) - 1:
                    agent.full_east = True
                percepts = self.get_percepts(agent)
                return percepts
            # TODO: Yellow bring east action
            
        elif action["action"] == "put_down":
            if isinstance(agent, GreenRobotAgent) and agent.full_east and agent.carried_color == "yellow":
                current_pos = agent.pos
                new_waste = Waste(self.next_id(), self, "yellow")
                agent.wastes_carried = []
                agent.carried_color = "green"
                agent.full_east = False
                self.grid.place_agent(new_waste, current_pos)
                percepts = self.get_percepts(agent)
                return percepts
            # TODO: Yellow and Red put down action

    def is_move_possible(self, agent, destination):
        # TODO
        pass

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
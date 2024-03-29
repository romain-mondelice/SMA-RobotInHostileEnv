# agents.py
from mesa import Agent
from agents.object_agents import Radioactivity

class RobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.knowledge = {}
        self.waste_carried = None
        self.moore = True

    def step(self):
        percepts = self.model.get_percepts(self)
        print(percepts)
        self.update_knowledge(percepts)
        action = self.deliberate()
        percepts = self.model.do(self, action)

    def update_knowledge(self, percepts):
        self.knowledge.update(percepts)

    def deliberate(self):
        # Implement the decision-making process based on the agent's knowledge
        pass

class GreenRobotAgent(RobotAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_zone = 1

    def deliberate(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)

        if self.waste_carried is None:
            print(self.knowledge)
            # Look for green waste in the current zone
            for pos, contents in self.knowledge.items():
                print(type(contents), isinstance(contents, Radioactivity))
                if 'green_waste' in contents:
                    return {'action': 'pick_up', 'waste_type': 'green', 'pos': pos}
        elif self.waste_carried == 'green':
            # Transform green waste into yellow waste
            return {'action': 'transform', 'waste_type': 'yellow'}
        elif self.waste_carried == 'yellow':
            # Transport yellow waste to the next zone
            next_zone = self.model.get_next_zone(self.pos)
            if next_zone <= self.max_zone:
                return {'action': 'move', 'direction': 'east'}
        return {'action': 'move', 'next_move': next_move}

class YellowRobotAgent(RobotAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_zone = 2

    def deliberate(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)

        if self.waste_carried is None:
            # Look for yellow waste in the current zone
            for pos, contents in self.knowledge.items():
                if 'yellow_waste' in contents:
                    return {'action': 'pick_up', 'waste_type': 'yellow', 'pos': pos}
        elif self.waste_carried == 'yellow':
            # Transform yellow waste into red waste
            return {'action': 'transform', 'waste_type': 'red'}
        elif self.waste_carried == 'red':
            # Transport red waste to the next zone
            next_zone = self.model.get_next_zone(self.pos)
            if next_zone <= self.max_zone:
                return {'action': 'move', 'direction': 'east'}
        return {'action': 'move', 'next_move': next_move}

class RedRobotAgent(RobotAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_zone = 3

    def deliberate(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)

        if self.waste_carried is None:
            # Look for red waste in the current zone
            for pos, contents in self.knowledge.items():
                if 'red_waste' in contents:
                    return {'action': 'pick_up', 'waste_type': 'red', 'pos': pos}
        elif self.waste_carried == 'red':
            # Transport red waste to the waste disposal zone
            waste_disposal_zone = self.model.get_waste_disposal_zone()
            if self.pos == waste_disposal_zone:
                return {'action': 'put_down', 'waste_type': 'red'}
            else:
                direction = self.model.get_direction(self.pos, waste_disposal_zone)
                return {'action': 'move', 'direction': direction}
        return {'action': 'move', 'next_move': next_move}
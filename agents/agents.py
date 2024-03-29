# agents.py
from mesa import Agent
from agents.object_agents import Waste

class RobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.knowledge = {}
        self.waste_carried = None
        self.moore = True

    def step(self):
        percepts = self.model.get_percepts(self)
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
        self.wastes_carried = []
        self.carried_color = "green"
        self.full_east = False

    def deliberate(self):
        # Random move
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, include_center=False)
        next_move = self.random.choice(next_moves)

        # Check validity of the move
        height_pos_check = next_move[1] < self.model.grid.height - 1
        height_neg_check = next_move[1] > 0
        width_zone_check = next_move[0] < self.model.grid.width // 3
        width_neg_check = next_move[0] > 0
        if (not height_pos_check or not height_neg_check or not width_zone_check or not width_neg_check):
            next_move = self.pos

        if len(self.wastes_carried) < 2 and self.carried_color == "green":
            waste = self.model.get_waste_at(self.pos)
            if waste and waste.waste_type == "green":
                return {'action': 'pick_up', 'waste': waste}
        elif len(self.wastes_carried) == 2 and self.carried_color == "green":
            return {'action': 'transform'}
        elif self.carried_color == "yellow" and not self.full_east:
            return {'action': 'bring_east'}
        elif self.carried_color == "yellow" and self.full_east:
            return {'action': 'put_down'}
        else:
            return {'action': 'move', 'next_move': next_move}
        return {'action': 'move', 'next_move': next_move}

class YellowRobotAgent(RobotAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_zone = 2
        self.wastes_carried = []

    def deliberate(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        if self.waste_carried is None:
            # If not carrying waste, try to pick up yellow waste
            waste = self.model.get_waste_at(self.pos)
            if waste and waste.waste_type == "yellow":
                return {'action': 'pickup', 'waste': waste}
        else:
            # If carrying waste, try to transform or move
            if self.waste_carried.waste_type == "yellow" and len(self.wastes_carried) == 2:
                return {'action': 'transform'}
            else:
                return {'action': 'move', 'next_move': next_move}
        return {'action': 'move', 'next_move': next_move}

class RedRobotAgent(RobotAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_zone = 3

    def deliberate(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        if self.waste_carried is None:
            # If not carrying waste, try to pick up red waste
            waste = self.model.get_waste_at(self.pos)
            if waste and waste.waste_type == "red":
                return {'action': 'pickup', 'waste': waste}
        else:
            # If carrying waste, try to move to the waste disposal zone
            if self.model.is_waste_disposal_zone(next_move):
                return {'action': 'putdown'}
            else:
                return {'action': 'move', 'next_move': next_move}
        return {'action': 'move', 'next_move': next_move}
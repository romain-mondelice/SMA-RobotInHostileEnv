from mesa import Agent

class Radioactivity(Agent):
    def __init__(self, unique_id, model, zone):
        super().__init__(unique_id, model)
        self.zone = zone
        self.level = self.calculate_radioactivity_level()

    def calculate_radioactivity_level(self):
        if self.zone == "z1":
            return self.random.uniform(0, 0.33)
        elif self.zone == "z2":
            return self.random.uniform(0.33, 0.66)
        else:
            return self.random.uniform(0.66, 1)

class WasteDisposalZone(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Waste(Agent):
    def __init__(self, unique_id, model, waste_type):
        super().__init__(unique_id, model)
        self.waste_type = waste_type
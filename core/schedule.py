import random
from collections import defaultdict

from mesa.time import BaseScheduler


class RandomActivationByType(BaseScheduler):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step() method.
    """

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_type = defaultdict(dict)

    def add(self, agent):
        """
        Add an Agent object to the schedule.

        Args:
            agent: An Agent to be added to the schedule.
        """
        agent_class = type(agent)
        self.agents_by_type[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.

        Args:
            agent: An agent object.
        """
        agent_class = type(agent)
        del self.agents_by_type[agent_class][agent.unique_id]

    def step(self, by_type=True):
        """
        Executes the step of each agent type, one at a time, in random order.

        Args:
            by_type: If True, run all agents of a single type before running
                      the next one.
        """
        if by_type:
            for agent_class in self.agents_by_type:
                self.step_type(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_type(self, agent_type):
        """
        Shuffle order and run all agents of a given type.

        Args:
            agent_type: Class object of the type to run.
        """
        agent_keys = list(self.agents_by_type[agent_type].keys())
        random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_type[agent_type][agent_key].step()

    def get_type_count(self, agent_type):
        """
        Returns the current number of agents of certain type in the queue.

        Args:
            agent_type: Class object of the type to count.
        """
        return len(self.agents_by_type[agent_type].values())
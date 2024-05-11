from abc import ABC, abstractmethod
from typing import List

from logger.logger import Logger


class Agent(ABC):
    """Represents an abstract agent interacting with the world."""

    def __init__(self, trials: int) -> None:
        Logger.info(f"This simulation is using a {self.__class__}")
        # Init stats
        self.action_hist_t = [[] for _ in range(trials)]
        self.observation_hist_t = [[] for _ in range(trials)]
        # Aliases
        self.action_hist: List[float]
        self.observation_hist: List[float]

    @abstractmethod
    def start_trial(self, trial: int) -> None:
        """Prepare the agent for an upcoming trial."""
        # Change alliases for stats
        self.action_hist = self.action_hist_t[trial]
        self.observation_hist = self.observation_hist_t[trial]

    @abstractmethod
    def save_stats(self):
        """Saves the stats needed by the agent."""

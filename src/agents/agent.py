from abc import ABC, abstractmethod
from typing import List

from matplotlib import pyplot as plt

from logger.logger import Logger


class Agent(ABC):
    """Represents an abstract agent interacting with the world."""

    def __init__(self, trials: int, T: int) -> None:
        Logger.info(f"This simulation is using a {self.__class__}")
        self.T = T
        self.n_trials = trials
        # Init stats
        self.action_hist_t: List[List[float]] = [[] for _ in range(trials)]
        self.observation_hist_t: List[List[float]] = [
            [] for _ in range(trials)
        ]
        self.optimal_observation_t: List[List[float]] = [
            [] for _ in range(trials)
        ]
        # Aliases
        self.action_hist: List[float]
        self.observation_hist: List[float]
        self.optimal_observation: List[float]

    def update_regret(self, best_price_idx: int, feedback: int) -> None:
        """Update the regret of this agent."""
        self.optimal_observation.append(feedback)

    @abstractmethod
    def start_trial(self, trial: int) -> None:
        """Prepare the agent for an upcoming trial."""
        # Change alliases for stats
        self.action_hist = self.action_hist_t[trial]
        self.observation_hist = self.observation_hist_t[trial]
        self.optimal_observation = self.optimal_observation_t[trial]

    @abstractmethod
    def save_stats(self):
        """Saves the stats needed by the agent."""

from abc import ABC, abstractmethod
import math
from typing import Any, List

from matplotlib import pyplot as plt
import numpy as np

from logger.jpegger import JPEGger
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

    @abstractmethod
    def start_trial(self, trial: int) -> None:
        """Prepare the agent for an upcoming trial."""
        # Change alliases for stats
        self.action_hist = self.action_hist_t[trial]
        self.observation_hist = self.observation_hist_t[trial]
        self.optimal_observation = self.optimal_observation_t[trial]

    def update_regret(self, best_price_idx: int, feedback: int) -> None:
        """Update the regret of this agent."""
        self.optimal_observation.append(feedback)

    @abstractmethod
    def save_stats(self):
        """Saves the stats needed by the agent."""
        rew = np.asarray(self.observation_hist_t)
        best_rew = np.asarray(self.optimal_observation_t)
        cum_regret = np.cumsum(best_rew - rew, axis=1)

        cum_regret_mean = np.mean(cum_regret, axis=0)
        cum_regret_std = np.std(cum_regret, axis=0)

        fig = plt.figure()
        plt.plot(np.arange(self.T), cum_regret_mean, label='Average Regret')
        plt.fill_between(
            np.arange(self.T),
            cum_regret_mean - cum_regret_std / math.sqrt(self.n_trials),
            cum_regret_mean + cum_regret_std / math.sqrt(self.n_trials),
            alpha=0.3,
            label='Uncertainty',
        )
        plt.title('Cumulative regret')
        plt.xlabel('Days')
        plt.legend()
        JPEGger.save_jpg(fig, "pricing_agent_regret.jpg")

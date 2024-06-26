from abc import abstractmethod
import math

from matplotlib import pyplot as plt
import numpy as np

from logger.jpegger import JPEGger
from src.agents.agent import Agent


class PricingAgent(Agent):
    """Represents an abstract agent that interacts with
    the pricing problem."""

    @abstractmethod
    def get_price(self, day: int) -> float:
        """Return the price chosen by this agent."""

    @abstractmethod
    def update(self, reward: float) -> None:
        """Update the internal status of this agent after it acted."""

    def save_stats(self):
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
        JPEGger.save_jpg(fig, f"pricing_agent_regret.jpg")

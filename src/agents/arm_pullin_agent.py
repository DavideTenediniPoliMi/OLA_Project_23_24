from typing import List

import numpy as np
from matplotlib import pyplot as plt

from logger.jpegger import JPEGger
from src.agents.agent import Agent


class ArmPullingAgent(Agent):
    def __init__(self, trials: int, discretization: int) -> None:
        super().__init__(trials)
        self.arms = np.linspace(0, 1, discretization)
        self.N_pulls_t = [[0] * len(self.arms) for _ in range(trials)]
        # Alias
        self.N_pulls: List[int]

    def start_trial(self, trial: int) -> None:
        super().start_trial(trial)
        self.N_pulls = self.N_pulls_t[trial]

    def save_stats(self):
        super().save_stats()
        fig = plt.figure()
        plt.barh(
            np.arange(len(self.arms)),
            np.mean(self.N_pulls_t, axis=0),
        )
        plt.ylabel('actions')
        plt.xlabel('numer of pulls')
        plt.title('Avg Number of pulls for each action')
        JPEGger.save_jpg(fig, "pricing_agent.jpg")

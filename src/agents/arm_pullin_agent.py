from collections import Counter
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from logger.jpegger import JPEGger
from src.agents.agent import Agent


class ArmPullingAgent(Agent):
    def __init__(self, trials: int, T: int, discretization: int) -> None:
        super().__init__(trials, T)
        self.arms = np.linspace(0, 1, discretization)
        self.N_pulls_t: List[List[int]] = [
            [0] * len(self.arms) for _ in range(trials)
        ]
        self.optimal_arm_t: List[List[float]] = [[] for _ in range(trials)]
        # Alias
        self.N_pulls: List[int]
        self.optimal_arm: List[int]

    def start_trial(self, trial: int) -> None:
        super().start_trial(trial)
        self.N_pulls = self.N_pulls_t[trial]
        self.optimal_arm = self.optimal_arm_t[trial]

    def update_regret(self, best_price_idx: int, feedback: int) -> None:
        super().update_regret(best_price_idx, feedback)
        self.optimal_arm.append(best_price_idx)

    def save_stats(self):
        most_common_best_arm = Counter(
            np.asarray(self.optimal_arm_t).ravel()
        ).most_common(1)[0][0]

        super().save_stats()
        fig = plt.figure()
        plt.barh(
            np.arange(len(self.arms)),
            np.mean(self.N_pulls_t, axis=0),
        )
        plt.axhline(most_common_best_arm, color='red', label='Best price')
        plt.ylabel('actions')
        plt.xlabel('numer of pulls')
        plt.title('Avg Number of pulls for each action')
        plt.legend()
        JPEGger.save_jpg(fig, "pricing_agent_pulls.jpg")

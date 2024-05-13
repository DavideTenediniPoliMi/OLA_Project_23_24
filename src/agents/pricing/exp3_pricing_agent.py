import math

import numpy as np

from src.agents.arm_pullin_agent import ArmPullingAgent
from src.agents.pricing.pricing_agent import PricingAgent


class EXP3PricingAgent(ArmPullingAgent, PricingAgent):
    def __init__(
        self,
        trials: int,
        T: int,
        discretization: int,
        cost: float,
    ) -> None:
        super().__init__(trials, T, discretization)
        # Parameters
        self.learning_rate = math.sqrt(
            math.log(discretization) / (discretization * T)
        )
        self.max_price = 1 - cost
        self.weights: np.ndarray
        self.p_dist: np.ndarray

    def get_price(self, day: int) -> float:
        self.p_dist = self.weights / self.weights.sum()
        best_price_idx = np.random.choice(range(len(self.arms)), p=self.p_dist)

        # Update stats
        self.action_hist.append(best_price_idx)
        self.N_pulls[best_price_idx] += 1

        return self.arms[best_price_idx]

    def update(self, reward: float) -> None:
        # Update the price weights
        last_action = self.action_hist[-1]
        loss = self.max_price - reward
        norm_loss = loss / self.p_dist[last_action]
        self.weights[last_action] *= math.exp(-self.learning_rate * norm_loss)

        # Update stats
        self.observation_hist.append(reward)

    def start_trial(self, trial: int) -> None:
        super().start_trial(trial)
        self.weights = np.ones(len(self.arms))

    def save_stats(self):
        return super().save_stats()

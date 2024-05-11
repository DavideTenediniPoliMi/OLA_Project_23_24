import math

import numpy as np

from src.agents.arm_pullin_agent import ArmPullingAgent
from src.agents.pricing.pricing_agent import PricingAgent


class UCB1PricingAgent(ArmPullingAgent, PricingAgent):
    def __init__(self, trials: int, T: int, discretization: int) -> None:
        super().__init__(trials, discretization)
        # Time Horizon
        self.T = T
        # Means for the UCBs
        self.avg_rewards: np.ndarray
        # Another alias for ArmPullingAgent.N_pulls, except it's an
        # np.ndarray instead of a List[int]
        self.N_pulls_np: np.ndarray

    def bounds(self) -> np.ndarray:
        return np.sqrt(2 * math.log(self.T) / self.N_pulls_np)

    def get_price(self, day: int) -> float:
        # Try all the prices at the beginning
        if day < len(self.arms):
            best_price_idx = day
        else:  # Then choose the most promising price
            ucbs = self.avg_rewards + self.bounds()
            best_price_idx = np.argmax(ucbs)

        # Update stats
        self.action_hist.append(best_price_idx)
        self.N_pulls[best_price_idx] += 1
        self.N_pulls_np[best_price_idx] += 1

        return self.arms[best_price_idx]

    def update(self, reward: float) -> None:
        # Update the running mean
        last_idx = self.action_hist[-1]
        self.avg_rewards[last_idx] += (
            reward - self.avg_rewards[last_idx]
        ) / self.N_pulls_np[last_idx]

        # Update stats
        self.observation_hist.append(reward)

    def start_trial(self, trial: int) -> None:
        super().start_trial(trial)
        self.avg_rewards = np.zeros(len(self.arms))
        self.N_pulls_np = np.asarray(self.N_pulls)

    def save_stats(self):
        return super().save_stats()

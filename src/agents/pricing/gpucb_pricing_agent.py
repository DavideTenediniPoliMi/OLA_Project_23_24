import math

import numpy as np

from src.agents.arm_pullin_agent import ArmPullingAgent
from src.agents.pricing.pricing_agent import PricingAgent
from src.utils.rbf_gaussian_process import RBFGaussianProcess


class GPUCBPricingAgent(ArmPullingAgent, PricingAgent):
    def __init__(self, trials, T: int, discretization: int) -> None:
        super().__init__(trials, discretization)
        # Time Horizon
        self.T = T

    def gamma(self, t) -> float:
        return math.log(t + 1) ** 2

    def beta(self, t) -> float:
        return 1 + 0.5 * np.sqrt(2 * (self.gamma(t) + 1 + math.log(self.T)))

    def get_price(self, day: int) -> float:
        mu, sigma = self.gp.predict(self.arms)

        # Compute the UCBs for the prices and choose the best one
        ucbs = mu + self.beta(day) * sigma
        best_price_idx = np.argmax(ucbs)
        best_price = self.arms[best_price_idx]

        # Update stats
        self.action_hist.append(best_price_idx)
        self.N_pulls[best_price_idx] += 1

        return best_price

    def update(self, reward: float) -> None:
        # Update the Gaussian Process
        self.gp = self.gp.fit(self.arms[self.action_hist[-1]], reward)

        # Update stats
        self.observation_hist.append(reward)

    def start_trial(self, trial) -> None:
        super().start_trial(trial)
        self.gp = RBFGaussianProcess().fit()

    def save_stats(self):
        super().save_stats()

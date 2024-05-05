import math

import numpy as np

from src.agents.pricing.pricing_agent import PricingAgent
from src.utils.rbf_gaussian_process import RBFGaussianProcess


class GPUCBPricingAgent(PricingAgent):
    def __init__(self, T, discretization) -> None:
        # Time Horizon
        self.T = T
        # Discretized set of arms
        self.prices = np.linspace(0, 1, discretization)
        self.gp = RBFGaussianProcess().fit()
        # Init stats
        self.price_hist = []
        self.reward_hist = []
        self.N_pulls = [0] * discretization

    def gamma(self, t):
        return math.log(t + 1) ** 2

    def beta(self, t):
        return 1 + 0.5 * np.sqrt(2 * (self.gamma(t) + 1 + math.log(self.T)))

    def get_price(self, day: int) -> float:
        # Fit the GP with the last data point and predict the next one
        if day != 0:
            self.gp = self.gp.fit(self.price_hist[-1], self.reward_hist[-1])
        mu, sigma = self.gp.predict(self.prices)

        # Compute the UCBs for the prices and chose the best one
        ucbs = mu + self.beta(day) * sigma
        best_price_idx = np.argmax(ucbs)
        best_price = self.prices[best_price_idx]

        # Update stats
        self.price_hist.append(best_price)
        self.N_pulls[best_price_idx] += 1

        return best_price

    def update(self, reward) -> None:
        self.reward_hist.append(reward)

    def save_stats(self):
        return super().save_stats()

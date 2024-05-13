from abc import ABC, abstractmethod

from matplotlib import pyplot as plt
import numpy as np

from logger.logger import Logger


class User(ABC):
    @abstractmethod
    def _get_prob(self, p: float | np.ndarray) -> float | np.ndarray:
        """Return the probability that the user buys the product at the
        given price."""

    def does_buy(self, prices: np.ndarray) -> np.ndarray:
        """Return whether the user buys the product given the price."""
        return np.random.binomial(1, self._get_prob(prices))

    def draw_prob(self, discretization) -> None:
        prices = np.linspace(0, 1, discretization)
        plt.plot(prices, self._get_prob(prices))
        plt.xlabel('Prices')
        plt.ylabel('Purchase Probabilities')

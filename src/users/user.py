from abc import ABC, abstractmethod

import numpy as np


class User(ABC):
    @abstractmethod
    def _get_prob(self, p: float) -> float:
        """Return the probability that the user buys the product at the
        given price."""

    def does_buy(self, price: float) -> bool:
        """Return whether the user buys the product given the price."""
        return np.random.binomial(1, self._get_prob(price))

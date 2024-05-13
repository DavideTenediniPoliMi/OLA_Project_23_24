import numpy as np
import scipy.stats as stats

from src.users.user import User


class ProbitUser(User):
    def __init__(self, alpha: float, beta: float) -> None:
        assert alpha != None and beta != None, "Invalid Parameters!"
        self.alpha = alpha
        self.beta = beta

    def _get_prob(self, p: float | np.ndarray) -> float | np.ndarray:
        return stats.norm.cdf(self.alpha + self.beta * p)

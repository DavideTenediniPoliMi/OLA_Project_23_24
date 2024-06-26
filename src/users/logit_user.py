import numpy as np

from src.users.user import User


class LogitUser(User):
    def __init__(self, alpha: float, beta: float) -> None:
        assert (
            alpha != None and beta != None and beta < 0
        ), "Invalid Parameters!"
        self.alpha = alpha
        self.beta = beta

    def _get_prob(self, p: float | np.ndarray) -> float | np.ndarray:
        return 1 / (1 + np.exp(-(self.alpha + self.beta * p)))

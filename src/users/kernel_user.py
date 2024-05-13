import numpy as np

from src.users.user import User


class KernelUser(User):
    def __init__(self, alpha: float, beta: float, gamma: float) -> None:
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def _get_prob(self, p: float | np.ndarray) -> float | np.ndarray:
        return (
            np.abs(
                np.sin(2 * np.pi * p) * np.exp(-self.alpha * p) + self.beta * p
            )
            + self.gamma
        )

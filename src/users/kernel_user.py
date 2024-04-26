from math import exp, pi, sin

from src.users.user import User


class KernelUser(User):
    def __init__(self, alpha: float, beta: float, gamma: float) -> None:
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def _get_prob(self, p: float) -> float:
        return (
            abs(sin(2 * pi * p) * exp(-self.alpha * p) + self.beta * p)
            + self.gamma
        )

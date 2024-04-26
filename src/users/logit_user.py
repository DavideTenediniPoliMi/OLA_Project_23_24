from math import exp

from src.users.user import User


class LogitUser(User):
    def __init__(self, alpha: float, beta: float) -> None:
        assert alpha != None and beta != None, "Invalid Parameters!"
        self.alpha = alpha
        self.beta = beta

    def _get_prob(self, p: float) -> float:
        return 1 / (1 + exp(-(self.alpha + self.beta * p)))

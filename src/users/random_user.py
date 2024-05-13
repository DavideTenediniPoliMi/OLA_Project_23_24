from random import random

from colorama import init
import numpy as np

from src.users.user import User


class RandomUser(User):
    def _get_prob(self, p: float | np.ndarray) -> float | np.ndarray:
        if isinstance(p, float):
            return 0.5
        else:
            return np.full_like(p, 0.5)

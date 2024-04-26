from random import random

from colorama import init

from src.users.user import User


class RandomUser(User):
    def _get_prob(self, p: float) -> float:
        return 0.5

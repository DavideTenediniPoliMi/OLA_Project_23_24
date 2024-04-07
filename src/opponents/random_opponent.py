from random import random
from src.opponents.opponent import Opponent


class RandomOpponent(Opponent):
    def get_bid(self) -> float:
        return random() * 100

from random import random

from src.opponents.opponent import Opponent


class RandomOpponent(Opponent):
    def get_bid(self, day: int, auction_num: int) -> float:
        return random() * 100

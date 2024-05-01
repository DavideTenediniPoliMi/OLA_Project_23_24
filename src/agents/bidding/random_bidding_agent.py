from random import random

from src.agents.bidding.bidding_agent import BiddingAgent


class RandomBiddingAgent(BiddingAgent):
    """Represents a bidding agent that chooses its bid randomly."""

    def get_bid(self, day: int, auction_num: int) -> float:
        return random()

    def save_stats(self):
        pass

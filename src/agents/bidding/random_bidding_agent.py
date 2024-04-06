from random import random

from src.agents.bidding.bidding_agent import BiddingAgent


class RandomBiddingAgent(BiddingAgent):
    """Represents a bidding agent that chooses its bid randomly."""

    def get_bid(self) -> float:
        return random() * 100

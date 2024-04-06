from random import random
from src.agents.bidding.bidding_agent import BiddingAgent


class RandomBiddingAgent(BiddingAgent):
    def get_bid(self) -> float:
        return random() * 100

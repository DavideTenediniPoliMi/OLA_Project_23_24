from abc import abstractmethod

from src.agents.agent import Agent


class BiddingAgent(Agent):
    """Represents an abstract agent interacting with
    the bidding problem."""

    @abstractmethod
    def get_bid(self, day: int, auction_num: int) -> float:
        """Return the bid chosen by this agent."""

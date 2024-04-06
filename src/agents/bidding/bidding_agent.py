from abc import abstractmethod

from src.agents.agent import Agent


class BiddingAgent(Agent):
    """Represents an abstract agent interacting with
    the bidding problem."""

    @abstractmethod
    def get_bid(self) -> float:
        """Return the bid chosen by this agent."""

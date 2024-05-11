from abc import abstractmethod

from src.agents.agent import Agent


class BiddingAgent(Agent):
    """Represents an abstract agent interacting with
    the bidding problem."""

    def __init__(self, budget: float = 0) -> None:
        super().__init__()
        self.budget = budget

    def incur_cost(self, cost: float) -> None:
        self.budget -= cost
        assert self.budget >= 0, "Budget under zero!"

    @abstractmethod
    def get_bid(self, day: int, auction_num: int) -> float:
        """Return the bid chosen by this agent."""

    @abstractmethod
    def update(self, observation) -> None:
        """Update the internal status of this agent after it acted."""

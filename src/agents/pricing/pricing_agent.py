from abc import abstractmethod

from src.agents.agent import Agent


class PricingAgent(Agent):
    """Represents an abstract agent that interacts with
    the pricing problem."""

    @abstractmethod
    def get_price(self, day: int) -> float:
        """Return the price chosen by this agent."""

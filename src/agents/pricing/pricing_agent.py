from abc import abstractmethod

from src.agents.agent import Agent


class PricingAgent(Agent):

    @abstractmethod
    def get_price(self) -> float:
        """Return the price chosen by this agent."""

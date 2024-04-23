from random import random

from src.agents.pricing.pricing_agent import PricingAgent


class RandomPricingAgent(PricingAgent):
    """Represents a pricing agent that chooses the price randomly."""

    def get_price(self, day: int) -> float:
        return random() * 100

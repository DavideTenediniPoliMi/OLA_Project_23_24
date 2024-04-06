from random import random
from src.agents.pricing.pricing_agent import PricingAgent


class RandomPricingAgent(PricingAgent):
    def get_price(self) -> float:
        return random() * 100

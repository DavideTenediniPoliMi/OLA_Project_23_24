from typing import Any, Dict, List
from src.agents.pricing.pricing_agent import PricingAgent
from src.agents.pricing.random_pricing_agent import RandomPricingAgent


class PricingAgentFactory:
    @staticmethod
    def build_agent(agent: Dict[str, Any]) -> List[PricingAgent]:
        match agent["type"]:
            case "random":
                return [RandomPricingAgent() for _ in range(agent["count"])]
            case _:
                raise NotImplementedError("Agent type not supported!")

from typing import Any, Dict, List

from src.agents.pricing.gpucb_pricing_agent import GPUCBPricingAgent
from src.agents.pricing.pricing_agent import PricingAgent
from src.agents.pricing.random_pricing_agent import RandomPricingAgent


class PricingAgentFactory:
    @staticmethod
    def build_agent(agent: Dict[str, Any]) -> PricingAgent:
        match agent["type"]:
            case "random":
                return RandomPricingAgent()
            case "gpucb":
                return GPUCBPricingAgent(agent["T"], agent["discretization"])
            case _:
                raise NotImplementedError("Agent type not supported!")

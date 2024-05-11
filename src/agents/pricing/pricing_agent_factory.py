from typing import Any, Dict, List

from src.agents.pricing.exp3_pricing_agent import EXP3PricingAgent
from src.agents.pricing.gpucb_pricing_agent import GPUCBPricingAgent
from src.agents.pricing.pricing_agent import PricingAgent
from src.agents.pricing.random_pricing_agent import RandomPricingAgent
from src.agents.pricing.ucb1_pricing_agent import UCB1PricingAgent


class PricingAgentFactory:
    @staticmethod
    def build_agent(agent: Dict[str, Any]) -> PricingAgent:
        match agent["type"]:
            case "random":
                return RandomPricingAgent()
            case "gpucb":
                return GPUCBPricingAgent(
                    agent["trials"], agent["T"], agent["discretization"]
                )
            case "ucb1":
                return UCB1PricingAgent(
                    agent["trials"], agent["T"], agent["discretization"]
                )
            case "exp3":
                return EXP3PricingAgent(
                    agent["trials"],
                    agent["T"],
                    agent["discretization"],
                    agent["cost"],
                )
            case _:
                raise NotImplementedError("Agent type not supported!")

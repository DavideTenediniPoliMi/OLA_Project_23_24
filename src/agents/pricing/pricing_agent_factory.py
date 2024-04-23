from src.agents.pricing.random_pricing_agent import RandomPricingAgent


class PricingAgentFactory:
    @staticmethod
    def build_agent(agent):
        match agent["type"]:
            case "random":
                return [RandomPricingAgent() for _ in range(agent["count"])]
            case _:
                raise NotImplementedError("Agent not supported!")

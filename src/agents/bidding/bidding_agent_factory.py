from typing import Any, Dict, List
from src.agents.bidding.bidding_agent import BiddingAgent
from src.agents.bidding.random_bidding_agent import RandomBiddingAgent


class BiddingAgentFactory:
    @staticmethod
    def build_agent(agent: Dict[str, Any]) -> List[BiddingAgent]:
        match agent["type"]:
            case "random":
                return [
                    RandomBiddingAgent(agent["budget"])
                    for _ in range(agent["count"])
                ]
            case _:
                raise NotImplementedError("Agent type not supported!")

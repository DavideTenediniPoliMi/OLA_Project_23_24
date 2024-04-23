from src.agents.bidding.random_bidding_agent import RandomBiddingAgent


class BiddingAgentFactory:
    @staticmethod
    def build_agent(agent):
        match agent["type"]:
            case "random":
                return [RandomBiddingAgent() for _ in range(agent["count"])]
            case _:
                raise NotImplementedError("Agent not supported!")

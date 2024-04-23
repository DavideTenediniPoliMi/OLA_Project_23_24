import sys
from typing import List

import numpy as np
from rich.progress import track

from config.config import load_config
from logger.logger import Logger
from src.agents.bidding.bidding_agent import BiddingAgent
from src.agents.bidding.bidding_agent_factory import BiddingAgentFactory
from src.agents.pricing.pricing_agent import PricingAgent
from src.agents.pricing.pricing_agent_factory import PricingAgentFactory
from src.auctions.auction_factory import AuctionFactory


class Simulation:
    def __init__(self, config) -> None:
        assert config["type"] in {
            "pricing",
            "bidding",
            "both",
        }, "Simulation type not supported!"

        self.config = config
        self.pricing_agents: List[PricingAgent] = []
        self.bidding_agents: List[BiddingAgent] = []

        self.init_agents()

        self.bids = np.empty(
            (
                len(self.bidding_agents),
                config["sim_length"],
                config["n_users"],
            ),
            dtype=float,
        )
        self.prices = np.empty(
            (
                len(self.pricing_agents),
                config["sim_length"],
            ),
            dtype=float,
        )

    def init_agents(self):
        if self.config["type"] != "pricing":
            for agent in self.config["auction"]["agents"]:
                self.bidding_agents.extend(
                    BiddingAgentFactory.build_agent(agent)
                )
        if self.config["type"] != "bidding":
            for agent in self.config["auction"]["agents"]:
                self.pricing_agents.extend(
                    PricingAgentFactory.build_agent(agent)
                )

    def run(self):
        for day_num in track(
            range(config["sim_length"]), description="Simulating..."
        ):
            if config["type"] != "bidding":
                self.prices[:, day_num] = [
                    agent.get_price(day_num) for agent in self.pricing_agents
                ]

            for auction_num in range(config["n_users"]):
                won = True
                CTR = 1
                if config["type"] != "pricing":
                    auction = AuctionFactory.build_auction(
                        config["auction"], day_num, auction_num
                    )
                    ids = [auction.join(CTR) for agent in self.bidding_agents]
                    bids = [
                        agent.get_bid(day_num, auction_num)
                        for agent in self.bidding_agents
                    ]
                    self.bids[:, day_num, auction_num] = bids
                    for id, bid in zip(ids, bids):
                        auction.place_bid(id, bid)
                    results = [auction.did_win(id) for id in ids]

                if config["type"] != "bidding":
                    # TODO implement client
                    pass


if __name__ == "__main__":
    config = load_config()
    Logger.init(config["log_path"])

    # Load command line requirement specific simulation
    # If no arguments were passed just run with the defaults
    args = sys.argv[1:]
    if len(args) == 0:
        config = config["defaults"]
    else:
        assert (
            args[0] in config and args[0] != "log_path"
        ), "Argument not supported!"
        config = config[args[0]]
    sim = Simulation(config)
    sim.run()

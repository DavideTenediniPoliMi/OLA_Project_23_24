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
from src.users.user_factory import UserFactory


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
        self.user_factory = UserFactory(config["users"])
        self.init_agents()

        # Prep Stats
        self.prices = np.empty(
            (
                len(self.pricing_agents),
                config["sim_length"],
            ),
            dtype=float,
        )
        self.bids = np.empty(
            (
                len(self.bidding_agents),
                config["sim_length"],
                self.user_factory.n_users,
            ),
            dtype=float,
        )
        self.budgets = np.empty(
            (
                len(self.bidding_agents),
                config["sim_length"] + 1,
                self.user_factory.n_users,
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

        if self.config["type"] == "both":
            assert len(self.bidding_agents) == len(
                self.pricing_agents
            ), "Number of Pricing and Bidding agents don't match"

    def run(self):
        for day_num in track(
            range(config["sim_length"]), description="Simulating..."
        ):
            if config["type"] != "bidding":
                self.prices[:, day_num] = [
                    agent.get_price(day_num) for agent in self.pricing_agents
                ]

            users = self.user_factory.build_users()
            for auction_num, user in enumerate(users):
                CTR = 1
                won = [True] * len(self.bidding_agents)
                if config["type"] != "pricing":
                    self.budgets[:, day_num, auction_num] = [
                        agent.budget for agent in self.bidding_agents
                    ]

                    auction = AuctionFactory.build_auction(
                        config["auction"], day_num, auction_num
                    )
                    # TODO add agent ctr custom
                    ids = [auction.join(CTR) for agent in self.bidding_agents]
                    bids = [
                        agent.get_bid(day_num, auction_num)
                        for agent in self.bidding_agents
                    ]
                    self.bids[:, day_num, auction_num] = bids
                    for id, bid in zip(ids, bids):
                        auction.place_bid(id, bid)
                    results = [auction.did_win(id) for id in ids]
                    won = [res[0] for res in results]

                    for i, w in enumerate(won):
                        if w:
                            self.bidding_agents[i].incur_cost(results[i][1])

                if config["type"] != "bidding":
                    for i, w in enumerate(won):
                        if user.does_buy(self.prices[i, day_num]):
                            pass  # TODO add revenue stats & update

        if config["type"] != "pricing":
            self.budgets[:, -1] = [
                agent.budget for agent in self.bidding_agents
            ]


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

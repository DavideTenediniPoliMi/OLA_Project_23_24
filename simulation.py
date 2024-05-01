from array import array
import random
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
        self.type = config["type"]
        assert self.type in {
            "pricing",
            "bidding",
            "both",
        }, "Simulation type not supported!"

        # Flags to recognize if the pricing and bidding tasks are active
        self.PRICING = self.type != "bidding"
        self.BIDDING = self.type != "pricing"

        # Congfigs
        self.length = config["sim_length"]
        self.cost = config["pricing"]["cost"]
        self.num_prods = config["pricing"]["num_prods"]
        # Randomness
        random.seed(config["seed"])
        np.random.seed(config["seed"])
        # Agents
        self.pricing_agents: List[PricingAgent] = []
        self.bidding_agents: List[BiddingAgent] = []
        # Statistics
        self.prices: np.ndarray  # [agent, day]
        self.profits: np.ndarray  # [agent, day]
        self.bids: np.ndarray  # [agent, day, auction]
        # Budgets at the beginning of each auction of each day.
        # The second dimension is num_days + 1 so that we can save the
        # remaining budget after the last auction of the last day.
        self.budgets: np.ndarray  # [agent, day, auction]
        self.wins: np.ndarray  # [agent, day, auction]
        self.costs: np.ndarray  # [agent, day, auction]

        # Init simulation resources
        self.user_factory = UserFactory(config["users"])
        self.auction_factory = AuctionFactory(config["auction"])
        self.init_agents(
            config["pricing"]["agents"], config["auction"]["agents"]
        )
        self.init_stats()

    def init_agents(self, pricing_agents, bidding_agents):
        if self.PRICING:
            for agent in pricing_agents:
                self.pricing_agents.extend(
                    PricingAgentFactory.build_agent(agent)
                )

        if self.BIDDING:
            for agent in bidding_agents:
                self.bidding_agents.extend(
                    BiddingAgentFactory.build_agent(agent)
                )

        if self.type == "both":
            assert len(self.bidding_agents) == len(
                self.pricing_agents
            ), "Number of Pricing and Bidding agents doesn't match"

    def init_stats(self):
        if self.PRICING:
            self.prices = np.empty(
                (len(self.pricing_agents), self.length),
                dtype=float,
            )
            self.profits = np.empty(
                (len(self.pricing_agents), self.length),
                dtype=float,
            )

        if self.BIDDING:
            self.bids = np.empty(
                (
                    len(self.bidding_agents),
                    self.length,
                    self.user_factory.n_users,
                ),
                dtype=float,
            )
            self.budgets = np.empty(
                (
                    len(self.bidding_agents),
                    self.length + 1,
                    self.user_factory.n_users,
                ),
                dtype=float,
            )
            self.wins = np.empty(
                (
                    len(self.bidding_agents),
                    self.length,
                    self.user_factory.n_users,
                ),
                dtype=bool,
            )
            self.costs = np.empty(
                (
                    len(self.bidding_agents),
                    self.length,
                    self.user_factory.n_users,
                ),
                dtype=float,
            )

            # Save Starting Budgets
            starting_budget = np.array(
                [agent.budget for agent in self.bidding_agents]
            ).reshape(-1, 1)
            self.budgets[:, -1] = np.repeat(
                starting_budget, self.budgets.shape[2]
            )

    def run(self):
        """
        Run the simulation based on the parameters in the config file.

        If the simulation type is "pricing" then the simulation will
        take place as follows:
        FOREACH day
            make all the pricing agents choose a price for the day
            FOREACH user
                make user decide whether to buy based on the price

        If the simulation type is "bidding" then the simulation will
        take place as follows:
        FOREACH user of each day
            make all the bidding agents place a bid for the auction
            declare the winner(s) of the auction

        If the simulation type is "both" then the simulation will
        take place as follows:
        FOREACH day
            make all the pricing agents choose a price for the day
            FOREACH user
                make all the bidding agents place a bid for the auction
                show the ad(s) of the winner(s) to the user
                make user decide whether to buy based on the price
        """
        for day_num in track(range(self.length), description="Simulating..."):
            self.run_day(day_num)

    def run_day(self, day_num):
        if self.PRICING:
            # Make agents chhoose the prices
            prices = [
                agent.get_price(day_num) for agent in self.pricing_agents
            ]

        users = self.user_factory.build_users()
        for auction_num, user in enumerate(users):
            won = [True] * len(self.bidding_agents)
            if self.BIDDING:
                won = self.run_auction(day_num, auction_num, user)

            if self.PRICING:
                # Make user buy the products
                bought = [False] * len(self.pricing_agents)
                for i, w in enumerate(won):
                    if not w:
                        continue
                    if user.does_buy(prices[i]):
                        bought[i] = True
                        pass  # TODO update

        # Save Statistics
        self.prices[:, day_num] = prices
        self.profits[:, day_num] = np.where(
            bought, np.array(prices) - self.cost, 0
        )

    def run_auction(self, day_num, auction_num, user) -> List[bool]:
        CTR = 1
        # Init auction
        auction = self.auction_factory.build_auction(day_num, auction_num)
        # Add agents to auction
        # TODO add agent ctr custom
        ids = [auction.join(CTR) for agent in self.bidding_agents]
        # Make agents place a bid
        bids = [
            agent.get_bid(day_num, auction_num)
            for agent in self.bidding_agents
        ]
        for id, bid in zip(ids, bids):
            auction.place_bid(id, bid)
        # Save results
        results = np.array([list(auction.did_win(id)) for id in ids])
        won = results[:, 0]
        # Collect payments
        for i, w in enumerate(won):
            if w:
                self.bidding_agents[i].incur_cost(results[i, 1])

        # Save Statistics
        self.wins[:, day_num, auction_num] = won
        self.costs[:, day_num, auction_num] = [
            c if c != None else 0 for c in results[:, 1]
        ]
        self.bids[:, day_num, auction_num] = bids
        self.budgets[:, day_num, auction_num] = [
            agent.budget for agent in self.bidding_agents
        ]

        return won

    def save_sim_stats(self) -> None:
        np.set_printoptions(threshold=np.inf)
        if self.PRICING:
            Logger.info("Pricing stats:")
            Logger.info("Prices:")
            Logger.info(self.prices)
            Logger.info("Profits:")
            Logger.info(self.profits)

            for agent in self.pricing_agents:
                agent.save_stats()

        if self.BIDDING:
            Logger.info("Bidding stats:")
            Logger.info("Bids:")
            Logger.info(self.bids)
            Logger.info("Budgets:")
            Logger.info(self.budgets)
            Logger.info("Wins:")
            Logger.info(self.wins)
            Logger.info("Costs:")
            Logger.info(self.costs)

            for agent in self.bidding_agents:
                agent.save_stats()


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
    Logger.info(f"Rand Seed : {config['seed']}")
    sim = Simulation(config)
    sim.run()
    sim.save_sim_stats()

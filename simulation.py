import random
import sys
from typing import List

import numpy as np
from rich.progress import track

from config.config import load_config
from logger.jpegger import JPEGger
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

        # Flags to recognize if the pricing and bidding tasks are active
        self.PRICING = config["type"] != "bidding"
        self.BIDDING = config["type"] != "pricing"

        # Congfigs
        self.trials = config["trials"]
        self.length = config["sim_length"]
        self.cost = config["pricing"]["cost"]
        self.num_prods = config["pricing"]["num_prods"]
        self.seed = config["seed"]
        self.VERBOSE = config["verbose"]
        self.SILENT = config["silent"]
        # Randomness
        random.seed(self.seed)
        np.random.seed(self.seed)
        # Agents
        self.pricing_agent: PricingAgent
        self.bidding_agents: List[BiddingAgent] = []
        # Statistics
        self.prices: np.ndarray  # [agent, day]
        self.profits: np.ndarray  # [agent, day]
        self.bids: np.ndarray  # [agent, day, auction]
        # Budgets after each auction of each day.
        # The second dimension is num_days + 1. The first day is just to
        # save the initial budgets of the agents.
        self.budgets: np.ndarray  # [agent, day, auction]
        self.wins: np.ndarray  # [agent, day, auction]
        self.costs: np.ndarray  # [agent, day, auction]

        # Init simulation resources
        self.user_factory = UserFactory(config["users"])
        self.auction_factory = AuctionFactory(config["auction"])

        # Inject useful parameters
        config["pricing"]["agent"]["T"] = self.length
        config["pricing"]["agent"]["trials"] = self.trials
        config["pricing"]["agent"]["cost"] = self.cost
        self.init_agents(
            config["pricing"]["agent"], config["auction"]["agents"]
        )

    def init_agents(self, pricing_agent, bidding_agents):
        if self.PRICING:
            self.pricing_agent = PricingAgentFactory.build_agent(pricing_agent)
            self.num_agents = 1

        if self.BIDDING:
            for agent in bidding_agents:
                self.bidding_agents.extend(
                    BiddingAgentFactory.build_agent(agent)
                )
            self.num_agents = len(self.bidding_agents)

        if self.PRICING and self.BIDDING:
            assert (
                len(self.bidding_agents) == 1
            ), "Only one agent allowed when pricing in active!"

    def init_stats(self):
        if self.PRICING:
            self.prices = np.empty(self.length, dtype=float)
            self.profits = np.empty(
                (self.length, self.user_factory.n_users), dtype=float
            )

        if self.BIDDING:
            self.bids = np.empty(
                (self.num_agents, self.length, self.user_factory.n_users),
                dtype=float,
            )
            self.budgets = np.empty(
                (self.num_agents, self.length + 1, self.user_factory.n_users),
                dtype=float,
            )
            self.wins = np.empty(
                (self.num_agents, self.length, self.user_factory.n_users),
                dtype=bool,
            )
            self.costs = np.empty(
                (self.num_agents, self.length, self.user_factory.n_users),
                dtype=float,
            )

            # Save Starting Budgets
            starting_budget = np.array(
                [agent.budget for agent in self.bidding_agents]
            ).reshape(-1, 1)
            self.budgets[:, 0] = np.repeat(
                starting_budget, self.budgets.shape[2], axis=1
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
        for trial in range(self.trials):
            days_range = range(self.length)

            if self.VERBOSE:
                Logger.info(f"Trial {trial + 1}:")
            if not self.SILENT:
                print(f"Trial {trial + 1}:")
                days_range = track(days_range, description="Simulating...")

            # Init trial
            random.seed(self.seed + trial)
            np.random.seed(self.seed + trial)
            self.init_stats()
            if self.PRICING:
                self.pricing_agent.start_trial(trial)
            if self.BIDDING:
                for agent in self.bidding_agents:
                    agent.start_trial(trial)

            # Run trial
            for day_num in days_range:
                self.run_day(day_num)

            self.save_trial_stats()

    def run_day(self, day_num):
        if self.PRICING:
            # Make agents chhoose the prices
            price = self.pricing_agent.get_price(day_num)

        users = self.user_factory.build_users()
        profits = [0] * self.user_factory.n_users
        n_users_seen = 0
        for auction_num, user in enumerate(users):
            won = [True] * self.num_agents
            if self.BIDDING:
                won = self.run_auction(day_num, auction_num)

            if self.PRICING:
                # Make user buy the products
                # NOTE when pricing is active there's only one agent!!
                won = won[0]
                if won:
                    n_users_seen += 1
                    if user.does_buy(price):
                        profits[auction_num] = price - self.cost

        # Update agent with the profits for the day normalized by the
        # number of users that actually saw the price and decided
        # whether to buy the product or not. If only PRICING is active
        # then every user sees the price, if BOTH are active then the
        # number of users that see the price depends on the bidding
        # strategy.
        self.pricing_agent.update(sum(profits) / n_users_seen)

        # Save Statistics
        if self.PRICING:
            self.prices[day_num] = price
            self.profits[day_num, :] = profits

    def run_auction(self, day_num, auction_num) -> List[bool]:
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
        self.budgets[:, day_num + 1, auction_num] = [
            agent.budget for agent in self.bidding_agents
        ]

        return won

    def save_trial_stats(self) -> None:
        if not self.VERBOSE:
            return

        np.set_printoptions(threshold=np.inf)
        if self.PRICING:
            Logger.info("Pricing stats:")
            Logger.info("Prices:")
            Logger.info(self.prices)
            Logger.info("Profits:")
            Logger.info(self.profits)

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

    def save_sim_stats(self) -> None:
        if self.PRICING:
            self.pricing_agent.save_stats()

        if self.BIDDING:
            for agent in self.bidding_agents:
                agent.save_stats()


if __name__ == "__main__":
    config = load_config()
    Logger.init(config["log_path"])
    JPEGger.init(config["log_path"])
    # TODO arg parser
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

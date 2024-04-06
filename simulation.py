from random import random

from rich.progress import track

from config.config import load_config
from logger.logger import Logger
from src.agents.bidding.random_bidding_agent import RandomBiddingAgent
from src.agents.pricing.random_pricing_agent import RandomPricingAgent
from src.auctions.random_auction import RandomAuction

config = load_config()

assert config["type"] in {
    "pricing",
    "bidding",
    "both",
}, "Simulation type not supported!"

Logger.init(config["log_path"])

if config["type"] != "bidding":
    pricing_agent = RandomPricingAgent()
if config["type"] != "pricing":
    bidding_agent = RandomBiddingAgent()

for day_num in track(range(config["sim_length"]), description="Simulating..."):
    Logger.info(f"Simulating day #{day_num + 1}")
    if config["type"] != "bidding":
        price = pricing_agent.get_price()
        Logger.info(f"The agent chose the price: {price}")

    for auction_num in range(config["n_steps_per_day"]):
        won = True
        if config["type"] != "pricing":
            Logger.info(f"Aution #{auction_num + 1}")
            auction = RandomAuction(config["auction"]["n_opponents_dist"])
            bid = bidding_agent.get_bid()
            Logger.info(f"The agent chose the bid: {bid}")
            auction.place_bid(bid)
            won, cost = auction.did_win()

            if not won:
                Logger.info("The agent did not win the auction")
                continue

            Logger.info(f"The agent won the auction with cost {cost}")

        if config["type"] != "bidding":
            # Random client that always observes the ad
            if random() < 0.5:
                Logger.info(f"The client bought the item at price {price}")
            else:
                Logger.info("The client did not by the item")

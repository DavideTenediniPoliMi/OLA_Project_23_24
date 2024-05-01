from typing import Any, Dict

from src.auctions.auction import Auction
from src.auctions.generalized_first_price_auction import (
    GeneralizedFirstPriceAuction,
)
from src.auctions.random_auction import RandomAuction
from src.auctions.second_price_auction import SecondPriceAuction


class AuctionFactory:
    def __init__(self, auction: Dict[str, Any]) -> None:
        self.auction = auction

    def build_auction(self, day: int, auction_num: int) -> Auction:
        match self.auction["type"]:
            case "random":
                return RandomAuction(
                    self.auction["opponents"], day, auction_num
                )
            case "second_price":
                return SecondPriceAuction(
                    self.auction["opponents"], day, auction_num
                )
            case "generalized_first_price":
                return GeneralizedFirstPriceAuction(self.auction["opponents"])
            case _:
                raise NotImplementedError("Auction type not supported!")

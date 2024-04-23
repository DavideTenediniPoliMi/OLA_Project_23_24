from typing import Any, Dict

from src.auctions.auction import Auction
from src.auctions.generalized_first_price_auction import (
    GeneralizedFirstPriceAuction,
)
from src.auctions.random_auction import RandomAuction
from src.auctions.second_price_auction import SecondPriceAuction


class AuctionFactory:
    @staticmethod
    def build_auction(
        auction: Dict[str, Any], day: int, auction_num: int
    ) -> Auction:
        match auction["type"]:
            case "random":
                return RandomAuction(auction["opponents"], day, auction_num)
            case "second_price":
                return SecondPriceAuction(
                    auction["opponents"], day, auction_num
                )
            case "generalized_first_price":
                return GeneralizedFirstPriceAuction(auction["opponents"])
            case _:
                raise NotImplementedError("Auction type not supported!")

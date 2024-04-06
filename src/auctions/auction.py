from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
from numpy import ndarray
from scipy.stats import truncnorm, randint

from logger.logger import Logger


class Auction(ABC):

    def __init__(self, n_opponents_dist_params: Dict[str, Any]) -> None:
        self.player_bid: float
        self.n_opponents: int

        self._init_n_opponents(n_opponents_dist_params)
        self._init_opponents_bids()

    def _init_n_opponents(self, params) -> None:
        match params["type"]:
            case "trunc_normal":
                loc, scale = params["mean"], params["std"]
                # a, b in truncnorm are the number of std, so we need to
                # transform the abscissae value
                a = (params["min"] - loc) / scale
                b = (params["max"] - loc) / scale
                self.n_opponents = int(
                    truncnorm.rvs(a, b, loc=loc, scale=scale)
                )
            case "constant":
                self.n_opponents = params["mean"]
            case "uniform":
                self.n_opponents = randint.rvs(params["min"], params["max"])
            case _:
                raise NotImplementedError(
                    "Distribution for the number of opponents in the auction is not supported"
                )

        Logger.info(f"This auction has {self.n_opponents + 1} participants")

    def place_bid(self, bid: float) -> None:
        """Places the bid of the player."""
        self.player_bid = bid

    @abstractmethod
    def did_win(self) -> Tuple[bool, float | None]:
        """
        Returns whether the player won the auction. If it did, then it also
        returns the cost that the player has incurred.

        Returns:
            A bool indicating if the player won or not. If it won, then
            a Typle with also the cost incurred.
        """
        pass

    @abstractmethod
    def _init_opponents_bids(self) -> int | ndarray:
        """Return the bids of the opponents."""
        pass

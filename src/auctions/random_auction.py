from random import random, randrange
from typing import Any, Dict, Optional, Tuple

from numpy import ndarray

from src.auctions.auction import Auction


class RandomAuction(Auction):
    def __init__(
        self, opponents_params: Dict[str, Any], day: int, auction_num: int
    ) -> None:
        super().__init__(opponents_params, day, auction_num)
        self._winner: Optional[int] = None
        self._payment = random()

    def _declare_winner(self) -> None:
        self._winner = randrange(self.n_bidders)

    def did_win(self, id: int) -> Tuple[bool, float | None]:
        if self._winner == None:
            self._declare_winner()
        if id != self._winner:
            return False, None
        return True, self._payment

from typing import Any, Dict, Optional, Tuple

import numpy as np

from src.auctions.auction import Auction


class SecondPriceAuction(Auction):
    def __init__(self, opponents_params: Dict[str, Any]) -> None:
        super().__init__(opponents_params)
        self._winner: Optional[int] = None
        self._payment: float

    def _declare_winner(self) -> None:
        assert (
            self.n_bidders > 1
        ), "Not enough bidders for a second-price auction"
        winner, second = np.argsort(self._bids)[-2:].tolist()
        self._winner = winner
        self._payment = self._values[second] / self._CTRs[winner]

    def did_win(self, id: int) -> Tuple[bool, float | None]:
        if self._winner == None:
            self._declare_winner()
        if id != self._winner:
            return False, None
        return True, self._payment

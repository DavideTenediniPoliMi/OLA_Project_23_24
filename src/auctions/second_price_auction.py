from typing import Any, Dict, Optional, Tuple

import numpy as np
from src.auctions.auction import Auction


class SecondPriceAuction(Auction):
    def __init__(self, opponents_params: Dict[str, Any]) -> None:
        super().__init__(opponents_params)
        self._winner: Optional[int] = None
        self._cost: float

    def _declare_winner(self) -> None:
        assert (
            self.n_bidders > 1
        ), "Not enough bidders for a second-price auction"
        winner, runner_up = np.argsort(self._bids)[-2:].tolist()
        self._winner = winner
        self._cost = self._bids[runner_up]

    def did_win(self, id: int) -> Tuple[bool, float | None]:
        if self._winner == None:
            self._declare_winner()
        if id != self._winner:
            return False, None
        return True, self._cost

from typing import Any, Dict, List, Tuple

import numpy as np

from src.auctions.auction import Auction


class GeneralizedFirstPriceAuction(Auction):
    def __init__(self, opponents_params: Dict[str, Any], k: int) -> None:
        super().__init__(opponents_params)
        self._winners: List[int]
        self.k = k

    def _declare_winner(self) -> None:
        self._winners = np.argsort(self._bids)[-self.k :].tolist()

    def did_win(self, id: int) -> Tuple[bool, float | None]:
        if len(self._winners) == 0:
            self._declare_winner()
        if id not in self._winners:
            return False, None
        return True, self._bids[id]

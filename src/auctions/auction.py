from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from src.opponents.opponent_factory import OpponentFactory


class Auction(ABC):

    def __init__(
        self,
        opponents_params: Dict[str, Any],
        day: int,
        auction_num: int,
    ) -> None:
        # Build opponents
        factory = OpponentFactory(opponents_params)
        self.opponenents = factory.build_opponents()
        self.n_opponents: int = len(self.opponenents)
        # Compute opponents' bids
        self.n_bidders: int = self.n_opponents
        self._bids: List[float] = []
        self._CTRs: List[float] = []
        self._values: List[float] = []

        for opponent in self.opponenents:
            self._bids.append(opponent.get_bid(day, auction_num))
            self._CTRs.append(opponent.get_CTR(day, auction_num))
            self._values.append(self._bids[-1] * self._CTRs[-1])

    def join(self, CTR) -> int:
        """Add a new bidder to the aution. Return its id number."""
        self.n_bidders += 1
        self._bids.append(None)
        self._CTRs.append(CTR)
        self._values.append(None)
        return self.n_bidders - 1

    def place_bid(self, id: int, bid: float) -> None:
        """Places the bid of the player `id`."""
        assert self.n_opponents <= id < self.n_bidders, "Unkown player!"
        assert self._bids[id] is None, "Player already bid!"
        self._bids[id] = bid
        self._values[id] = self._bids[id] * self._CTRs[id]

    @abstractmethod
    def _declare_winner(self) -> None:
        """Compute the winner's id for this auction"""
        pass

    @abstractmethod
    def did_win(self, id: int) -> Tuple[bool, float | None]:
        """
        Returns whether the player with `id` won the auction. If it did,
        then it also returns the cost that the player has incurred.

        Returns:
            A bool indicating if the player won or not. If it won, the
            second element of the tuple is the cost incurred.
        """

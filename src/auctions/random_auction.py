from random import randrange
from typing import Tuple

from numpy import ndarray

from src.auctions.auction import Auction


class RandomAuction(Auction):

    def _declare_winner(self) -> None:
        self._winner = randrange(self.n_opponents + 1)

    def did_win(self, id: int) -> Tuple[bool, float | None]:
        super().did_win(id)
        # Choose a random id as the winner

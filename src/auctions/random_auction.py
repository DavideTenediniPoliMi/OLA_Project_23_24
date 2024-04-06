from random import randrange
from typing import Tuple

from numpy import ndarray

from src.auctions.auction import Auction


class RandomAuction(Auction):

    def did_win(self) -> Tuple[bool, float | None]:
        # Choose a random number representing the participants
        # If the number is 0 than the player won
        winner = randrange(self.n_opponents + 1)
        if winner != 0:
            return False, None
        return True, self.player_bid

    def _init_opponents_bids(self) -> int | ndarray:
        # Not needed in the random auction
        return 0

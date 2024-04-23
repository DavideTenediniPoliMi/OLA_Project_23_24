from abc import ABC, abstractmethod


class Opponent(ABC):
    def get_CTR(self, day: int, auction_num: int) -> float:
        """Return the Click-Through Rate of this opponent's ad."""
        return 1

    @abstractmethod
    def get_bid(self, day: int, auction_num: int) -> float:
        """Return the bid of the opponent."""

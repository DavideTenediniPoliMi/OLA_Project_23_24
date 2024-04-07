from abc import ABC, abstractmethod


class Opponent(ABC):
    @abstractmethod
    def get_bid(self) -> float:
        """Return the bid of the opponent."""

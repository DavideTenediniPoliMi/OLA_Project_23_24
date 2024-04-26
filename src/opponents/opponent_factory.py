from typing import Any, Dict

from src.opponents.random_opponent import RandomOpponent
from src.utils.n_dist import get_n_from_n_dist


class OpponentFactory:
    def __init__(self, params: Dict[str, Any]) -> None:
        self.params = params
        self.n_opponents = get_n_from_n_dist(self.params["n_dist"])

    def build_opponents(self):
        return [self._build_opponent() for _ in range(self.n_opponents)]

    def _build_opponent(self):
        match self.params["type"]:
            case "random":
                return RandomOpponent()
            case _:
                raise NotImplementedError("Opponent type not supported!")

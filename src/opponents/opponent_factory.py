from typing import Any, Dict

from scipy.stats import randint, truncnorm

from src.opponents.random_opponent import RandomOpponent


class OpponentFactory:
    def __init__(self, params: Dict[str, Any]) -> None:
        self.n_opponents: int

        self.params = params
        self._init_n_opponents()

    def _init_n_opponents(self) -> None:
        params = self.params["n_dist"]
        match params["type"]:
            case "trunc_normal":
                loc, scale = params["mean"], params["std"]
                # a, b in truncnorm are the number of std, so we need to
                # transform the abscissae value
                a = (params["min"] - loc) / scale
                b = (params["max"] - loc) / scale
                self.n_opponents = int(
                    truncnorm.rvs(a, b, loc=loc, scale=scale)
                )
            case "constant":
                self.n_opponents = params["mean"]
            case "uniform":
                self.n_opponents = randint.rvs(params["min"], params["max"])
            case _:
                raise NotImplementedError("Distribution not supported!")

    def build_opponents(self):
        return [self._build_opponent() for _ in range(self.n_opponents)]

    def _build_opponent(self):
        match self.params["type"]:
            case "random":
                return RandomOpponent()
            case _:
                raise NotImplementedError("Opponent type not supported!")

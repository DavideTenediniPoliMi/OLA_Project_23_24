from typing import Any, Dict

from scipy.stats import randint, truncnorm


def get_n_from_n_dist(params: Dict[str, Any]) -> int:
    match params["type"]:
        case "trunc_normal":
            loc, scale = params["mean"], params["std"]
            # a, b in truncnorm are the number of std, so we need to
            # transform the abscissae value
            a = (params["min"] - loc) / scale
            b = (params["max"] - loc) / scale
            return int(truncnorm.rvs(a, b, loc=loc, scale=scale))
        case "constant":
            return params["mean"]
        case "uniform":
            return randint.rvs(params["min"], params["max"])
        case _:
            raise NotImplementedError("Distribution not supported!")

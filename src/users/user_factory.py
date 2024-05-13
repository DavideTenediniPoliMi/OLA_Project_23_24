from typing import Any, Dict

from matplotlib import pyplot as plt
import numpy as np

from logger.jpegger import JPEGger
from src.users.kernel_user import KernelUser
from src.users.linear_user import LinearUser
from src.users.logit_user import LogitUser
from src.users.probit_user import ProbitUser
from src.users.random_user import RandomUser
from src.users.user import User
from src.utils.n_dist import get_n_from_n_dist


class UserFactory:
    def __init__(self, params: Dict[str, Any]) -> None:
        self.params = params
        self.n_users = get_n_from_n_dist(self.params["n_dist"])

    def build_user(self, day: int) -> User:
        match self.params["type"]:
            case "random":
                return RandomUser()
            case "linear":
                return LinearUser(self.params["alpha"], self.params["beta"])
            case "logit":
                return LogitUser(self.params["alpha"], self.params["beta"])
            case "probit":
                return ProbitUser(self.params["alpha"], self.params["beta"])
            case "kernel":
                return KernelUser(
                    self.params["alpha"],
                    self.params["beta"],
                    self.params["gamma"],
                )
            case _:
                raise NotImplementedError("User type not supported!")

    def save_stats(self) -> None:
        fig = plt.figure()
        self.build_user(0).draw_prob(self.params["discretization"])
        JPEGger.save_jpg(fig, "user.jpg")

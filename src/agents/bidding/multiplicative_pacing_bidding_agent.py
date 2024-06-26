import numpy as np
from src.agents.bidding.bidding_agent import BiddingAgent


class MultiplicativePacingBiddingAgent(BiddingAgent):
    def __init__(
        self, T: int, valuation: int, eta: float, budget: float = 0
    ) -> None:
        super().__init__(T, valuation, budget)
        # Learning Rate
        self.eta = eta
        self.lmbd = 1
        self.rho = self.budget / self.T

    def get_bid(self, day: int, auction_num: int) -> float:
        if self.budget < 1:
            bid = self.budget
        else:
            bid = self.valuation / (self.lmbd + 1)

        self.action_hist.append(bid)
        return bid

    def incur_cost(self, cost: float) -> None:
        self.lmbd = np.clip(
            self.lmbd - self.eta * (self.rho - cost),
            a_min=0,
            a_max=1 / self.rho,
        )
        self.observation_hist.append(cost)

        return super().incur_cost(cost)

    def update(self, observation) -> None:
        pass

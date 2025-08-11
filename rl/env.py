import gym
from gym import spaces
import numpy as np
import pandas as pd

class TradingEnv(gym.Env):
    """A simple trading environment for reinforcement learning.

    The environment consumes a price series provided via a ``pandas``
    ``DataFrame`` with a ``price`` column. The observation consists of the
    current price, cash balance and asset holdings. Actions are:

    * 0 - hold
    * 1 - buy with all available cash
    * 2 - sell all holdings

    Rewards are the change in portfolio value across timesteps.
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self, data: pd.DataFrame, initial_balance: float = 1000.0,
                 fee: float = 0.001):
        super().__init__()
        if "price" not in data.columns:
            raise ValueError("data must contain a 'price' column")
        self.data = data.reset_index(drop=True)
        self.initial_balance = initial_balance
        self.fee = fee

        # Action space: hold, buy, sell
        self.action_space = spaces.Discrete(3)
        # Observation: price, balance, holdings
        self.observation_space = spaces.Box(low=0.0, high=np.inf, shape=(3,),
                                            dtype=np.float32)

        self.reset()

    def _get_obs(self) -> np.ndarray:
        price = float(self.data.loc[self.current_step, "price"])
        return np.array([price, self.balance, self.holdings],
                        dtype=np.float32)

    def _portfolio_value(self, price: float) -> float:
        return self.balance + self.holdings * price

    def step(self, action: int):
        price = float(self.data.loc[self.current_step, "price"])
        prev_value = self._portfolio_value(price)

        if action == 1:  # buy
            qty = self.balance / price
            cost = qty * price * (1 + self.fee)
            if cost <= self.balance:
                self.balance -= cost
                self.holdings += qty
        elif action == 2:  # sell
            revenue = self.holdings * price * (1 - self.fee)
            self.balance += revenue
            self.holdings = 0.0

        self.current_step += 1
        done = self.current_step >= len(self.data) - 1

        next_price = float(self.data.loc[self.current_step, "price"])
        current_value = self._portfolio_value(next_price)
        reward = current_value - prev_value

        obs = self._get_obs()
        info = {"portfolio_value": current_value}
        return obs, reward, done, info

    def reset(self):  # type: ignore[override]
        self.balance = float(self.initial_balance)
        self.holdings = 0.0
        self.current_step = 0
        return self._get_obs()

    def render(self, mode: str = "human") -> None:
        price = float(self.data.loc[self.current_step, "price"])
        value = self._portfolio_value(price)
        print(
            f"Step: {self.current_step} | Price: {price:.2f} | "
            f"Balance: {self.balance:.2f} | Holdings: {self.holdings:.4f} | "
            f"Value: {value:.2f}"
        )

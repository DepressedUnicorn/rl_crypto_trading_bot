"""Baseline agent utilities using Stable-Baselines3.

This module provides helper functions to train a simple PPO agent on the
:class:`TradingEnv` environment and to run inference with a saved model.
"""
from __future__ import annotations

import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from .env import TradingEnv


def load_data(csv_path: str) -> pd.DataFrame:
    """Load market data from a CSV file.

    The CSV file must contain at least a ``price`` column.
    """
    return pd.read_csv(csv_path)


def train(data_path: str, timesteps: int = 10_000,
          model_path: str = "ppo_trading") -> None:
    """Train a PPO agent on the :class:`TradingEnv`.

    Parameters
    ----------
    data_path: str
        Path to a CSV file containing the historical price data.
    timesteps: int
        Number of timesteps to train for.
    model_path: str
        Location where the trained model will be saved.
    """
    data = load_data(data_path)
    env = DummyVecEnv([lambda: TradingEnv(data)])
    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=timesteps)
    model.save(model_path)


def run_inference(data_path: str, model_path: str = "ppo_trading") -> float:
    """Run inference using a trained model.

    Parameters
    ----------
    data_path: str
        Path to CSV file with market data.
    model_path: str
        Path to the saved model.

    Returns
    -------
    float
        Final portfolio value after running the agent on the dataset.
    """
    data = load_data(data_path)
    env = TradingEnv(data)
    model = PPO.load(model_path)

    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, _, done, info = env.step(int(action))

    return float(info["portfolio_value"])

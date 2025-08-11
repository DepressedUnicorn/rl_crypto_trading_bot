# RL Crypto Trading Bot

This repository contains a simple reinforcement learning setup for training a
cryptocurrency trading agent.

## Components

- `rl/env.py` – OpenAI Gym–compatible environment based on portfolio value
  changes.
- `rl/baseline.py` – Utilities for training and running a PPO agent with
  Stable‑Baselines3.
- `rl/train.py` – Command line entry point for training.
- `rl/infer.py` – Command line entry point for inference.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the agent on historical data stored in `prices.csv`:

```bash
python -m rl.train prices.csv --timesteps 10000 --out ppo_trading
```

Run inference using the trained model:

```bash
python -m rl.infer prices.csv --model ppo_trading
```

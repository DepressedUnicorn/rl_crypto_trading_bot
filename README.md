# RL Crypto Trading Bot


## Environment Setup

### Python

This project targets **Python 3.11**. Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Environment Variables

Store your Binance API credentials in environment variables or a `.env` file:

```bash
export BINANCE_API_KEY="your-testnet-key"
export BINANCE_API_SECRET="your-testnet-secret"
```

> **Warning**: Never use real Binance API keys during development. Generate test credentials from the [Binance Testnet](https://testnet.binance.vision/).

## Example CLI Commands

Below are example commands illustrating how this project could be used once the CLI is implemented.

```bash
# Train the agent for 10 episodes
python bot.py train --episodes 10
# Expected output:
# Episode 1/10 - reward: ...
# ...
# Episode 10/10 - reward: ...
# Model saved to models/latest.pt

# Execute a trade on the testnet
python bot.py trade --symbol BTCUSDT --qty 0.001 --testnet
# Expected output:
# Placed order: BUY BTCUSDT qty=0.001 price=25000.0
```

Outputs will vary depending on market data and training progress.

## Additional Notes

- Ensure `requirements.txt` lists the libraries required by your implementation.
- This README will expand as the project evolves.

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
main

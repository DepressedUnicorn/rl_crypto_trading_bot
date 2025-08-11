"""Command line entry point for training the baseline agent."""
import argparse

from . import baseline


def main() -> None:
    parser = argparse.ArgumentParser(description="Train PPO trading agent")
    parser.add_argument("data", help="Path to CSV file with price data")
    parser.add_argument("--timesteps", type=int, default=10_000,
                        help="Number of training timesteps")
    parser.add_argument("--out", default="ppo_trading",
                        help="Where to save the trained model")
    args = parser.parse_args()
    baseline.train(args.data, timesteps=args.timesteps, model_path=args.out)


if __name__ == "__main__":
    main()

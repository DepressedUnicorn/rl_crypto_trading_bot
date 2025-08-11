"""Command line entry point for running inference with a trained model."""
import argparse

from . import baseline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run inference with PPO model")
    parser.add_argument("data", help="Path to CSV file with price data")
    parser.add_argument("--model", default="ppo_trading",
                        help="Path to the trained model")
    args = parser.parse_args()
    value = baseline.run_inference(args.data, model_path=args.model)
    print(f"Final portfolio value: {value:.2f}")


if __name__ == "__main__":
    main()

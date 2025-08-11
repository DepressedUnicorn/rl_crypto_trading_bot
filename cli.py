import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Command line interface for the RL crypto trading bot"
    )
    parser.add_argument(
        "--symbol",
        type=str,
        help="Trading pair symbol, e.g., BTCUSDT",
    )
    parser.add_argument(
        "--papertrading",
        action="store_true",
        help="Run in paper trading mode instead of live trading",
    )
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--train",
        action="store_true",
        help="Train the reinforcement learning agent",
    )
    action_group.add_argument(
        "--run",
        action="store_true",
        help="Run the trading bot",
    )
    args = parser.parse_args()
    return parser, args


def main():
    parser, args = parse_args()

    if args.train:
        if not args.symbol:
            parser.error("--symbol is required when training")
        from train import train_agent

        train_agent(args.symbol)
    elif args.run:
        if not args.symbol:
            parser.error("--symbol is required when running")
        if args.papertrading:
            from paper_trader import run_paper_trading

            run_paper_trading(args.symbol)
        else:
            from live_trader import run_live_trading

            run_live_trading(args.symbol)


if __name__ == "__main__":
    main()

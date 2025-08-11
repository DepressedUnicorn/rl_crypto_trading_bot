"""Configuration loader for environment variables."""
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Expose API keys
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

import os

# ==========================
# Telegram Settings
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ==========================
# Market
# ==========================
EXCHANGE = "binance"

SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "XRP/USDT",
]

TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
    "1h",
]

CHECK_INTERVAL = 15

# ==========================
# Strategy
# ==========================
MIN_SCORE = 80

RSI_BUY = 30
RSI_SELL = 70

EMA_FAST = 20
EMA_SLOW = 50

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ==========================
# Signal Control
# ==========================
SEND_DUPLICATE = False

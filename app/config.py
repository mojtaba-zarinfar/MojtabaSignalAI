import os

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# بررسی هر 15 ثانیه
CHECK_INTERVAL = 15

# ارزها
SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "XRP/USDT",
]

# تایم‌فریم‌ها
TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
]

# حداقل امتیاز لازم برای ارسال سیگنال
MIN_SCORE = 80

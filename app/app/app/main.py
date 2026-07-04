import time
import pandas as pd

from app.market import get_ohlcv
from app.indicators import add_indicators
from app.strategy import get_signal
from app.telegram_bot import send_message, format_signal
from app.config import SYMBOLS, TIMEFRAMES, CHECK_INTERVAL


def run_analysis():
    for symbol in SYMBOLS:

        try:
            # گرفتن دیتا
            data = get_ohlcv(symbol, timeframe="5m", limit=200)

            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume"
            ])

            # اندیکاتورها
            df = add_indicators(df)

            latest = df.iloc[-1]
            current_price = latest["close"]
            entry_price = df["close"].mean()  # ساده برای نسخه 1

            # سیگنال
            signal = get_signal(latest, entry_price, current_price)

            if signal:

                text = format_signal(signal, symbol)
                send_message(text)

        except Exception as e:
            print(f"Error in {symbol}: {e}")


if __name__ == "__main__":
    print("Bot started...")

    while True:
        run_analysis()
        time.sleep(CHECK_INTERVAL)

import time
import pandas as pd

from app.config import SYMBOLS, TIMEFRAMES, CHECK_INTERVAL
from app.market import get_ohlcv
from app.indicators import add_indicators
from app.strategy import get_final_signal, validate_signal
from app.telegram_bot import send_message, format_signal
from app.btc_filter import analyze_btc


# ==========================================
# Get BTC Context
# ==========================================

def get_btc_context():

    data = get_ohlcv("BTC/USDT", timeframe="5m", limit=200)

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume"
    ])

    df = add_indicators(df)

    return analyze_btc(df)


# ==========================================
# Get Market Data
# ==========================================

def get_symbol_data(symbol, timeframe):

    data = get_ohlcv(symbol, timeframe=timeframe, limit=200)

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume"
    ])

    df = add_indicators(df)

    return df

# ==========================================
# Run Analysis
# ==========================================

def run_analysis():

    btc_result = get_btc_context()

    for symbol in SYMBOLS:

        try:

            for tf in TIMEFRAMES:

                df = get_symbol_data(symbol, tf)

                signal = get_final_signal(df, btc_result)

                if not validate_signal(signal):
                    continue

                text = format_signal(signal, symbol)

                send_message(text)

        except Exception as e:
            print(f"Error in {symbol}: {e}")


# ==========================================
# Main Loop
# ==========================================

if __name__ == "__main__":

    print("Bot Started...")

    while True:

        run_analysis()

        time.sleep(CHECK_INTERVAL)

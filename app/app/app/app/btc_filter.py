import pandas as pd

from app.indicators import add_indicators


# ==========================================
# BTC Trend Analyzer
# ==========================================

def analyze_btc(df):

    df = add_indicators(df)

    last = df.iloc[-1]

    score = 0

    # EMA
    if last["ema20"] > last["ema50"]:
        score += 30

    # MACD
    if last["macd"] > last["macd_signal"]:
        score += 25

    # RSI
    if 45 <= last["rsi"] <= 70:
        score += 20

    # Momentum
    if last["macd_hist"] > 0:
        score += 15

    # Volume
    avg_volume = df["volume"].tail(20).mean()

    if last["volume"] > avg_volume:
        score += 10

    if score >= 80:
        trend = "BULLISH"

    elif score >= 55:
        trend = "NEUTRAL"

    else:
        trend = "BEARISH"

    return {
        "trend": trend,
        "score": score
    }


# ==========================================
# BTC Permission
# ==========================================

def allow_trade(btc_result, market_type):

    trend = btc_result["trend"]

    if trend == "BULLISH":
        return True

    if trend == "NEUTRAL":
        return True

    # بازار نزولی

    if market_type == "PULLBACK":
        return True

    if market_type == "BOUNCE":
        return True

    return False

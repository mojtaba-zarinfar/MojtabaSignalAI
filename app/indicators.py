import pandas as pd
import numpy as np


# ==========================================
# EMA
# ==========================================

def ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


# ==========================================
# RSI
# ==========================================

def rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()

    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss

    return 100 - (100 / (1 + rs))


# ==========================================
# MACD
# ==========================================

def macd(df):

    ema12 = ema(df, 12)

    ema26 = ema(df, 26)

    macd_line = ema12 - ema26

    signal = macd_line.ewm(span=9, adjust=False).mean()

    hist = macd_line - signal

    return macd_line, signal, hist


# ==========================================
# ATR
# ==========================================

def atr(df, period=14):

    high_low = df["high"] - df["low"]

    high_close = np.abs(df["high"] - df["close"].shift())

    low_close = np.abs(df["low"] - df["close"].shift())

    tr = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    return tr.rolling(period).mean()


# ==========================================
# Average Volume
# ==========================================

def average_volume(df, period=20):

    return df["volume"].rolling(period).mean()


# ==========================================
# Volume Spike
# ==========================================

def volume_spike(df):

    avg = average_volume(df)

    return df["volume"] > (avg * 1.5)


# ==========================================
# Trend Power
# ==========================================

def trend_power(df):

    last = df.iloc[-1]

    score = 0

    if last["ema20"] > last["ema50"]:
        score += 1

    if last["ema50"] > last["ema200"]:
        score += 1

    if last["macd"] > last["macd_signal"]:
        score += 1

    if last["rsi"] > 50:
        score += 1

    return score

# ==========================================
# Distance From EMA
# ==========================================

def ema_distance(df):

    close = df["close"]

    return (
        ((close - df["ema20"]) / df["ema20"]) * 100,
        ((close - df["ema50"]) / df["ema50"]) * 100,
        ((close - df["ema200"]) / df["ema200"]) * 100,
    )


# ==========================================
# Market Volatility
# ==========================================

def volatility_state(df):

    last_atr = df["atr"].iloc[-1]
    avg_atr = df["atr"].tail(20).mean()

    if pd.isna(last_atr) or pd.isna(avg_atr):
        return "NORMAL"

    if last_atr > avg_atr * 1.30:
        return "HIGH"

    if last_atr < avg_atr * 0.70:
        return "LOW"

    return "NORMAL"


# ==========================================
# Trend Direction
# ==========================================

def trend_direction(df):

    last = df.iloc[-1]

    if (
        last["ema20"] > last["ema50"] > last["ema200"]
        and last["macd"] > last["macd_signal"]
    ):
        return "UP"

    if (
        last["ema20"] < last["ema50"] < last["ema200"]
        and last["macd"] < last["macd_signal"]
    ):
        return "DOWN"

    return "SIDE"


# ==========================================
# Add All Indicators
# ==========================================

def add_indicators(df):

    df = df.copy()

    df["rsi"] = rsi(df)

    df["ema20"] = ema(df, 20)
    df["ema50"] = ema(df, 50)
    df["ema200"] = ema(df, 200)

    macd_line, signal, hist = macd(df)

    df["macd"] = macd_line
    df["macd_signal"] = signal
    df["macd_hist"] = hist

    df["atr"] = atr(df)

    df["avg_volume"] = average_volume(df)

    df["volume_spike"] = volume_spike(df)

    d20, d50, d200 = ema_distance(df)

    df["ema20_distance"] = d20
    df["ema50_distance"] = d50
    df["ema200_distance"] = d200

    return df

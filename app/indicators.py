import pandas as pd
import numpy as np


# =========================
# RSI
# =========================
def rsi(df, period=14):
    delta = df["close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))


# =========================
# EMA
# =========================
def ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


# =========================
# MACD
# =========================
def macd(df):
    ema12 = ema(df, 12)
    ema26 = ema(df, 26)

    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram


# =========================
# Add all indicators
# =========================
def add_indicators(df):
    df["rsi"] = rsi(df)
    df["ema20"] = ema(df, 20)
    df["ema50"] = ema(df, 50)

    macd_line, signal_line, hist = macd(df)
    df["macd"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_hist"] = hist

    return df

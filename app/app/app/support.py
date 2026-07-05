import numpy as np
import pandas as pd


# ==========================================
# Swing High / Swing Low
# ==========================================

def find_pivots(df, left=3, right=3):

    highs = df["high"].values
    lows = df["low"].values

    pivot_highs = []
    pivot_lows = []

    for i in range(left, len(df) - right):

        high = highs[i]

        if high == max(highs[i-left:i+right+1]):
            pivot_highs.append((i, high))

        low = lows[i]

        if low == min(lows[i-left:i+right+1]):
            pivot_lows.append((i, low))

    return pivot_highs, pivot_lows


# ==========================================
# Merge close levels
# ==========================================

def merge_levels(levels, tolerance=0.003):

    if len(levels) == 0:
        return []

    values = sorted([x[1] for x in levels])

    merged = []

    current = values[0]

    bucket = [current]

    for value in values[1:]:

        if abs(value-current)/current <= tolerance:

            bucket.append(value)

        else:

            merged.append(sum(bucket)/len(bucket))

            bucket = [value]

        current = value

    if bucket:
        merged.append(sum(bucket)/len(bucket))

    return merged


# ==========================================
# Strong Support
# ==========================================

def get_supports(df):

    _, lows = find_pivots(df)

    supports = merge_levels(lows)

    supports.sort(reverse=True)

    return supports[:3]


# ==========================================
# Strong Resistance
# ==========================================

def get_resistances(df):

    highs, _ = find_pivots(df)

    resistances = merge_levels(highs)

    resistances.sort()

    return resistances[:3]


# ==========================================
# Closest Levels
# ==========================================

def nearest_support(df):

    price = df.iloc[-1]["close"]

    supports = get_supports(df)

    for s in supports:

        if s < price:
            return s

    return None


def nearest_resistance(df):

    price = df.iloc[-1]["close"]

    resistances = get_resistances(df)

    for r in resistances:

        if r > price:
            return r

    return None

# ==========================================
# Distance Calculations
# ==========================================

def distance_to_support(price, support):

    if support is None:
        return None

    return ((price - support) / price) * 100


def distance_to_resistance(price, resistance):

    if resistance is None:
        return None

    return ((resistance - price) / price) * 100


# ==========================================
# Reward / Risk
# ==========================================

def reward_percent(price, target):

    if target is None:
        return 0

    return ((target - price) / price) * 100


def risk_percent(price, stop):

    if stop is None:
        return 100

    return ((price - stop) / price) * 100


# ==========================================
# Dynamic Stop Loss
# ==========================================

def dynamic_stop(df):

    support = nearest_support(df)

    if support is None:
        return None

    return support * 0.997


# ==========================================
# Dynamic Take Profit
# ==========================================

def dynamic_target(df):

    resistance = nearest_resistance(df)

    if resistance is None:
        return None

    return resistance * 0.997


# ==========================================
# Breakout Detection
# ==========================================

def is_breakout(df):

    resistance = nearest_resistance(df)

    if resistance is None:
        return False

    close = df.iloc[-1]["close"]

    volume = df.iloc[-1]["volume"]

    avg_volume = df["volume"].tail(20).mean()

    if close > resistance and volume > avg_volume * 1.5:
        return True

    return False


# ==========================================
# Bounce Detection
# ==========================================

def is_bounce(df):

    support = nearest_support(df)

    if support is None:
        return False

    close = df.iloc[-1]["close"]

    low = df.iloc[-1]["low"]

    volume = df.iloc[-1]["volume"]

    avg_volume = df["volume"].tail(20).mean()

    touch = abs(low - support) / support <= 0.003

    bullish = close > support

    return touch and bullish and volume > avg_volume

# ==========================================
# Pullback Detection
# ==========================================

def is_pullback(df):

    if len(df) < 25:
        return False

    close = df.iloc[-1]["close"]
    ema20 = df.iloc[-1]["ema20"]

    distance = abs(close - ema20) / ema20

    # نزدیک EMA20 باشد
    if distance > 0.004:
        return False

    # کندل آخر صعودی باشد
    if close <= df.iloc[-1]["open"]:
        return False

    return True


# ==========================================
# Fake Breakout Filter
# ==========================================

def fake_breakout(df):

    resistance = nearest_resistance(df)

    if resistance is None:
        return False

    last = df.iloc[-1]

    if last["high"] > resistance and last["close"] < resistance:
        return True

    return False


# ==========================================
# Market Zone
# ==========================================

def market_zone(df):

    support = nearest_support(df)
    resistance = nearest_resistance(df)

    if support is None or resistance is None:
        return "UNKNOWN"

    price = df.iloc[-1]["close"]

    width = resistance - support

    if width <= 0:
        return "UNKNOWN"

    position = (price - support) / width

    if position < 0.25:
        return "BUY_ZONE"

    if position > 0.75:
        return "SELL_ZONE"

    return "MIDDLE"


# ==========================================
# Full Support & Resistance Analysis
# ==========================================

def analyze_levels(df):

    support = nearest_support(df)
    resistance = nearest_resistance(df)

    return {
        "support": support,
        "resistance": resistance,
        "stop": dynamic_stop(df),
        "target": dynamic_target(df),
        "reward": reward_percent(df.iloc[-1]["close"], dynamic_target(df)),
        "risk": risk_percent(df.iloc[-1]["close"], dynamic_stop(df)),
        "bounce": is_bounce(df),
        "breakout": is_breakout(df),
        "fake_breakout": fake_breakout(df),
        "pullback": is_pullback(df),
        "zone": market_zone(df),
    }

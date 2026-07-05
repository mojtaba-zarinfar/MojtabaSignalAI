from app.support import analyze_levels
from app.scoring import (
    calculate_score,
    signal_strength,
    can_send_signal,
    entry_warning,
)
from app.btc_filter import allow_trade


# ==========================================
# Detect Market Type
# ==========================================

def detect_market_type(df, btc_result):

    levels = analyze_levels(df)

    trend = "SIDE"

    last = df.iloc[-1]

    if (
        last["ema20"] > last["ema50"] > last["ema200"]
    ):
        trend = "UP"

    elif (
        last["ema20"] < last["ema50"] < last["ema200"]
    ):
        trend = "DOWN"

    # برگشت از حمایت
    if levels["bounce"]:
        return "BOUNCE"

    # پول‌بک
    if levels["pullback"]:
        return "PULLBACK"

    return trend


# ==========================================
# Build Signal
# ==========================================

def build_signal(df, btc_result):

    market_type = detect_market_type(df, btc_result)

    if not allow_trade(btc_result, market_type):
        return None

    result = calculate_score(df, btc_result)

    if not can_send_signal(result):
        return None

    levels = result["levels"]

    last = df.iloc[-1]

    signal = {

        "type": "BUY",

        "score": result["score"],

        "strength": signal_strength(result["score"]),

        "entry": last["close"],

        "target": levels["target"],

        "stop": levels["stop"],

        "reward": levels["reward"],

        "risk": levels["risk"],

        "reasons": result["reasons"],

        "zone": levels["zone"],

        "market": market_type,
    }

    return signal

# ==========================================
# Pre-Signal Warning
# ==========================================

def pre_signal(df, entry_price):

    last = df.iloc[-1]

    current_price = last["close"]

    diff = abs(current_price - entry_price) / entry_price * 100

    # هشدار نزدیک ورود
    if 0.1 <= diff <= 0.3:
        return {
            "type": "WARNING",
            "message": "⚠️ نزدیک محدوده ورود هستیم",
            "distance": diff
        }

    return None


# ==========================================
# Final Decision Wrapper
# ==========================================

def get_final_signal(df, btc_result):

    # ساخت سیگنال اصلی
    signal = build_signal(df, btc_result)

    if signal is None:
        return None

    # بررسی هشدار قبل ورود
    warning = pre_signal(df, signal["entry"])

    if warning:
        signal["warning"] = warning

    return signal


# ==========================================
# Safe Signal Validator
# ==========================================

def validate_signal(signal):

    if signal is None:
        return False

    # حداقل سود 1.5٪
    if signal["reward"] < 1.5:
        return False

    # حداقل امتیاز
    if signal["score"] < 80:
        return False

    # جلوگیری از ریسک بالا
    if signal["risk"] > 4:
        return False

    return True

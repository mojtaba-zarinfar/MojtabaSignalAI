from app.support import analyze_levels


# ==========================================
# Score System
# ==========================================

MAX_SCORE = 100


def calculate_score(df, btc_result):

    last = df.iloc[-1]

    levels = analyze_levels(df)

    score = 0

    reasons = []

    # ==========================
    # BTC Trend
    # ==========================

    if btc_result["trend"] == "BULLISH":
        score += 15
        reasons.append("BTC Trend Bullish")

    elif btc_result["trend"] == "NEUTRAL":
        score += 8
        reasons.append("BTC Trend Neutral")

    else:
        reasons.append("BTC Trend Bearish")


    # ==========================
    # EMA Trend
    # ==========================

    if last["ema20"] > last["ema50"]:
        score += 15
        reasons.append("EMA20 > EMA50")

    elif abs(last["ema20"] - last["ema50"]) / last["close"] < 0.003:
        score += 8
        reasons.append("EMA Compression")


    # ==========================
    # RSI
    # ==========================

    if 35 <= last["rsi"] <= 55:
        score += 10
        reasons.append("Healthy RSI")

    elif last["rsi"] < 35:
        score += 14
        reasons.append("RSI Pullback")


    # ==========================
    # MACD
    # ==========================

    if last["macd"] > last["macd_signal"]:
        score += 12
        reasons.append("MACD Bullish")

    if last["macd_hist"] > 0:
        score += 8
        reasons.append("Positive Momentum")


    # ==========================
    # Volume
    # ==========================

    avg_volume = df["volume"].tail(20).mean()

    if last["volume"] > avg_volume * 1.3:
        score += 10
        reasons.append("High Volume")

    elif last["volume"] > avg_volume:
        score += 5
        reasons.append("Good Volume")

    # ==========================
    # Support / Resistance
    # ==========================

    if levels["bounce"]:
        score += 15
        reasons.append("Support Bounce")

    if levels["pullback"]:
        score += 12
        reasons.append("EMA Pullback")

    if levels["breakout"]:
        score += 12
        reasons.append("Resistance Breakout")

    if levels["fake_breakout"]:
        score -= 15
        reasons.append("Fake Breakout")

    # ==========================
    # Market Zone
    # ==========================

    if levels["zone"] == "BUY_ZONE":
        score += 10
        reasons.append("Buy Zone")

    elif levels["zone"] == "MIDDLE":
        score += 3

    elif levels["zone"] == "SELL_ZONE":
        score -= 10
        reasons.append("Near Resistance")

    # ==========================
    # Reward / Risk
    # ==========================

    reward = levels["reward"]
    risk = levels["risk"]

    if reward >= 3:
        score += 15
        reasons.append("Reward > 3%")

    elif reward >= 2:
        score += 10
        reasons.append("Reward > 2%")

    elif reward >= 1.5:
        score += 5
        reasons.append("Reward > 1.5%")

    else:
        score -= 20
        reasons.append("Low Profit Potential")

    if risk <= 1:
        score += 5
        reasons.append("Low Risk")

    elif risk > 3:
        score -= 10
        reasons.append("High Risk")

    # ==========================
    # Final Score Limits
    # ==========================

    if score < 0:
        score = 0

    if score > MAX_SCORE:
        score = MAX_SCORE

    return {
        "score": score,
        "reasons": reasons,
        "levels": levels
    }


# ==========================================
# Signal Quality
# ==========================================

def signal_strength(score):

    if score >= 90:
        return "VERY_STRONG"

    if score >= 80:
        return "STRONG"

    if score >= 70:
        return "GOOD"

    if score >= 60:
        return "WEAK"

    return "IGNORE"


# ==========================================
# Entry Warning
# ==========================================

def entry_warning(current_price, entry_price):

    if entry_price <= 0:
        return False

    diff = abs(current_price - entry_price) / entry_price * 100

    return diff <= 0.30


# ==========================================
# Can Send Signal
# ==========================================

def can_send_signal(result):

    score = result["score"]
    reward = result["levels"]["reward"]

    # حداقل سود مورد انتظار
    if reward < 1.5:
        return False

    # حداقل امتیاز
    if score < 80:
        return False

    return True

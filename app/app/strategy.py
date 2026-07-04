from app.config import RSI_BUY, RSI_SELL, MIN_SCORE


# =========================
# Score-based Strategy
# =========================
def calculate_score(row):
    score = 0
    reasons = []

    # Trend (EMA)
    if row["ema20"] > row["ema50"]:
        score += 20
        reasons.append("Uptrend (EMA20 > EMA50)")
    else:
        score += 0

    # RSI
    if row["rsi"] < RSI_BUY:
        score += 20
        reasons.append("RSI oversold zone")
    elif row["rsi"] > RSI_SELL:
        score += 0
    else:
        score += 10
        reasons.append("RSI neutral zone")

    # MACD
    if row["macd"] > row["macd_signal"]:
        score += 20
        reasons.append("MACD bullish crossover")

    # Momentum
    if row["macd_hist"] > 0:
        score += 15
        reasons.append("Positive momentum")

    # Volume (simple heuristic)
    if row.get("volume", 0) > 0:
        score += 10

    return score, reasons


# =========================
# Signal decision
# =========================
def get_signal(row, entry_price, current_price):
    score, reasons = calculate_score(row)

    # فاصله تا ورود
    diff = abs(current_price - entry_price) / entry_price * 100

    # =========================
    # 1. PRE-SIGNAL (0.3%)
    # =========================
    if 0.1 <= diff <= 0.3 and score >= (MIN_SCORE - 10):
        return {
            "type": "WARNING",
            "score": score,
            "reasons": reasons,
            "message": "⚠️ نزدیک محدوده ورود هستیم (0.3%)"
        }

    # =========================
    # 2. ENTRY SIGNAL
    # =========================
    if score >= MIN_SCORE:
        potential_profit = 1.5  # حداقل سود مورد انتظار

        if potential_profit < 1.5:
            return None

        return {
            "type": "ENTRY",
            "score": score,
            "reasons": reasons,
            "message": "🟢 سیگنال ورود"
        }

    # =========================
    # 3. NO SIGNAL
    # =========================
    return None

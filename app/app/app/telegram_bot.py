import requests
from app.config import BOT_TOKEN, CHAT_ID


BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ==========================================
# Send Message
# ==========================================

def send_message(text):

    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        requests.post(url, data=payload, timeout=10)

    except Exception as e:
        print("Telegram error:", e)


# ==========================================
# Format Signal Message
# ==========================================

def format_signal(signal, symbol):

    msg = f"""
📊 <b>{symbol}</b>

📍 Type: {signal.get('type')}
⚡ Strength: {signal.get('strength')}
📈 Score: {signal.get('score')}

💰 Entry: {signal.get('entry')}
🎯 Target: {signal.get('target')}
🛑 Stop: {signal.get('stop')}

📊 Reward: {signal.get('reward'):.2f}%
📉 Risk: {signal.get('risk'):.2f}%

📌 Market: {signal.get('market')}
📍 Zone: {signal.get('zone')}

"""

    if signal.get("warning"):
        w = signal["warning"]
        msg += f"\n⚠️ Warning: نزدیک ورود ({w.get('distance'):.2f}%)\n"

    msg += "\n📌 Reasons:\n"

    for r in signal.get("reasons", []):
        msg += f"• {r}\n"

    return msg

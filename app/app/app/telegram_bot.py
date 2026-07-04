import requests
from app.config import BOT_TOKEN, CHAT_ID


BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(text):
    """
    ارسال پیام ساده به تلگرام
    """
    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


def format_signal(signal, symbol):
    """
    ساخت پیام حرفه‌ای برای سیگنال
    """

    msg = f"""
📊 <b>{symbol}</b>

{signal.get('message')}

📈 Score: {signal.get('score')}

📌 Reasons:
"""

    for r in signal.get("reasons", []):
        msg += f"• {r}\n"

    return msg

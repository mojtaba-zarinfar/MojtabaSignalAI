import ccxt
from app.config import EXCHANGE

def get_exchange():
    """
    ایجاد اتصال به صرافی
    """
    if EXCHANGE == "auto":
        return ccxt.kucoin({
            "enableRateLimit": True,
        })

    return getattr(ccxt, EXCHANGE)({
        "enableRateLimit": True,
    })

exchange = get_exchange()


def get_ohlcv(symbol, timeframe="5m", limit=200):
    """
    دریافت کندل‌ها
    """
    return exchange.fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit
    )

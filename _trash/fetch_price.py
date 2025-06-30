# file: alpha_vantage_client.py

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env (must be in project root)
load_dotenv()

def fetch_daily_price(symbol: str, outputsize: str = "compat") -> dict:
    """
    Fetch daily time series data for a given symbol from Alpha Vantage.

    Args:
        symbol (str): Stock ticker, e.g. "TSLA".
        outputsize (str): "compact" or "full". "full" returns full-length history.

    Returns:
        dict: Parsed JSON response from Alpha Vantage.
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found. Please set ALPHA_VANTAGE_API_KEY in .env")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": outputsize,
        "datatype": "json",   # 返回 JSON；若改成 "csv" 则直接返回 CSV 文本
        "apikey": api_key
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()  # 如果 HTTP 状态不是 200，会抛异常
    return resp.json()


def save_json(data: dict, filename: str) -> None:
    """
    Save a Python dict as a JSON file.

    Args:
        data (dict): 要保存的数据结构
        filename (str): 保存路径，如 "TSLA_daily.json"
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 测试：下载 TSLA 全量历史日线并保存
    tsla_data = fetch_daily_price("TSLA", outputsize="full")
    save_json(tsla_data, "TSLA_daily.json")
    print("✅ TSLA 日线数据已保存到 TSLA_daily.json")

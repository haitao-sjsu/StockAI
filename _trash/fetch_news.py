import os
import json
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load Alpha Vantage API key from environment
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    raise RuntimeError("API key not found. Please set ALPHA_VANTAGE_API_KEY in your .env file.")


def fetch_news_sentiment(
    symbol: str,
    limit: int = 1000,
    sort: str = "LATEST",
    time_from: str = None,
    time_to: str = None
) -> list[dict]:
    """
    Fetch raw news sentiment feed for a given stock ticker using the Alpha Vantage NEWS_SENTIMENT API.
    Does not apply any filtering, returns up to `limit` items sorted by the specified order.

    Args:
        symbol (str): Stock ticker symbol (e.g., "TSLA").
        limit (int): Maximum number of articles to request (up to 1000).
        sort (str): Sort order: "LATEST", "EARLIEST", or "RELEVANCE".
        time_from (str, optional): Start time in "YYYYMMDDTHHMM" format (UTC).
        time_to (str, optional): End time in "YYYYMMDDTHHMM" format (UTC).

    Returns:
        list[dict]: List of news feed items as returned by the API.
    """
    endpoint = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "limit": limit,
        "sort": sort,
        "apikey": API_KEY
    }
    if time_from:
        params["time_from"] = time_from
    if time_to:
        params["time_to"] = time_to

    response = requests.get(endpoint, params=params, timeout=15)
    response.raise_for_status()
    payload = response.json()

    if "feed" not in payload:
        raise RuntimeError(f"Unexpected API response: {payload}")

    # Return raw feed without filtering
    return payload["feed"]


def save_json(data: list, filename: str):
    """Save Python object as pretty-printed JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Define time window: last 90 days
    now = datetime.now(timezone.utc)
    three_months_ago = now - timedelta(days=90)
    tf = three_months_ago.strftime("%Y%m%dT%H%M")
    tt = now.strftime("%Y%m%dT%H%M")

    # Fetch and save news
    news_feed = fetch_news_sentiment(
        symbol="TSLA",
        limit=1000,
        sort="LATEST",               # default sort by time
        time_from=tf,
        time_to=tt
    )
    output_file = "TSLA_news_3months.json"
    save_json(news_feed, output_file)
    print(f"✅ Downloaded {len(news_feed)} TSLA articles from {tf} to {tt}. Saved to {output_file}.")

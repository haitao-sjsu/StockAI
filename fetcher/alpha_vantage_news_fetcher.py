import requests_cache
from typing import List, Dict
from .base import Fetcher


class AlphaVantageNewsFetcher(Fetcher):
    """
    Fetcher implementation for Alpha Vantage NEWS_SENTIMENT API.
    """
    def __init__(self, api_key: str, session: requests_cache.CachedSession = None):
        self.api_key = api_key
        # Create a cached session: responses are stored in SQLite and expire after 300s
        self._session = session or requests_cache.CachedSession(
            cache_name='av_cache',
            backend='sqlite',
            expire_after=600  # seconds
        )
        self.endpoint = "https://www.alphavantage.co/query"

    def fetch(
        self,
        symbol: str,
        time_from: str,
        time_to: str,
        sortBy: str = "LATEST",
        limit: int = 1000,
    ) -> List[Dict]:
        """
        Fetch raw news sentiment feed for a given stock ticker.

        Args:
            symbol (str): Stock ticker symbol, e.g. "TSLA".
            limit (int): Maximum number of articles to request (up to 1000).
            sort (str): Sort order: "LATEST", "EARLIEST", or "RELEVANCE".
            time_from (str, optional): Start time in "YYYYMMDDTHHMM" UTC format.
            time_to (str, optional): End time in "YYYYMMDDTHHMM" UTC format.

        Returns:
            List[Dict]: Raw news feed items as returned by the API.
        """
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "time_from": time_from.strtime('%Y%m%d') + 'T000000',
            "time_to": time_to.strtime('%Y%m%d') + 'T235959',
            "limit": limit,
            "sort": sortBy,
            "apikey": self.api_key
        }

        resp = self._session.get(self.endpoint, params=params, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
        return payload["feed"]
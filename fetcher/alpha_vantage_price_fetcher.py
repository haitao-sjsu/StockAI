import requests_cache
from typing import Dict, Any
from .base import Fetcher


class AlphaVantagePriceFetcher(Fetcher):
    """
    Fetcher implementation for Alpha Vantage TIME_SERIES_DAILY API.
    """
    def __init__(self, api_key: str, session: requests_cache.CachedSession = None):
        # Inject API key and optional session for HTTP requests
        self.api_key = api_key
        self._session = session or requests_cache.CachedSession(
            cache_name='av_cache',
            backend='sqlite',
            expire_after=600  # seconds
        )
        self.endpoint = "https://www.alphavantage.co/query"

    def fetch(
        self,
        symbol: str,
        outputsize: str = "compact"
    ) -> Dict[str, Any]:
        """
        Fetch daily time series data for a given stock ticker.

        Args:
            symbol (str): Stock ticker symbol, e.g., "TSLA".
            outputsize (str): "compact" for recent 100 days, "full" for full history.

        Returns:
            Dict[str, Any]: Parsed JSON response from Alpha Vantage.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
            "datatype": "json",
            "apikey": self.api_key
        }
        resp = self._session.get(self.endpoint, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if "Time Series (Daily)" not in data:
            raise RuntimeError(f"Unexpected API response: {data}")
        return data

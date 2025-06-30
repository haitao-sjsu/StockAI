import requests_cache
from .base import Fetcher

class NewsAPIFetcher(Fetcher):
    def _init(self, api_key: str, session: requests_cache.CachedSession = None):
        self.api_key = api_key
        # Create a cached session: responses are stored in SQLite and expire after 300s
        self._session = session or requests_cache.CachedSession(
            cache_name='av_cache',
            backend='sqlite',
            expire_after=600  # seconds
        )
        self.end_point = "https://newsapi.org/v2/everything"
    
    def _fetch(self, company_name, time_from, time_to, sortBy='relevancy'):
        """
        Fetch news articles for a given symbol within a specified time range.
        
        :param symbol: The stock symbol to fetch news for.
        :param time_from: Start date in 'YYYY-MM-DD' format.
        :param time_to: End date in 'YYYY-MM-DD' format.
        :param sortBy: Sorting criteria ('relevancy', 'popularity', or 'publishedAt').
        :return: A list of news articles.
        """
        time_from_str = time_from.strftime('%Y-%m-%d') + 'T00:00:00'
        time_to_str = time_to.strftime('%Y-%m-%d') + 'T23:59:59'
         
        params = {
            'language': 'en',
            'q': company_name,
            'from': time_from_str,
            'to': time_to_str,
            'sortBy': sortBy,
            'apiKey': self.api_key
        }
        print(params)        
        response = self._session.get(self.end_point, params=params)
        response.raise_for_status()
        payload = response.json()
        return payload['articles']
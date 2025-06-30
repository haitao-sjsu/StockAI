from fetcher.newsapi_news_fetcher import NewsAPIFetcher
import config

fetcher = NewsAPIFetcher(config.NEWSAPI_API_KEY)

raw_news = fetcher.fetch('RKLB', '2025-06-23T00:00:00', '2025-06-23T23:59:59', 'relevancy')

print(raw_news[0])
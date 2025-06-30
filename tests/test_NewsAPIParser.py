from fetcher.newsapi_news_fetcher import NewsAPIFetcher
from parser.newsapi_news_parser import NewsAPIParser
import config

fetcher = NewsAPIFetcher(config.NEWSAPI_API_KEY)
parser = NewsAPIParser()
raw_news = fetcher.fetch('rocket lab', '2025-06-23T00:00:00', '2025-06-23T23:59:59', 'relevancy')
df_news = parser.parse(raw_news)
print(df_news)
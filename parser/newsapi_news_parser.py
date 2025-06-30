from parser.base import Parser
import pandas as pd

class NewsAPIParser(Parser):
    def _parse(self, raw_news):
        news_list = []
        for entry in raw_news:

            news = {
                'title':entry.get('title'),
                'summary':entry.get('description'),
                'url':entry.get('url'),
                'time_published':entry.get('publishedAt'),
            }

            news_list.append(news)
        return pd.DataFrame(news_list)
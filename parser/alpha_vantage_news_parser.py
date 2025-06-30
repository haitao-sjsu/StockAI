import pandas as pd
from typing import List, Dict, Any
from .base import Parser

class AlphaVantageNewsParser(Parser):
    """
    Parse raw Alpha Vantage NEWS_SENTIMENT feed into standardized records.
    """
    def __init__(self, target_ticker: str):
        self.target_ticker = target_ticker

    def _parse(self, raw_feed: List[Dict[str, Any]]) -> pd.DataFrame:
        # 只专注核心业务逻辑
        print(raw_feed['totalResults'])
        records: List[Dict[str, Any]] = []
        
        for entry in raw_feed:
            # Parse publication time
            time_str = entry.get('time_published')
            if not time_str:
                continue
            dt = pd.to_datetime(time_str, format='%Y%m%dT%H%M%S', errors='coerce')
            if pd.isna(dt):
                continue

            # Extract nested sentiment
            ticker_list = entry.get('ticker_sentiment', []) or []
            if ticker_list:
                matching = [ts for ts in ticker_list if ts.get('ticker') == self.target_ticker]
                if matching:
                    ts0 = matching[0]
                    rel_score = ts0.get('relevance_score')
                    sentiment_score = ts0.get('ticker_sentiment_score')
                    sentiment_label = ts0.get('ticker_sentiment_label')
                else:
                    continue
            else:
                continue
                
            # Normalize numeric values
            try:
                relevance_score = float(rel_score)
            except (TypeError, ValueError):
                relevance_score = 1.0
            try:
                ticker_sentiment_score = float(sentiment_score) if sentiment_score is not None else 0.0
            except (TypeError, ValueError):
                ticker_sentiment_score = 0.0
            if sentiment_label is None:
                sentiment_label = "Neutral"

            # Build standardized record
            record: Dict[str, Any] = {
                'time_published': dt,
                'title': entry.get('title'),
                'summary': entry.get('summary'),
                'url': entry.get('url'),
                'source': entry.get('source'),
                'relevance_score': relevance_score,
                'ticker_sentiment_score': ticker_sentiment_score,
                'ticker_sentiment_label': sentiment_label
            }
            records.append(record)
            
        # Sort by time
        records.sort(key=lambda r: r['time_published'])
        return pd.DataFrame(records)
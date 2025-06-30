# ----- data_loader.py -----
import json
import pandas as pd

def load_prices(path: str) -> pd.DataFrame:
    """Load daily price JSON (Alpha Vantage) into a DataFrame with pct_change."""
    with open(path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    ts = raw.get("Time Series (Daily)", {})
    df = pd.DataFrame.from_dict(ts, orient='index', dtype=float)
    df.rename(
        columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        },
        inplace=True
    )
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df['prev_close'] = df['close'].shift(1)
    df['pct_change'] = (df['close'] / df['prev_close'] - 1) * 100
    return df


import json
import pandas as pd

def load_news(path: str, target_ticker: str = None) -> pd.DataFrame:
    """
    Load news JSON list into a DataFrame with datetime field and numeric relevance.
    Missing relevance_score values default to 1.0.
    Extract relevance_score, ticker_sentiment_score, and ticker_sentiment_label 
    from nested ticker_sentiment for the target_ticker if provided,
    otherwise from first ticker_sentiment or top-level relevance_score.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    records = []
    for entry in data:
        # Parse publication time, expecting format YYYYMMDDThhmmss
        time_str = entry.get('time_published')
        if not time_str:
            raise KeyError("Missing 'time_published' in news data")
        dt = pd.to_datetime(time_str, format='%Y%m%dT%H%M%S')

        # Try to extract relevance_score, ticker_sentiment_score and ticker_sentiment_label from nested ticker_sentiment
        rel_score = None
        sentiment_score = None
        sentiment_label = None
        ticker_list = entry.get('ticker_sentiment', [])
        if ticker_list:
            # If a specific ticker is requested, filter for it
            if target_ticker:
                matching = [ts for ts in ticker_list if ts.get('ticker') == target_ticker]
                if matching:
                    rel_score = matching[0].get('relevance_score')
                    sentiment_score = matching[0].get('ticker_sentiment_score')
                    sentiment_label = matching[0].get('ticker_sentiment_label')
            # Fallback to the first item if no match or no target_ticker
            if rel_score is None:
                rel_score = ticker_list[0].get('relevance_score')
                sentiment_score = ticker_list[0].get('ticker_sentiment_score')
                sentiment_label = ticker_list[0].get('ticker_sentiment_label')
        else:
            # No nested data: use top-level field or default to 1.0
            rel_score = entry.get('relevance_score', 1.0)

        # Ensure numeric and default invalid values to 1.0 for relevance_score
        try:
            rel_score = float(rel_score)
        except (TypeError, ValueError):
            rel_score = 1.0
            
        # Ensure numeric and default invalid values for ticker_sentiment_score
        try:
            sentiment_score = float(sentiment_score) if sentiment_score is not None else 0.0
        except (TypeError, ValueError):
            sentiment_score = 0.0
            
        # Default sentiment_label if not available
        if sentiment_label is None:
            sentiment_label = "Neutral"

        # Assemble a flat record
        record = {
            'time_published': dt,
            'title': entry.get('title'),
            'summary': entry.get('summary'),
            'url': entry.get('url'),
            'source': entry.get('source'),
            'relevance_score': rel_score,
            'ticker_sentiment_score': sentiment_score,
            'ticker_sentiment_label': sentiment_label
            # Add other fields here if needed
        }
        records.append(record)

    # Build DataFrame and sort by publication time
    df = pd.DataFrame(records)
    df.sort_values('time_published', inplace=True)
    return df

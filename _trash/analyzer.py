# ----- analyzer.py -----
from datetime import timedelta
from typing import List, Dict
import pandas as pd

def detect_significant_moves(
    df_prices: pd.DataFrame,
    threshold_pct: float
) -> List[pd.Timestamp]:
    """Return list of dates where |pct_change| >= threshold_pct."""
    mask = df_prices['pct_change'].abs() >= threshold_pct
    return df_prices.index[mask].tolist()


def associate_news(
    dates: List[pd.Timestamp],
    df_news: pd.DataFrame,
    days_before: int,
    relevance_threshold: float
) -> Dict[pd.Timestamp, pd.DataFrame]:
    """
    For each date in dates, select news published within [date-days_before 00:00, date 23:59]
    and with relevance_score >= relevance_threshold.
    Return a dict mapping date to a DataFrame sorted by relevance_score descending
    and then time_published descending.
    """
    association: Dict[pd.Timestamp, pd.DataFrame] = {}
    for date in dates:
        # Start from beginning of the day (days_before) days ago
        start = date - timedelta(days=days_before)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # End at the end of the signal day
        end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Filter by time and relevance threshold
        mask = (
            (df_news['time_published'] >= start) &
            (df_news['time_published'] <= end) &
            (df_news['relevance_score'] >= relevance_threshold)
        )
        # Sort by time_published (latest first)
        df_filtered = df_news.loc[mask].sort_values(
            'time_published',
            ascending=False
        )
        association[date] = df_filtered.reset_index(drop=True)
    return association
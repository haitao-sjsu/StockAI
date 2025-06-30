import pandas as pd
from typing import List


def detect_significant_moves(
    df_prices: pd.DataFrame,
    threshold_pct: float
) -> List[pd.Timestamp]:
    """
    Calculate percentage changes and identify dates where the absolute percentage 
    change meets or exceeds a threshold. Modifies the input DataFrame in-place.

    Args:
        df_prices (pd.DataFrame): DataFrame with 'close' column and datetime index.
                                 Will be modified to include 'pct_change' column.
        threshold_pct (float): Percentage threshold (e.g., 5.0 for 5%).

    Returns:
        List[pd.Timestamp]: List of dates where |pct_change| >= threshold_pct.
    """
    # Calculate percentage changes and add to the original DataFrame
    df_prices['prev_close'] = df_prices['close'].shift(1)
    df_prices['pct_change'] = (df_prices['close'] / df_prices['prev_close'] - 1) * 100
    
    # Find dates with significant moves
    mask = df_prices['pct_change'].abs() >= threshold_pct
    return df_prices.index[mask].tolist()

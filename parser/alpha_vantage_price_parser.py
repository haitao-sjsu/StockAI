# parser/price_parser.py

from typing import Dict, Any
import pandas as pd
from .base import Parser

class AlphaVantagePriceParser(Parser):
    """
    专用于解析 Alpha Vantage 日线 JSON 的解析器。
    """
    def _parse(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        # 复用之前的逻辑
        ts = raw_data.get('Time Series (Daily)', {})
        df = pd.DataFrame.from_dict(ts, orient='index', dtype=float)
        df.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        }, inplace=True)
        df.index = pd.to_datetime(df.index)
        return df

from typing import Any
import pandas as pd
from .base import Parser

class YFinanceParser(Parser):
    """
    专用于解析 YFinance DataFrame 的解析器。
    """
    def _parse(self, df: Any) -> pd.DataFrame:
        # 只专注核心业务逻辑，异常会被基类处理
        df.rename(columns={'Close': 'close'}, inplace=True)
        df.index = pd.to_datetime(df.index)
        return df
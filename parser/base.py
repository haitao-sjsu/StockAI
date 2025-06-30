from abc import ABC, abstractmethod
from typing import Any
import logging

logger = logging.getLogger(__name__)

class Parser(ABC):
    """
    通用解析器抽象基类。
    统一处理异常，子类只需实现 _parse() 方法专注业务逻辑。
    """
    
    def parse(self, raw_data: Any) -> Any:
        """
        解析原始数据，统一异常处理
        
        Args:
            raw_data: 由 Fetcher 拉取到的原始数据
            
        Returns:
            解析后的结构化结果
        """
        try:
            return self._parse(raw_data)
        except Exception as e:
            logger.error(f"{self.__class__.__name__} parse failed: {e}")
            raise
    
    @abstractmethod
    def _parse(self, raw_data: Any) -> Any:
        """
        子类实现的具体解析逻辑，不需要处理异常
        
        Args:
            raw_data: 原始数据
            
        Returns:
            解析后的结构化结果
        """
        pass
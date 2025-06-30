from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
import pandas as pd

class Renderer(ABC):
    """
    Abstract base class for rendering components.
    
    Defines a unified interface with a single entry point for rendering
    complete analysis results including charts, news, and interactions.
    
    This design promotes:
    - Single responsibility: One method handles all rendering
    - Consistency: All renderers provide the same interface
    - Simplicity: Clients only need to call one method
    """
    
    @abstractmethod
    def render_price_chart(
        self, 
        df_prices: pd.DataFrame, 
        signal_dates: List[pd.Timestamp],
        lang: str
    ) -> bool:
        """
        Render the price chart with signal markers.
        
        Args:
            df_prices: DataFrame indexed by date with a 'close' column
            signal_dates: List of significant move dates to mark on the chart
            lang: Language code for UI text
            
        Returns:
            bool: True if chart was rendered successfully, False if no signals found
        """
        pass
        
    @abstractmethod
    def render_llm_analysis(
        self, 
        association: Dict[pd.Timestamp, Dict],
        df_prices: pd.DataFrame,
        lang: str
    ) -> None:
        """
        Render LLM analysis results for each anomaly date.
        
        Args:
            association: Dictionary mapping signal dates to analysis data
            df_prices: DataFrame with price data including calculated percentage changes
            lang: Language code for UI text
        """
        pass
    
    @abstractmethod
    def render_language_selector(self) -> str:
        """
        Render language selector UI component.
        
        Returns:
            str: Selected language code
        """
        pass
    
    @abstractmethod
    def sidebar_controls(self, lang: str) -> Tuple[str, int, float]:
        """
        Render sidebar controls and return user-selected parameters.
        
        Args:
            lang: Language code for UI text
            
        Returns:
            Tuple containing: (symbol, period_days, threshold)
        """
        pass
    
    @abstractmethod
    def render_title(self, lang: str, title: str = None) -> None:
        """
        Render the main title of the application.
        
        Args:
            lang: Language code for UI text
            title: Optional custom title text
        """
        pass

# Example usage:
# from ui.base import Renderer
# 
# class StreamlitRenderer(Renderer):
#     def render_price_chart(self, df_prices, signal_dates):
#         # Create and render interactive chart with plotly
#         # ... implementation details ...
#         
#     def render_llm_analysis(self, association, df_prices):
#         # Render LLM analysis results
#         # ... implementation details ...
# 
# class FlaskRenderer(Renderer):
#     def render_analysis_results(self, fig, df_prices, association):
#         # Return HTML template with embedded chart and news
#         return render_template('analysis.html', 
#                              chart_json=fig.to_json(),
#                              news_data=association)

import config

from fetcher.base import Fetcher
from tests.mock import DummySession
from parser.base import Parser
from analyzer.moves import detect_significant_moves
from analyzer.openai import analyze_news_with_openai
from ui.streamlit_renderer import StreamlitRenderer

import logging

logging.basicConfig(level=logging.INFO)

def run(
    symbol: str,
    period_days: int,
    threshold: float,
    lang: str,
    news_fetcher: Fetcher,
    price_fetcher: Fetcher,
    news_parser: Parser,
    price_parser: Parser,
    render: StreamlitRenderer
):
    """
    Core logic with all dependencies injected.
    """
    # 1. Fetch the price data
    company_name, raw_prices = price_fetcher.fetch(symbol, period_days)
    df_prices = price_parser.parse(raw_prices)

    # 2.1 Detect the signal
    signal_dates = detect_significant_moves(df_prices, threshold)
    
    # 2.2 Render the price chart (with built-in signal validation)
    if not render.render_price_chart(df_prices, signal_dates, lang):
        return  # No signals found, exit early
    
    # 3. Find associate news and get llm results with progress indication
    # First render the analysis header
    render.render_analysis_header(lang)
    
    # Show progress information
    total_signals = len(signal_dates)
    render.show_analysis_progress_info(total_signals, lang)
    
    association = {}
    for signal_date in signal_dates:
        raw_news = news_fetcher.fetch(company_name, signal_date, signal_date)
        df_news = news_parser.parse(raw_news)
        pct_change = df_prices.loc[signal_date]['pct_change']
        llm_analysis = analyze_news_with_openai(df_news, signal_date, pct_change, symbol, lang)
        
        # Render this analysis result
        render.render_single_llm_analysis(signal_date, llm_analysis, pct_change, lang)
        
        association[signal_date] = {
            'news': df_news,
            'llm_analysis': llm_analysis
        }

    # 4. Add separator after all analyses
    render.add_separator()

def main():
    # Create renderer instance first
    render = config.RENDERERS[config.DEFAULT_RENDERER]()
    
    # Render language selector first (in sidebar)
    lang = render.render_language_selector()
    
    # Sidebar controls (language selector is already rendered above)
    symbol, period_days, threshold = render.sidebar_controls(lang)

    # Render the main title with selected language
    render.render_title(lang)
    
    news_fetcher = config.NEWS_FETCHERS[config.DEFAULT_NEWS_FETCHER](api_key=config.NEWSAPI_API_KEY)
    price_fetcher = config.PRICE_FETCHERS[config.DEFAULT_PRICE_FETCHER]()
    
    news_parser = config.NEWS_PARSERS[config.DEFAULT_NEWS_PARSER]()
    price_parser = config.PRICE_PARSERS[config.DEFAULT_PRICE_PARSER]()

    # Run core application with language parameter
    run(
        symbol,
        period_days,
        threshold,
        lang,
        news_fetcher,
        price_fetcher,
        news_parser,
        price_parser,
        render
    )


if __name__ == '__main__':
    main()

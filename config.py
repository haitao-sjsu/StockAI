import os

from dotenv import load_dotenv

# load .env into environment
load_dotenv(override=True)

# --- Configuration ---
MOCK_MODE = False

# --- API Keys ---
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
NEWSAPI_API_KEY=os.getenv('NEWSAPI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# --- OpenAI Configuration ---
OPENAI_MODEL = 'gpt-3.5-turbo'

# --- Fetcher Registry ---
from fetcher.alpha_vantage_news_fetcher import AlphaVantageNewsFetcher
from fetcher.alpha_vantage_price_fetcher import AlphaVantagePriceFetcher
from fetcher.newsapi_news_fetcher import NewsAPIFetcher
from fetcher.yfinance_price_fetcher import YfinanceFetcher

NEWS_FETCHERS = {
    'alpha_vantage': AlphaVantageNewsFetcher,
    'newsapi': NewsAPIFetcher,
    # 'finnhub': FinnhubNewsFetcher,  # Example for future extension
}
DEFAULT_NEWS_FETCHER = 'newsapi'

PRICE_FETCHERS = {
    'alpha_vantage': AlphaVantagePriceFetcher,
    'yfinance': YfinanceFetcher
}
DEFAULT_PRICE_FETCHER = 'yfinance'

# --- Parser Registry ---
from parser.alpha_vantage_news_parser import AlphaVantageNewsParser
from parser.newsapi_news_parser import NewsAPIParser
from parser.base import Parser as NewsParserBase  # for type hints
from parser.base import Parser

NEWS_PARSERS = {
    'alpha_vantage': AlphaVantageNewsParser,
    'newsapi': NewsAPIParser
    # 'finnhub': FinnhubNewsParser,
}
DEFAULT_NEWS_PARSER = 'newsapi'

from parser.base import Parser as PriceParserBase
from parser.alpha_vantage_price_parser import AlphaVantagePriceParser
from parser.yfinance_price_parser import YFinanceParser

PRICE_PARSERS = {
    'alpha_vantage': AlphaVantagePriceParser,
    'yfinance': YFinanceParser
}
DEFAULT_PRICE_PARSER = 'yfinance'

# --- Model Client Registry ---
# import your model clients here when available
# from model.openai_client import OpenAIClient
# from model.local_llm_client import LocalLLMClient

MODEL_CLIENTS = {
    # 'openai': OpenAIClient,
    # 'local': LocalLLMClient,
}
DEFAULT_MODEL_CLIENT = 'openai'

# --- Renderer Registry ---
from ui.streamlit_renderer import StreamlitRenderer
# from visualizer.flask_renderer import FlaskRenderer

RENDERERS = {
    'streamlit': StreamlitRenderer,
    # 'flask': FlaskRenderer,
}
DEFAULT_RENDERER = 'streamlit'

DEFAULT_RELEVANCE_THRESHOLD = 0.3

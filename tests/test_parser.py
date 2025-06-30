import pytest
import json
import pandas as pd
from parser.alpha_vantage_news_parser import AlphaVantageNewsParser
from parser.alpha_vantage_price_parser import AlphaVantagePriceParser

# Test data fixtures

def get_sample_news_data():
    """Return sample news data similar to Alpha Vantage format."""
    return [
        {
            "title": "Tesla Celebrates 1 Million Powerwall Milestone",
            "url": "https://www.benzinga.com/test-article",
            "time_published": "20250603T204801",
            "summary": "Tesla has produced one million Powerwalls in 10 years.",
            "source": "Benzinga",
            "ticker_sentiment": [
                {
                    "ticker": "TSLA",
                    "relevance_score": "0.950184",
                    "ticker_sentiment_score": "0.576245",
                    "ticker_sentiment_label": "Bullish"
                }
            ]
        },
        {
            "title": "Why Shares of Tesla Are Sinking Today",
            "url": "https://www.motleyfool.com/test-article",
            "time_published": "20250604T162431",
            "summary": "Tesla shares are down on delivery concerns.",
            "source": "Motley Fool",
            "ticker_sentiment": [
                {
                    "ticker": "TSLA",
                    "relevance_score": "0.680000",
                    "ticker_sentiment_score": "-0.206000",
                    "ticker_sentiment_label": "Somewhat-Bearish"
                }
            ]
        }
    ]

def get_sample_price_data():
    """Return sample price data similar to Alpha Vantage format."""
    return {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "TSLA",
            "3. Last Refreshed": "2025-06-25",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2025-06-25": {
                "1. open": "342.7100",
                "2. high": "342.8600",
                "3. low": "320.4000",
                "4. close": "327.5500",
                "5. volume": "119283781"
            },
            "2025-06-24": {
                "1. open": "356.1700",
                "2. high": "356.2600",
                "3. low": "340.4400",
                "4. close": "340.4700",
                "5. volume": "114736245"
            }
        }
    }

# Tests for AlphaVantageNewsParser

def test_news_parser_returns_list_correctly():
    """Test that news parser returns a list of parsed records."""
    parser = AlphaVantageNewsParser(target_ticker="TSLA")
    sample_data = get_sample_news_data()
    
    result = parser.parse(sample_data)
    assert isinstance(result, list)
    assert len(result) == 2

def test_news_parser_extracts_fields_correctly():
    """Test that news parser extracts all required fields."""
    parser = AlphaVantageNewsParser(target_ticker="TSLA")
    sample_data = get_sample_news_data()
    
    result = parser.parse(sample_data)
    record = result[0]
    
    # Check all expected fields are present
    expected_fields = [
        'time_published', 'title', 'summary', 'url', 'source',
        'relevance_score', 'ticker_sentiment_score', 'ticker_sentiment_label'
    ]
    for field in expected_fields:
        assert field in record

def test_news_parser_converts_time_correctly():
    """Test that news parser converts time strings to timestamps."""
    parser = AlphaVantageNewsParser(target_ticker="TSLA")
    sample_data = get_sample_news_data()
    
    result = parser.parse(sample_data)
    for record in result:
        assert isinstance(record['time_published'], pd.Timestamp)
        assert not pd.isna(record['time_published'])

def test_news_parser_extracts_sentiment_for_target_ticker():
    """Test that parser correctly extracts sentiment for target ticker."""
    parser = AlphaVantageNewsParser(target_ticker="TSLA")
    sample_data = get_sample_news_data()
    
    result = parser.parse(sample_data)
    
    # First article should have bullish sentiment
    assert result[0]['ticker_sentiment_score'] == 0.576245
    assert result[0]['ticker_sentiment_label'] == "Bullish"
    assert result[0]['relevance_score'] == 0.950184
    
    # Second article should have bearish sentiment
    assert result[1]['ticker_sentiment_score'] == -0.206000
    assert result[1]['ticker_sentiment_label'] == "Somewhat-Bearish"

def test_news_parser_handles_empty_input():
    """Test that news parser handles empty input gracefully."""
    parser = AlphaVantageNewsParser(target_ticker="TSLA")
    
    result = parser.parse([])
    assert result == []

def test_news_parser_skips_invalid_time():
    """Test that parser skips entries with invalid timestamps."""
    parser = AlphaVantageNewsParser(target_ticker="TSLA")
    invalid_data = [
        {
            "title": "Invalid Time Article",
            "time_published": "invalid_date",
            "ticker_sentiment": []
        }
    ]
    
    result = parser.parse(invalid_data)
    assert len(result) == 0  # Should skip invalid entry

# Tests for AlphaVantagePriceParser

def test_price_parser_returns_dataframe_correctly():
    """Test that price parser returns a DataFrame."""
    parser = AlphaVantagePriceParser()
    sample_data = get_sample_price_data()
    
    result = parser.parse(sample_data)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

def test_price_parser_renames_columns_correctly():
    """Test that price parser renames columns correctly."""
    parser = AlphaVantagePriceParser()
    sample_data = get_sample_price_data()
    
    result = parser.parse(sample_data)
    expected_columns = ['open', 'high', 'low', 'close', 'volume', 'prev_close', 'pct_change']
    for col in expected_columns:
        assert col in result.columns

def test_price_parser_converts_index_to_datetime():
    """Test that price parser converts index to datetime."""
    parser = AlphaVantagePriceParser()
    sample_data = get_sample_price_data()
    
    result = parser.parse(sample_data)
    assert isinstance(result.index, pd.DatetimeIndex)

def test_price_parser_sorts_by_date():
    """Test that price parser sorts data by date."""
    parser = AlphaVantagePriceParser()
    sample_data = get_sample_price_data()
    
    result = parser.parse(sample_data)
    assert result.index.is_monotonic_increasing

def test_price_parser_calculates_pct_change():
    """Test that price parser calculates percentage change correctly."""
    parser = AlphaVantagePriceParser()
    sample_data = get_sample_price_data()
    
    result = parser.parse(sample_data)
    
    # First row should have NaN pct_change
    assert pd.isna(result.iloc[0]['pct_change'])
    
    # Second row should have calculated pct_change
    expected_pct = (327.55 / 340.47 - 1) * 100  # (close[1] / close[0] - 1) * 100
    assert abs(result.iloc[1]['pct_change'] - expected_pct) < 0.01
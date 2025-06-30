import pytest
from fetcher.alpha_vantage_news_fetcher import AlphaVantageNewsFetcher
from fetcher.alpha_vantage_price_fetcher import AlphaVantagePriceFetcher

class DummyResponse:
    def __init__(self, payload):
        self._payload = payload
    def raise_for_status(self):
        pass
    def json(self):
        return self._payload

class DummySession:
    def __init__(self, response):
        self._response = response
    def get(self, url, params=None, timeout=None):
        return self._response

# Tests for AlphaVantageNewsFetcher

def test_news_fetcher_returns_feed_correctly():
    # Prepare dummy payload with feed
    payload = {'feed': [{'title': 'Test News'}]}
    session = DummySession(DummyResponse(payload))
    fetcher = AlphaVantageNewsFetcher(api_key='testkey', session=session)

    result = fetcher.fetch(symbol='TSLA', limit=10)
    assert isinstance(result, list)
    assert result == payload['feed']

def test_news_fetcher_raises_on_missing_feed():
    # Payload without 'feed' key
    payload = {'not_feed': []}
    session = DummySession(DummyResponse(payload))
    fetcher = AlphaVantageNewsFetcher(api_key='testkey', session=session)
    with pytest.raises(RuntimeError) as exc:
        fetcher.fetch(symbol='TSLA')
    assert 'Unexpected API response' in str(exc.value)

# Tests for AlphaVantagePriceFetcher

def test_price_fetcher_returns_json_when_key_present():
    # Prepare dummy payload with correct key
    ts_data = {'2021-01-01': {'1. open': '100', '2. high': '110', '3. low': '90', '4. close': '105', '5. volume': '1000'}}
    payload = {'Time Series (Daily)': ts_data}
    session = DummySession(DummyResponse(payload))
    fetcher = AlphaVantagePriceFetcher(api_key='testkey', session=session)

    result = fetcher.fetch(symbol='TSLA', outputsize='compact')
    # Expect the same payload dict
    assert isinstance(result, dict)
    assert 'Time Series (Daily)' in result
    assert result['Time Series (Daily)'] == ts_data

def test_price_fetcher_raises_on_missing_timeseries():
    payload = {'Wrong Key': {}}
    session = DummySession(DummyResponse(payload))
    fetcher = AlphaVantagePriceFetcher(api_key='testkey', session=session)
    with pytest.raises(RuntimeError) as exc:
        fetcher.fetch(symbol='TSLA')
    assert 'Unexpected API response' in str(exc.value)

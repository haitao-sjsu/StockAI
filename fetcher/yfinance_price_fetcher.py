import yfinance as yf
from fetcher.base import Fetcher

class YfinanceFetcher(Fetcher):
    def _init(self, *args, **kwargs):
        pass
    
    def _fetch(self, symbol, period):
        ticker = yf.Ticker(symbol)

        if period == 30:
            hist_data = ticker.history(period='1mo')
        elif period == 7:
            hist_data = ticker.history(period='1mo').tail(7)
        else:
            raise NotImplementedError('only support period 30 days and 7 days')

        info = ticker.info
        company_name = (info.get('displayName') or 
                        info.get('longName') or 
                        info.get('shortName') or 
                        symbol)
                
        return company_name, hist_data

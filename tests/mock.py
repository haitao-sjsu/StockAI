import json


class DummyResponse:
    """模拟 requests.Response 对象"""
    
    def __init__(self, payload):
        self._payload = payload
    
    def raise_for_status(self):
        pass
    
    def json(self):
        return self._payload


class DummySession:
    """模拟 requests.Session，从本地JSON文件返回数据"""
    
    def __init__(self, price_file: str, news_file: str):
        self.price_file = price_file
        self.news_file = news_file
        
        # 预加载数据
        try:
            with open(price_file, 'r', encoding='utf-8') as f:
                self.price_data = json.load(f)
            print(f"✅ Successfully loaded price data from {price_file}")
        except Exception as e:
            print(f"❌ Error loading price data from {price_file}: {e}")
            self.price_data = {}
            
        try:
            with open(news_file, 'r', encoding='utf-8') as f:
                self.news_data = json.load(f)
            print(f"✅ Successfully loaded news data from {news_file}")
        except Exception as e:
            print(f"❌ Error loading news data from {news_file}: {e}")
            self.news_data = {}
    
    def get(self, url, params=None, timeout=None):
        """模拟 requests.get 方法"""
        # 根据参数中的 function 字段决定返回哪种数据
        if params and 'function' in params:
            function = params.get('function', '')
            if function == 'TIME_SERIES_DAILY':
                print(f"📁 [MOCK] Returning price data from {self.price_file}")
                return DummyResponse(self.price_data)
            elif function == 'NEWS_SENTIMENT':
                print(f"📁 [MOCK] Returning news data from {self.news_file}")
                payload = {'feed': self.news_data}
                return DummyResponse(payload)

        # 如果没有匹配的函数，返回空数据
        print(f"⚠️ Unknown function or missing params: {params}")
        return DummyResponse({})

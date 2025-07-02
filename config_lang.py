# Language configurations
LANG_CONFIG = {
    "zh": {
        # Frontend UI text
        "ui": {
            "title": "📊 股票事件关联分析（献给傻妞我老婆）",
            "sidebar_title": "控制面板",
            "stock_symbol": "股票代码",
            "stock_symbol_placeholder": "输入股票代码 (例如: TSLA, AAPL, MSFT)",
            "stock_symbol_help": "输入您要分析的股票代码",
            "analysis_period": "分析周期",
            "price_threshold": "价格变动阈值 (%)",
            "confirm_button": "确认分析",
            "confirm_button_help": "点击确认开始分析",
            "chart_title": "股价走势及异动信号",
            "chart_xaxis": "日期",
            "chart_yaxis": "收盘价",
            "ai_analysis_title": "🤖 AI 异动原因分析",
            "news_details_title": "📰 相关新闻详情",
            "no_signals": "🔍 未检测到显著异动信号。",
            "try_lower_threshold": "💡 尝试降低阈值或选择不同的时间周期。",
            "no_news_threshold": "当天没有符合相关度阈值的新闻。",
            "no_analysis": "暂无 AI 分析结果",
            "news_events": "新闻事件",
            "sentiment": "情绪",
            "relevance": "相关度",
            "read_full_article": "阅读完整文章",
            "no_url_available": "无链接",
            "close_price": "收盘价",
            "signal": "信号",
            "price_change": "涨跌幅",
            "date": "日期",
            "date_format": "%Y年%m月%d日",
            "chart_date_format": "%Y年%m月%d日",
            "hover_date_label": "日期",
            "hover_close_label": "收盘价",
            "hover_change_label": "涨跌幅",
            "hover_date_format": "custom"
        },
        # Backend analysis text
        "no_news": "当天没有相关新闻数据可供分析。",
        "no_api_key": "⚠️ 未配置 OpenAI API Key，无法进行 LLM 分析。请在环境变量中设置 OPENAI_API_KEY。",
        "date_format": "%Y年%m月%d日",
        "direction_up": "上涨",
        "direction_down": "下跌",
        "time_label": "时间",
        "title_label": "标题",
        "summary_label": "摘要",
        "system_instruction": "你是一位专业且谨慎的金融分析师，擅长根据新闻事件分析股价异动原因。你始终坚持基于事实进行分析，绝不编造或推测未在资料中明确提及的信息。当信息不足时，你会诚实地承认无法确定原因。",
        "user_prompt": """请分析以下关于股票 {symbol} 在 {date_str} 的新闻信息。

**重要背景信息**: 股票 {symbol} 在 {date_str} 当天{direction_text}了 {price_change:.2f}%

新闻信息：
{news_text}

请基于以上新闻信息和股价实际变动情况，分析并总结：
1. 可能影响股价的关键事件或消息
2. 这些事件如何解释当天的股价{direction_text}
3. 影响程度的评估

**重要提醒**：
- 请只基于提供的新闻信息进行分析，不要添加未提及的信息
- 如果提供的新闻信息不足以解释股价异动，请诚实说明"根据提供的新闻信息无法确定股价异动的具体原因"
- 不要强行编造或推测未在新闻中明确提及的原因
- 如果新闻内容与股价变动方向不符或关联性较弱，请如实指出

请用简洁明了的中文回答，重点解释为什么股票在当天{direction_text}了 {price_change:.2f}%。如果无法确定原因，请直接说明。""",
        "error_prefix": "LLM 分析失败"
    },
    "en": {
        # Frontend UI text
        "ui": {
            "title": "📊 Stock Event Correlation",
            "sidebar_title": "Controls",
            "stock_symbol": "Stock Symbol",
            "stock_symbol_placeholder": "Enter stock symbol (e.g., TSLA, AAPL, MSFT)",
            "stock_symbol_help": "Enter the stock ticker symbol you want to analyze",
            "analysis_period": "Analysis period",
            "price_threshold": "Price move threshold (%)",
            "confirm_button": "Confirm",
            "confirm_button_help": "Click Confirm to run analysis",
            "chart_title": "Price with Significant Moves",
            "chart_xaxis": "Date",
            "chart_yaxis": "Close Price",
            "ai_analysis_title": "🤖 AI Analysis Results",
            "news_details_title": "📰 Related News Details",
            "no_signals": "🔍 No significant moves detected with the current threshold.",
            "try_lower_threshold": "💡 Try lowering the threshold or selecting a different time period.",
            "no_news_threshold": "No news meets the relevance threshold for this date.",
            "no_analysis": "No AI analysis results available",
            "news_events": "News Events",
            "sentiment": "Sentiment",
            "relevance": "Relevance",
            "read_full_article": "Read full article",
            "no_url_available": "No URL available",
            "close_price": "Close Price",
            "signal": "Signal",
            "price_change": "Price Change",
            "date": "Date",
            "date_format": "%Y-%m-%d",
            "chart_date_format": "%Y-%m-%d",
            "hover_date_label": "Date",
            "hover_close_label": "Close",
            "hover_change_label": "Price Change",
            "hover_date_format": "plotly"
        },
        # Backend analysis text
        "no_news": "No relevant news data available for analysis on this date.",
        "no_api_key": "⚠️ OpenAI API Key not configured. Unable to perform LLM analysis. Please set OPENAI_API_KEY in environment variables.",
        "date_format": "%B %d, %Y",
        "direction_up": "gained",
        "direction_down": "declined",
        "time_label": "Time",
        "title_label": "Title", 
        "summary_label": "Summary",
        "system_instruction": "You are a professional and cautious financial analyst who excels at analyzing stock price movements based on news events. You always adhere to fact-based analysis and never fabricate or speculate on information not explicitly mentioned in the materials. When information is insufficient, you honestly admit that the cause cannot be determined.",
        "user_prompt": """Please analyze the following news information about stock {symbol} on {date_str}.

**Important Context**: Stock {symbol} {direction_text} {price_change:.2f}% on {date_str}

News Information:
{news_text}

Based on the above news information and the actual stock price movement, please analyze and summarize:
1. Key events or messages that may have affected the stock price
2. How these events explain the day's stock price movement
3. Assessment of the impact magnitude

**Important Guidelines**:
- Only base your analysis on the provided news information, do not add information not mentioned
- If the provided news information is insufficient to explain the stock price movement, please honestly state "The provided news information is insufficient to determine the specific cause of the stock price movement"
- Do not fabricate or speculate on reasons not explicitly mentioned in the news
- If the news content does not align with or has weak correlation to the stock price direction, please point this out honestly

Please provide a concise and clear response in English, focusing on explaining why the stock {direction_text} {price_change:.2f}% on that day. If the cause cannot be determined, please state so directly.""",
        "error_prefix": "LLM analysis failed"
    }
}


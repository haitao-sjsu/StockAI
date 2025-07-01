import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from typing import Dict, List, Any, Tuple
from .base import Renderer
import config_ui
from config_lang import LANG_CONFIG

class StreamlitRenderer(Renderer):
    """
    Streamlit-specific implementation of the Renderer interface.
    Renders charts and news/summaries using Streamlit components.
    """
    
    def __init__(self, lang: str = 'en'):
        """
        Initialize renderer with language setting.
        
        Args:
            lang: Language code ('en' or 'zh')
        """
        self.lang = lang
        self.texts = LANG_CONFIG.get(lang, LANG_CONFIG['en'])['ui']

        st.set_page_config(
            page_icon="📈",
            initial_sidebar_state="expanded"  # 👈 这一行控制 sidebar 初始状态
        )
    
    def sidebar_controls(self, lang: str) -> Tuple[str, int, float]:
        """
        Render Streamlit sidebar controls and return user-selected parameters.
        Note: Language selection is now handled separately in render_language_selector.

        Args:
            lang: Language code for UI text
            
        Returns:
            symbol (str): Stock symbol to analyze
            period_days (int): Analysis period in days
            threshold (float): Price move threshold in percent
        """
        texts = LANG_CONFIG.get(lang, LANG_CONFIG['en'])['ui']
        
        st.sidebar.title(texts["sidebar_title"])
        
        # Stock symbol input
        symbol = st.sidebar.text_input(
            texts["stock_symbol"], 
            value=config_ui.DEFAULT_COMPANY, 
            placeholder=texts["stock_symbol_placeholder"],
            help=texts["stock_symbol_help"]
        ).upper().strip()
        
        # Get period options for current language
        period_options = config_ui.get_period_options_for_lang(lang)
        default_period_display = config_ui.PERIOD_OPTIONS[lang][config_ui.DEFAULT_PERIOD]
        
        period_selected = st.sidebar.selectbox(
            texts["analysis_period"], 
            period_options, 
            index=period_options.index(default_period_display)
        )
        
        # Get price move options for current language
        price_move_options = config_ui.get_price_move_options_for_lang(lang)
        default_price_display = config_ui.PRICE_MOVE_OPTIONS[lang][config_ui.DEFAULT_PRICE_MOVE_THRESHOLD]
        
        threshold_selected = st.sidebar.selectbox(
            texts["price_threshold"], 
            price_move_options, 
            index=price_move_options.index(default_price_display)
        )
        
        if not st.sidebar.button(texts["confirm_button"]):
            st.sidebar.write(texts["confirm_button_help"])
            st.stop()

        # Convert selections to internal values
        period_key = config_ui.get_period_key_from_display(period_selected, lang)
        period_days = config_ui.PERIOD_DAYS[period_key]
        threshold_val = config_ui.get_price_move_value_from_display(threshold_selected, lang)
        
        return symbol, period_days, threshold_val

    def render_price_chart(
        self,
        df_prices: pd.DataFrame,
        signal_dates: List[pd.Timestamp],
        lang: str
    ) -> bool:
        """
        Render the price chart with signal markers in Streamlit.
        This method now incorporates the functionality of plot_price_with_signals.

        Args:
            df_prices: DataFrame indexed by date with a 'close' column.
            signal_dates: List of significant move dates to mark on the chart.
            lang: Language code for UI text
            
        Returns:
            bool: True if chart was rendered successfully, False if no signals found.
        """
        texts = LANG_CONFIG.get(lang, LANG_CONFIG['en'])['ui']
        
        # Check if there are any significant moves
        if not signal_dates:
            st.info(texts["no_signals"])
            st.info(texts["try_lower_threshold"])
            return False
        
        # Create the figure
        fig = go.Figure()
        
        # Add closing price line
        fig.add_trace(go.Scatter(
            x=df_prices.index,
            y=df_prices['close'],
            mode='lines',
            name=texts["close_price"]
        ))
        
        # Add markers for each signal date
        for date in signal_dates:
            if date in df_prices.index:
                price = df_prices.at[date, 'close']
                pct_change = df_prices.at[date, 'pct_change']
                
                # Format date display based on language configuration
                date_display = date.strftime(texts["date_format"])
                
                # Create hover template using language-specific labels and format
                if texts["hover_date_format"] == "custom":
                    # For Chinese, use custom formatted date
                    date_text = date_display
                else:
                    # For English, use Plotly's built-in date formatting
                    date_text = "%{x|%Y-%m-%d}"
                
                hovertemplate = (
                    f'{texts["hover_date_label"]}: {date_text}<br>' +
                    f'{texts["hover_close_label"]}: %{{y:.2f}}<br>' +
                    f'{texts["hover_change_label"]}: {pct_change:.2f}%<br>'
                )
                
                fig.add_trace(go.Scatter(
                    x=[date],
                    y=[price],
                    mode='markers',
                    marker=dict(color='red', size=10),
                    name=f'{texts["signal"]} {date_display}',
                    hovertemplate=hovertemplate
                ))
        
        # Update layout with language-specific formatting
        layout_config = {
            'title': texts["chart_title"],
            'xaxis_title': texts["chart_xaxis"],
            'yaxis_title': texts["chart_yaxis"],
            'hovermode': 'closest'
        }
        
        # Add Chinese-specific formatting if needed
        if lang == 'zh':
            layout_config['xaxis'] = dict(
                tickformat=texts["chart_date_format"],
                tickangle=45
            )
        
        fig.update_layout(**layout_config)
        
        # Render the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        return True

    def render_llm_analysis(
        self,
        association: Dict[pd.Timestamp, Dict],
        df_prices,
        lang: str
    ) -> None:
        """
        Render LLM analysis results for each anomaly date.
        
        Args:
            association: Dictionary mapping signal dates to analysis data
            df_prices: DataFrame with price data
            lang: Language code for UI text
        """
        texts = LANG_CONFIG.get(lang, LANG_CONFIG['en'])['ui']
        
        st.subheader(texts["ai_analysis_title"])
        
        for date, data in association.items():
            llm_analysis = data.get('llm_analysis', '')
            if llm_analysis:
                pct_change = df_prices.loc[date]['pct_change']
                change_text = f"{pct_change:.2f}%"
                if lang == 'zh':
                    expander_title = f"📅 {date.date()} 变动{change_text}分析"
                else:
                    expander_title = f"📅 {date.date()} Analysis ({change_text} change)"
                    
                with st.expander(expander_title, expanded=True):
                    st.markdown(llm_analysis)
            else:
                if lang == 'zh':
                    st.info(f"📅 {date.date()}: {texts['no_analysis']}")
                else:
                    st.info(f"📅 {date.date()}: {texts['no_analysis']}")
        
        st.markdown("---")

    def render_news_list(
        self,
        association: Dict[pd.Timestamp, Dict]
    ) -> None:
        """
        Render news items below the chart, including summary, relevance, and sentiment information.
        Since all news for each anomaly date are from the same day, we can simplify the logic.
        """
        st.subheader("📰 相关新闻详情")
        
        for date, data in association.items():
            news_df = data.get('news', pd.DataFrame())
            st.markdown(f"### 📅 {date.date()} 新闻事件")
            
            if news_df.empty:
                st.info("当天没有符合相关度阈值的新闻。")
            else:
                # 直接遍历新闻，无需按日期分组（因为都是同一天的新闻）
                for idx, row in news_df.iterrows():
                    # 使用简单的时间标识
                    time_str = row['time_published']
                    title = str(row.get('title') or "").strip() or "No title"
                    
                    # 新闻标题和时间
                    st.markdown(f"**⏰ {time_str} - {title}**")
                    
                    # 情感和相关度信息
                    sentiment_score = row.get('ticker_sentiment_score', 0.0)
                    sentiment_label = row.get('ticker_sentiment_label', 'Neutral')
                    relevance_score = row.get('relevance_score', 1.0)
                    
                    if sentiment_label.lower() == 'bullish':
                        sentiment_color = "🟢"
                    elif sentiment_label.lower() == 'bearish':
                        sentiment_color = "🔴"
                    else:
                        sentiment_color = "🟡"
                    
                    st.markdown(
                        f"_{sentiment_color} Sentiment: {sentiment_label} ({sentiment_score:.3f}) | "
                        f"Relevance: {relevance_score:.2f}_"
                    )
                    
                    # 新闻摘要
                    st.markdown(f"> {row.get('summary', 'No summary available')}")
                    
                    # 链接
                    url = row.get('url', '')
                    if url:
                        st.markdown(f"🔗 [Read full article]({url})")
                    else:
                        st.markdown("🔗 _No URL available_")
                    
                    st.markdown("---")

    def render_title(self, lang: str, title: str = None) -> None:
        """
        Render the main title of the application.
        
        Args:
            lang: Language code for UI text
            title: Optional custom title text
        """
        texts = LANG_CONFIG.get(lang, LANG_CONFIG['en'])['ui']
        display_title = title if title else texts["title"]
        st.title(display_title)
    
    def render_language_selector(self) -> str:
        """
        Render language selector in the top right corner using flag icons.
        
        Returns:
            str: Selected language code
        """
        # Create columns to position language selector in top right
        col1, col2 = st.columns([5, 1])
        
        with col2:
            # Initialize session state for language if not exists
            if 'selected_language' not in st.session_state:
                st.session_state.selected_language = config_ui.DEFAULT_LANGUAGE
            
            # Language options with flag icons
            language_options = config_ui.LANGUAGES
            
            # Create selectbox for language with custom styling
            current_lang = st.session_state.selected_language
            selected_display = st.selectbox(
                label="🌐 Language",
                options=list(language_options.keys()),
                format_func=lambda x: language_options[x],
                index=list(language_options.keys()).index(current_lang),
                key="language_selector"
            )
            
            # Check if language changed and reset if needed
            if selected_display != st.session_state.selected_language:
                st.session_state.selected_language = selected_display
                # Clear other session state to reset the page (except language)
                keys_to_keep = ['selected_language']
                for key in list(st.session_state.keys()):
                    if key not in keys_to_keep:
                        del st.session_state[key]
                st.rerun()
        
        return st.session_state.selected_language
    
    # ...existing code...

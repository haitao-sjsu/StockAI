# ----- visualizer.py -----
import plotly.graph_objs as go
import streamlit as st
from typing import Dict
import pandas as pd

def plot_price_with_signals(
    df_prices,
    signal_dates,
    association: dict
) -> go.Figure:
    """Plot price line and mark signal_dates as red markers with hover info."""
    fig = go.Figure()
    # Price line
    fig.add_trace(go.Scatter(
        x=df_prices.index,
        y=df_prices['close'],
        mode='lines',
        name='Close Price'
    ))
    # Markers for signals
    for date, news_df in association.items():
        # Prepare custom data with sentiment information
        if not news_df.empty:
            custom_data = []
            for _, row in news_df.iterrows():
                custom_data.append([
                    row['time_published'].strftime('%Y-%m-%d %H:%M:%S'),
                    row.get('relevance_score', 1.0),
                    row.get('ticker_sentiment_score', 0.0),
                    row.get('ticker_sentiment_label', 'Neutral')
                ])
        else:
            custom_data = []
            
        fig.add_trace(go.Scatter(
            x=[date],
            y=[df_prices.at[date, 'close']],
            mode='markers',
            marker=dict(color='red', size=8),
            name=f'Signal {date.date()}',
            customdata=custom_data,
            hovertemplate=
                'Date: %{x|%Y-%m-%d}<br>' +
                'Close: %{y:.2f}<br>' +
                'News count: '+str(len(news_df))+ '<br>' +
                '<extra></extra>'
        ))
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Close Price',
        hovermode='closest'
    )
    return fig



def render_news_cards(
    association: Dict[pd.Timestamp, pd.DataFrame]
) -> None:
    """Render news items below the chart, including summary, relevance, and sentiment information."""
    for date, news_df in association.items():
        st.subheader(f"Events around {date.date()}")
        if news_df.empty:
            st.write("No relevant news found.")
        else:
            # Group articles by date for timeline layout
            current_date = None
            
            for _, row in news_df.iterrows():
                article_date = row['time_published'].date()
                
                # Create columns for timeline layout
                col1, col2 = st.columns([1, 4])  # Left column for date, right for content
                
                with col1:
                    # Show date only when it changes
                    if current_date != article_date:
                        current_date = article_date
                        st.markdown(f"**{article_date.strftime('%Y-%m-%d')}**")
                        st.markdown("🕐")  # Clock indicator
                    else:
                        st.markdown("")  # Empty space to maintain alignment
                        st.markdown("⏰")  # Timeline dot for same-day articles
                
                with col2:
                    # Title with time
                    title = str(row['title']).strip() if row['title'] else "No title"
                    st.markdown(
                        f"**{row['time_published'].strftime('%H:%M:%S')} - {title}**"
                    )
                    
                    # Sentiment and relevance info
                    sentiment_score = row.get('ticker_sentiment_score', 0.0)
                    sentiment_label = row.get('ticker_sentiment_label', 'Neutral')
                    relevance_score = row.get('relevance_score', 1.0)
                    
                    # Color code sentiment label
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
                    # Summary as blockquote
                    st.markdown(
                        f"> {row.get('summary', 'No summary available')}"
                    )
                    # URL as clickable link
                    url = row.get('url', '')
                    if url:
                        st.markdown(f"🔗 [Read full article]({url})")
                    else:
                        st.markdown("🔗 _No URL available_")
                    
                    # Add some spacing between articles
                    st.markdown("---")
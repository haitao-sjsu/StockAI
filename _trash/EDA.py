# ----- news_source_analysis.py -----
import json
from collections import Counter
import pandas as pd

def analyze_tsla_news():
    """Simple analysis of TSLA news sources."""
    
    # Load the news data
    with open('TSLA_news_3months.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    print("=== TSLA News Summary ===")
    print(f"Total articles: {len(news_data)}")
    print()
    
    # Extract basic info
    sources = [article.get('source', 'Unknown') for article in news_data]
    categories = [article.get('category_within_source', 'Unknown') for article in news_data]
    
    # Count and display top sources
    source_counts = Counter(sources)
    print("Top News Sources:")
    print("-" * 30)
    for source, count in source_counts.most_common(10):
        percentage = (count / len(news_data)) * 100
        print(f"{source:<20} {count:>3} ({percentage:4.1f}%)")
    
    print()
    print("Top Categories:")
    print("-" * 30)
    category_counts = Counter(categories)
    for category, count in category_counts.most_common(10):
        percentage = (count / len(news_data)) * 100
        print(f"{category:<20} {count:>3} ({percentage:4.1f}%)")
    
    print()
    print("Summary:")
    print("-" * 30)
    print(f"Unique sources: {len(source_counts)}")
    print(f"Unique categories: {len(category_counts)}")

def find_earliest_news_date():
    """Find and display the earliest date in the TSLA news data."""
    
    # Load the news data
    with open('TSLA_news_3months.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    print("=== TSLA News Date Analysis ===")
    print(f"Total articles: {len(news_data)}")
    print()
    
    # Extract dates and convert to datetime
    dates = []
    for article in news_data:
        time_str = article.get('time_published')
        if time_str:
            # Convert from format YYYYMMDDThhmmss to datetime
            dt = pd.to_datetime(time_str, format='%Y%m%dT%H%M%S')
            dates.append(dt)
    
    if dates:
        earliest_date = min(dates)
        latest_date = max(dates)
        print("Date Range:")
        print("-" * 40)
        print(f"Earliest article: {earliest_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Latest article:   {latest_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Time span:        {(latest_date - earliest_date).days} days")
        
        return earliest_date, latest_date
    else:
        print("No valid dates found in the data")
        return None, None

if __name__ == "__main__":
    # Run the original analysis
    # analyze_tsla_news()
    find_earliest_news_date()

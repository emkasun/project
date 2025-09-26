import feedparser
import pandas as pd
from datetime import datetime

def parse_rss_feed():
    url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    feed = feedparser.parse(url)

    rss_data = []
    for entry in feed.entries:
        # Extract publication date and standardize it
        published_dt = datetime(*entry.published_parsed[:6]) # Convert parsed time to datetime object
        published_str = published_dt.strftime("%Y-%m-%d %H:%M:%S") # Standard format

        rss_data.append({
            'Title': entry.title,
            'Published_Date': published_str,
            'Summary': entry.summary,
            'Link': entry.link,
            'Source': 'NYT_RSS'
        })

    df = pd.DataFrame(rss_data)
    df.to_csv('../raw_data/rss_raw.csv', index=False)
    print(f"Parsed {len(df)} RSS entries. Data saved to 'raw_data/rss_raw.csv'.")

if __name__ == '__main__':
    parse_rss_feed()
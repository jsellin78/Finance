import time
import feedparser
import pytz
from dateutil.parser import parse

urls = [
    'https://www.forexlive.com/feed/',
    'https://www.dailyfx.com/feeds/market-news', 
    'http://rss.cnn.com/rss/edition_world.rss'# add more URLs here
]

def get_latest_news():
    latest_news = []

    for url in urls:
        NewsFeed = feedparser.parse(url)
        if NewsFeed.entries:
            entry = NewsFeed.entries[0]
            dt = parse(entry.published)
            dt = dt.astimezone(pytz.timezone('Europe/Stockholm')) # Convert pubdate to Swedish date
            dt_formatted = dt.strftime('%Y-%m-%d %H:%M')  
            latest_news.append((entry.title, dt, dt_formatted))
        else:
            print(f"No entries found in feed: {url}")
            latest_news.append((None, None, None))

    return latest_news

def check_keywords(headline, keywords):
    return [keyword for keyword in keywords if keyword.lower() in headline.lower()]

def monitor_feed():
    keywords = ['', '', '', '', '', '']  # Update this list with keywords you are interested in. 
    last_headlines = [None] * len(urls)

    while True:
        current_headlines = get_latest_news()
        
        for i, (current_headline, published_date, dt_formatted) in enumerate(current_headlines):
            if current_headline and current_headline != last_headlines[i]:
                print(f'New headline: {current_headline} {dt_formatted}')
               # print(f'Published at: {dt_formatted}')
                matching_keywords = check_keywords(current_headline, keywords)
                if matching_keywords:
                    print(f'Matching keywords: {matching_keywords}')
                last_headlines[i] = current_headline

        time.sleep(60)  # wait for 60 seconds

monitor_feed()

import time
import feedparser
import pytz
from dateutil.parser import parse
from datetime import datetime, timedelta

urls = [
    'https://www.forexlive.com/feed/',
    'https://www.dailyfx.com/feeds/market-news', 
    'https://www.myfxbook.com/rss/forex-economic-calendar-events',
    'https://www.myfxbook.com/rss/latest-forex-news',
    'http://feeds.bbci.co.uk/news/world/rss.xml',
    'http://feeds.bbci.co.uk/news/business/rss.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
    'https://feeds.npr.org/1006/rss.xml',
    'http://feeds.marketwatch.com/marketwatch/topstories/',
    'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'https://www.forbes.com/investing/feed/',
    'https://finance.yahoo.com/news/rssindex',
    'http://feeds.feedburner.com/zerohedge/feed',
    'https://www.theguardian.com/uk/business/rss',
    'http://feeds2.feedburner.com/businessinsider',
    'https://www.ft.com/rss/home/uk',
    ]

def get_latest_news():
    latest_news = []

    for url in urls:
        NewsFeed = feedparser.parse(url)
        if NewsFeed.entries:
            entry = NewsFeed.entries[0]
            try:
                dt = parse(entry.published)
            except AttributeError:
                try:
                    dt = parse(entry.pubDate)
                except AttributeError:
                    print(f"No published date found in entry: {entry.title} from URL: {url}")
                    dt = None

            if dt is not None:
                dt = dt.astimezone(pytz.timezone('Europe/Stockholm'))  # Convert pubdate to Swedish date
                dt_formatted = dt.strftime('%Y-%m-%d %H:%M')
            else:
                dt_formatted = None

            latest_news.append((entry.title, dt, dt_formatted, entry.link))

        else:
            print(f"No entries found in feed: {url}")
            latest_news.append((None, None, None, url))

    return latest_news


def check_keywords(headline, keywords):
    return [keyword for keyword in keywords if keyword.lower() in headline.lower()]


def check_excluded_keywords(headline, excluded_keywords):
    return any(keyword.lower() in headline.lower() for keyword in excluded_keywords)

def monitor_feed():
    keywords = ['g7 summit',
                'US Debt',
                'recession',
                'intervention',
                'speaking',
                'inflation',
                'ukraine',
                'ugly',
                'outlook',
                'retracement',
                'russia',
                'sharply',
                'stimulus',
                'record',
                'sentiment',
                'price stability',
                'talks stall',
                'retail sales', 
                'business sentiment',
                'GDP',
                'CPI',
                'Consumer Price Index',
                'Employment',
                'Interest Rate Decision',
                'stability',
                'FOMC',
                'ECB',
                'BOE',
                'RBA',
                'RBNZ',
                'BOC',
                'BOJ',
                'SNB',
                'Fed',
                'Pboc',

    ]  # Update this list with keywords you are interested in.

    excluded_keywords = ['keyword1',
                         'keyword2'
    ]

    last_headlines = [None] * len(urls)

    while True:
        current_headlines = get_latest_news()
        
        for i, (current_headline, published_date, dt_formatted, url) in enumerate(current_headlines):
            if current_headline and current_headline != last_headlines[i]:
               current_time = datetime.now(pytz.timezone('Europe/Stockholm'))  
               if published_date is not None:
                      time_diff = current_time - published_date
                      if time_diff <= timedelta(minutes=30):  # Check if the news is less than 30 minutes old, if it is then print it 
                          if not check_excluded_keywords(current_headline, excluded_keywords):  # Only print if the headline doesn't contain excluded keywords
                             print(f'New headline: {current_headline} {dt_formatted} \033]8;;{url}\007Link\033]8;;\007')
                             matching_keywords = check_keywords(current_headline, keywords)
                             if matching_keywords:
                                 print(f'Matching keywords: {matching_keywords}')
            last_headlines[i] = current_headline

        time.sleep(10)  # wait for 10 seconds, before checking agen. 

monitor_feed()

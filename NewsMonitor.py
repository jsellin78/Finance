import sys
import time
import feedparser
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from bs4 import BeautifulSoup
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from dateutil.parser import parse
import pytz
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QMessageBox, QWidget, QDialog, QTextBrowser, QPushButton, QInputDialog
import html
import re
import psycopg2
from psycopg2 import Error
from DatabaseManager import DatabaseManager
import warnings 

warnings.filterwarnings("ignore", category=UserWarning, module='beautifulsoup4')


class NewsMonitor(QThread):
    new_headline = pyqtSignal(str, str, str, str)

    def __init__(self, database_manager):
        super(NewsMonitor, self).__init__()
        self.database_manager = database_manager  # Save the database manager to a class variable
        self.urls = [ 
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
            'https://www.investing.com/rss/news.rss',
            'https://news.google.com/rss?topic=b&hl=en-US&gl=US&ceid=US:en',
            'https://www.investing.com/rss/news_1.rss',
            'https://abcnews.go.com/abcnews/moneyheadlines',
            'https://ch2rss.fflow.net/therussianmarket',
            'https://ch2rss.fflow.net/wewewesdadasd',
            'https://feeds.simplecast.com/54nAGcIl',
            'https://cdn.feedcontrol.net/8/1114-wioSIX3uu8MEj.xml',
            'https://www.huffpost.com/section/world-news/feed',
            'https://www.reutersagency.com/en/reutersbest/reuters-best-rss-feeds/rss',
            'https://nitter.net/kathylienfx/rss',
            'https://nitter.net/liveSquawk/rss',
            'https://nitter.net/FirstSquawk/rss',
            'https://nitter.net/Deltaone/rss',
            'https://nitter.net/RobinBrooksiif/rss',
        ]
        self.keywords = [
            'g7 summit',
            'us debt',  
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
            'sentiment',
            'price stability',
            'talks stall',
            'retail sales', 
            'business sentiment',
            'gdp',  
            'cpi',  
            'consumer price index',  
            'employment',  
            'interest rate decision',  
            'stability',
            'fomc',  
            'ecb',  
            'boe',  
            'rba',  
            'rbnz',  
            'boc',  
            'boj',
            'snb',  
            'fed',  
            'pboc', 
            'government',
            'goverment',
            'debt limit', 
            'legalizing',
            'monetary',
            'monetary policy',
            'preparing',
            'hike',
            'hiking',
            'deal',
            'what to watch',
            'race',
            'increase',
            'rate decision',
            'reassured',
            'cooperate',
        ]
        self.excluded_keywords = [
            # Your excluded keywords here
        ]
        self.interesting_articles = {}
        self.last_headlines = [None] * len(self.urls)

      

    def mark_article(self, title, description):
        self.interesting_articles[title] = description
    

    def show_articles(self):
        return self.interesting_articles


    def mark_article_with_dt(self, title, description, dt):  # New method
        self.interesting_articles[title] = (description, dt)  # Save dt along with description

    def sort_articles(self):
        self.interesting_articles = dict(sorted(self.interesting_articles.items(), key=lambda item: item[1][1]))
    # ...


    def run(self):
        while True:
            self.monitor_feed()
            time.sleep(60)

    def monitor_feed(self):
        for url in self.urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = BeautifulSoup(entry.title, "html.parser").get_text()
                if hasattr(entry, 'published'):
                   # Parse the date and convert it to the Swedish locale
                    dt = parse(entry.published)
                    dt = dt.astimezone(pytz.timezone('Europe/Stockholm'))  # Convert date to Swedish timezone
                    pubdate = dt.strftime('%Y-%m-%d %H:%M')

                description = ''
                if hasattr(entry, 'description'):
                    description = BeautifulSoup(entry.description, "html.parser").get_text()

                for keyword in self.keywords:
                    if keyword in title.lower() or keyword in description.lower():
                        if title not in self.interesting_articles:
                            self.new_headline.emit(pubdate, title, description, pubdate)
                            self.mark_article(title, description)
                            self.mark_article_with_dt(title, description, dt)  # Mark article with datetime
                            try:
                               self.database_manager.save_interesting_article(pubdate, title, description)
                            except Exception as e:
                                print("Error")
                for excluded in self.excluded_keywords:
                    if excluded in title.lower() or excluded in description.lower():
                        if title in self.interesting_articles:
                            del self.interesting_articles[title]

                            

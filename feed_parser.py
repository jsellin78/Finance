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
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QMessageBox, QWidget, QDialog, QTextBrowser
import html
import re
import psycopg2

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="192.168.1.220:220",
    database="interesting_articles",
    user="john",
    password="***"
)

# Create a cursor object
cur = conn.cursor()

# Create a new table to store interesting articles
cur.execute("""
    CREATE TABLE IF NOT EXISTS interesting_articles (
        date TEXT,
        headline TEXT,
        description TEXT
    )
""")

conn.commit()

class NewsMonitor(QThread):
    new_headline = pyqtSignal(str, str, str)

    def __init__(self):
        super(NewsMonitor, self).__init__()
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

    def run(self):
        while True:
            self.monitor_feed()
            time.sleep(10)

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
                            self.new_headline.emit(pubdate, title, description)
                            self.mark_article(title, description)

                for excluded in self.excluded_keywords:
                    if excluded in title.lower() or excluded in description.lower():
                        if title in self.interesting_articles:
                            del self.interesting_articles[title]


class MyWindow(QMainWindow):
    def __init__(self, monitor):
        super(MyWindow, self).__init__()
        self.monitor = monitor
        self.monitor.new_headline.connect(self.add_headline)
        self.monitor.start()
        self.setAppStyle()

        # Create QTreeWidget
        self.tree = QTreeWidget()
        #self.tree.setColumnCount(2)
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Date", "Headlines", "Description"])

        # Set Column Width 
        self.tree.setColumnWidth(0, 200) # for headline
        self.tree.setColumnWidth(1, 120) # for date
        self.tree.setColumnWidth(2, 400) # for description
        # Create and set layout to place widgets

        self.textBrowser = QTextBrowser()
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.current_item_index = 0
        self.tree.itemSelectionChanged.connect(self.update_current_item_index)


    def save_interesting_article(self):
        item = self.tree.currentItem()
        if item:
            date = item.text(0)
            headline = item.text(1)
            description = item.text(2)

            cur.execute("""
                INSERT INTO interesting_articles (date, headline, description)
                VALUES (%s, %s, %s)
            """, (date, headline, description))

            conn.commit()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Space:
            self.save_interesting_article()
        elif event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            self.open_article_dialog()

    def update_current_item_index(self):
         selected_items = self.tree.selectedItems()
         if selected_items:  # if there is a selection
            item = selected_items[0]  # get the first selected item
            self.current_item_index = self.tree.indexOfTopLevelItem(item)  # update the current item index           

    def open_article_dialog(self):
        articles = [(item.text(0), item.text(1), item.text(2)) for item in self.get_all_tree_items()]
        self.dialog = ArticleDialog(self, articles, self.monitor.keywords, self.current_item_index)
        self.dialog.show()         


    def get_all_tree_items(self):
        return [self.tree.topLevelItem(i) for i in range(self.tree.topLevelItemCount())]


    def setAppStyle(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0)) # Change background color to black
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255)) # Change text color to white
        self.setStyleSheet("background-color: black; color: white;")
        self.setPalette(palette)   

    def add_headline(self, date, headline, description):
        description = ' '.join(description.split())  # Remove extra spaces

        font = QFont()
        font.setPointSize(10)  # Set font size

        brush = QBrush()

        # Check if any keyword is in the headline or description
        if any(keyword.lower() in headline.lower() or keyword.lower() in description.lower() for keyword in self.monitor.keywords):
           brush.setColor(QColor(255, 0, 0))  # Set text color to red for matching keywords
        else:
            brush.setColor(QColor(0, 0, 0))  # Set text color to black

        item = QTreeWidgetItem([date, headline, description])
        item.setFont(0, font)
        item.setFont(1, font)
        item.setFont(2, font)  # Set font for description

        item.setForeground(0, brush)
        item.setForeground(1, brush)
        item.setForeground(2, brush)  # Apply brush to description

        # Add the item to the tree after setting the color
        self.tree.addTopLevelItem(item)
        index = self.tree.indexOfTopLevelItem(item)
        self.tree.takeTopLevelItem(index)
        self.tree.insertTopLevelItem(index, item)


class ArticleDialog(QDialog):
    def __init__(self, parent, articles, keywords, current_article_index):
        super().__init__(parent)
        self.articles = articles
        self.keywords = keywords 
        self.current_article_index = current_article_index
        

        self.textBrowser = QTextBrowser()
        layout = QVBoxLayout()
        layout.addWidget(self.textBrowser)
        self.setLayout(layout)

        self.display_current_article()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() in [Qt.Key_J, Qt.Key_Enter, Qt.Key_Return]:
            self.current_article_index += 1
            if self.current_article_index >= len(self.articles):
               self.current_article_index = 0  # Wrap around
        elif event.key() in [Qt.Key_K]:
              self.current_article_index -= 1
              if self.current_article_index < 0:
                 self.current_article_index = len(self.articles) - 1  # Wrap around

        self.display_current_article()

    def display_current_article(self):
        if self.articles:
            date, title, description = self.articles[self.current_article_index]

            # Highlight keywords in red
            for keyword in self.keywords:
                if keyword.lower() in title.lower():
                    title = re.sub(keyword, f'<span style="color: red;">{keyword}</span>', title, flags=re.IGNORECASE)
                if keyword.lower() in description.lower():
                    description = re.sub(keyword, f'<span style="color: red;">{keyword}</span>', description, flags=re.IGNORECASE)
                     
            content = f"Article {self.current_article_index + 1}/{len(self.articles)}\n\n"
            content += f"Date: {date}<br>Title: {title}<br><br>Description: {description}"
            self.textBrowser.setHtml(content)
           # self.textBrowser.setHtml(f"Date: {date}<br>Title: {title}<br><br>Description: {description}")

app = QApplication(sys.argv)
monitor = NewsMonitor()
window = MyWindow(monitor)
window.show()

app.exec_()

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

class ArticleDialog(QDialog):
    def __init__(self, parent, articles, keywords, current_article_index):
        super().__init__(parent)
        self.articles = articles
        self.keywords = keywords 
        self.current_article_index = current_article_index
       
        # Create a button to go to the latest article
        self.latest_button = QPushButton('Go to the latest article')
        self.latest_button.clicked.connect(self.go_to_latest)

        self.textBrowser = QTextBrowser()
        layout = QVBoxLayout()
        layout.addWidget(self.textBrowser)
        layout.addWidget(self.latest_button)  # Add the button to the layout
        self.setLayout(layout)
        self.display_current_article()

    def go_to_latest(self):
        self.current_article_index = len(self.articles) - 1  # Set the current index to the last article
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

    def get_selected_article(self):
        article_date, article_title, article_description = self.articles[self.current_article_index]
        return article_date, article_title, article_description

        


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


class DatabaseManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="192.168.1.220",
            port="5432",
            database="interesting_articles",
            user="john",
            password="john93"
        )
        self.cur = self.connection.cursor()  # Use self.cur, not self.database_manager.cur
        self.create_tables()

    def get_article_content(self, folder_name, article_title):
        try:
            self.cur.execute("""
                SELECT description
                FROM articles
                JOIN folders ON articles.folder_id = folders.id
                WHERE folders.name = %s AND articles.title = %s
            """, (folder_name, article_title))
            article_content = self.cur.fetchone()
            if article_content:
                return article_content[0]
        except psycopg2.Error as e:
            print(f"An error occurred while retrieving article content: {e}")
        return ""



    def delete_all_articles(self):
       try:
          self.cur.execute("DELETE FROM interesting_articles")
          deleted_articles = self.cur.rowcount  # Get the number of deleted rows
          self.connection.commit()
          print(f"Deleted {deleted_articles} articles.")  # Debug print statement
       except psycopg2.Error as e:
           print(f"An error occurred while deleting all articles: {e}")


    def delete_article(self, article_title):
       try:
          query = """
          DELETE FROM articless WHERE title = %s;
          """
          cursor = self.connection.cursor()
          cursor.execute(query, (article_title,))
          self.connection.commit()
          cursor.close()
          print(f"Article with title '{article_title}' deleted")
       except Error as e:
           print("Error while connecting to PostgreSQL", e)
           self.connection.rollback()

    def create_tables(self):
        folders_table_sql = """
        CREATE TABLE IF NOT EXISTS folders (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """
        articles_table_sql = """
        CREATE TABLE IF NOT EXISTS articless (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,  
            folder_id INTEGER REFERENCES folders(id)
        );
        """
        article_folders_table_sql = """
        CREATE TABLE IF NOT EXISTS article_folders (
            article_id INTEGER REFERENCES articles(id),
            folder_id INTEGER REFERENCES folders(id),
            PRIMARY KEY(article_id, folder_id)
        );
        """
        interesting_articles_table_sql = """
        CREATE TABLE IF NOT EXISTS interesting_articles (
            date TEXT,
            headline TEXT,
            description TEXT
        )
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            folder_id INTEGER NOT NULL,
            date DATE NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (folder_id) REFERENCES folders(id)
        );
        """
        self.cur.execute(folders_table_sql)  # Use self.cur, not self.database_manager.cur
        self.cur.execute(articles_table_sql)  # Use self.cur, not self.database_manager.cur
        self.cur.execute(article_folders_table_sql)  # Use self.cur, not self.database_manager.cur
        self.cur.execute(interesting_articles_table_sql)  # Use self.cur, not self.database_manager.cur
        self.cur.execute(create_table_query)  # Use self.cur, not self.database_manager.cur
        self.connection.commit()  # Use self.conn, not self.database_manager.conn

    def save_interesting_article(self, date, headline, description):
        try:
            self.cur.execute("""
                INSERT INTO interesting_articles (date, headline, description)
                VALUES (%s, %s, %s)
            """, (date, headline, description))

            self.connection.commit()  # Use self.conn, not self.database_manager.conn
        except Exception as e:
            print(f"Exception occurred: {e}")

    def show_all_articles(self):
        self.cur.execute("SELECT date, headline, description FROM interesting_articles")
        all_articles = self.cur.fetchall()

        return all_articles

    def fetch_articles(self):
       try:
          self.cur.execute("SELECT date, headline, description FROM interesting_articles")
          all = self.cur.fetchall()
          return all
       except psycopg2.Error as e:
           print(f"An error occurred: {e}")
           return []


    def get_all_folders(self):
        try:
           self.cur.execute("SELECT id, name FROM folders ORDER BY name")
           rows = self.cur.fetchall()
           return rows
        except (Exception, psycopg2.Error) as error:
            print("Error in operation", error)
            self.connection.rollback()  # Rollback the transaction

    def get_articles_in_folder(self, folder_id):
        self.cur.execute("SELECT id, title FROM articless WHERE folder_id = %s ORDER BY title", (folder_id,))  # Use self.cur, not self.database_manager.cur
        articless = self.cur.fetchall()  # Use self.cur, not self.database_manager.cur
        print(f"There are {len(articless)} articles in the folder with id {folder_id}.")
        return articless

    def add_new_folder(self, folder_name):
        folder_id = None
        try:
           cursor = self.connection.cursor()
           insert_query = """INSERT INTO folders (name) VALUES (%s) RETURNING id;"""  # Use the correct table name "folders"
           cursor.execute(insert_query, (folder_name,))
           folder_id = cursor.fetchone()[0]  # Fetch the returned id
           self.connection.commit()  # committing the transaction
           cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Failed inserting record into folder table", error)
            self.connection.rollback()  # rolling back the transaction in case of an error
        return folder_id      


    def save_article_to_folder(self, title, description, date, folder_id):
       try:
          print("title:", title)
          print("Description:", description)
          print("Date:", date)
          print("folder id:", folder_id)
          query = """
          INSERT INTO articless (title, description, date, folder_id) 
          VALUES (%s, %s, %s, %s);
          """
          cursor = self.connection.cursor()
          cursor.execute(query, (title, description, date, int(folder_id)))
          self.connection.commit()
          cursor.close()
       except Error as e:
           print("Error while connecting to PostgreSQL", e)
           self.connection.rollback()

    def show_all_folders(self, tree):
       try:
           self.cur.execute("SELECT id, name FROM folders ORDER BY name")
           all_folders = self.cur.fetchall()

           # Clear existing items in the tree widget
           tree.clear()

           for folder_id, folder_name in all_folders:
               folder_item = QTreeWidgetItem([folder_name])
               folder_item.setData(0, Qt.UserRole, folder_id)

                # Get articles for this folder
               folder_articles = self.get_articles_in_folder(folder_id)

               # Add articles to the folder_item
               for article_id, article_title in folder_articles:
                   article_item = QTreeWidgetItem([str(article_id), article_title])
                   folder_item.addChild(article_item)

               tree.addTopLevelItem(folder_item)

            # Expand all folders
           tree.expandAll()

       except (Exception, psycopg2.Error) as error:
           print("Error in operation", error)
           self.connection.rollback()   
  

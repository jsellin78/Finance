#from PyQt5.QtWidgets import QApplication, QMainWindow
from DatabaseManager import DatabaseManager
from NewsMonitor import NewsMonitor
from ArticleDialog import ArticleDialog
from FolderWidget import FolderWidget
import sys
import time
import feedparser
import html
import re
import psycopg2
from psycopg2 import Error
from dateutil.parser import parse
import pytz
from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt, QThread, pyqtSignal 
from PyQt5.QtGui import QColor, QBrush, QPalette, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QMessageBox, QWidget, QDialog, QTextBrowser, QPushButton, QInputDialog, QTextBrowser, QLineEdit, QFontDialog, QVBoxLayout, QWidget, QGridLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QAbstractItemView

from FolderWidget import FolderWidget
from FolderWidget import FolderWindow
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon


class MyWindow(QMainWindow):
    def __init__(self, monitor, database_manager):
        super(MyWindow, self).__init__()
        self.monitor = monitor
        self.database_manager = database_manager 
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel('Articles')
        self.target_tree = DropTreeWidget(self)
        self.target_tree.setHeaderLabel('Folders')
        self.target_tree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.target_tree.setFocusPolicy(Qt.StrongFocus)
        widget = QWidget()
        button_layout = QHBoxLayout()  # New QHBoxLayout for buttons
        main_layout = QVBoxLayout()
        layout = QHBoxLayout()  # New QHBoxLayout for buttons
        layout.addWidget(self.target_tree)
        layout.addWidget(self.tree)
        layout.setStretchFactor(self.target_tree, 1)  # Bigger factor, bigger size
        layout.setStretchFactor(self.tree, 2)  # Smaller factor, smaller size
#        self.target_tree.customContextMenuRequested.connect(self.create_context_menu)
       # self.target_tree.itemPressed.connect(self.display_article)
##        self.target_tree.itemClicked.connect(self.display_article)
     #   self.folder_widget = FolderWidget(self, database_manager)
        self.folder_widget = FolderWidget(self, database_manager)
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Date", "Headlines", "Description"])

        self.setWindowTitle("Folders")
        # Set Column Width 
        self.tree.setColumnWidth(0, 200) # for headline
        self.tree.setColumnWidth(1, 120) # for date
        self.tree.setColumnWidth(2, 400) # for description

        self.target_tree.setColumnCount(3)
        self.target_tree.setHeaderLabels(["Date", "Headlines"])

        self.target_tree.setColumnWidth(0, 200) # for headline
        self.target_tree.setColumnWidth(1, 120) # for date

        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree.setDragEnabled(True)
        self.tree.setDropIndicatorShown(True)

        self.target_tree.setDragEnabled(True)
        self.target_tree.setAcceptDrops(True)
        self.target_tree.setDropIndicatorShown(True)
        self.target_tree.setDragDropMode(QAbstractItemView.DropOnly)
        self.target_tree.customContextMenuRequested.connect(self.contextMenuEvent)
     #   self.target_tree.customContextMenuRequested.connect(self.DelArt)

        self.tree.setSortingEnabled(True)

        self.monitor.new_headline.connect(self.add_headline)
        self.monitor.start()
        self.setAppStyle()

        self.tray_icon = QSystemTrayIcon(self)
#        self.tray_icon.setIcon(self.notification_icon)
        self.tray_icon.setVisible(True)

        self.target_tree.set_main_window(self)
        self.new_folder_button = QPushButton('New folder')
        self.new_folder_button.setFixedSize(100, 50)

        self.new_folder_button.clicked.connect(self.create_new_folder)
        button_layout.addWidget(self.new_folder_button)

        self.show_all_folders_button = QPushButton('Show all folders')
        self.show_all_folders_button.setFixedSize(100, 50)
        self.show_all_folders_button.clicked.connect(self.show_all_folders)
        button_layout.addWidget(self.show_all_folders_button)


        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedSize(100, 50)
        self.delete_button.clicked.connect(self.delete_article_button_clicked)
        button_layout.addWidget(self.delete_button)
     #   self.delete_button.clicked.connect(self.delete_article_button_clicked)
     #   button_layout.addWidget(self.delete_button)

#        self.show_all_button = QPushButton('Show all articles')
 #       self.show_all_button.setFixedSize(100, 50)
 #       self.show_all_button.clicked.connect(self.show_all_articles)
 #       button_layout.addWidget(self.show_all_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

#LALAL
        self.current_item_index = 0
        self.tree.itemSelectionChanged.connect(self.update_current_item_index)
        folders = self.load_folders()  # Get all the folders
        for id, name in folders:
            item = QTreeWidgetItem([name])
#            print(item)
 #           self.target_tree.addTopLevelItem(item)


    def update_articles(self):
        self.tree.clear()  # Clear the tree before adding new items
        articles = self.database_manager.show_all_articles()  # Fetch all articles from the DatabaseManager
        for date, headline, description in articles:
            # Create a tree item for each article and add it to the tree
            item = QTreeWidgetItem([date, headline, description])
            self.tree.addTopLevelItem(item)       

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()

    def load_folders(self):
        # Clear the current tree
        self.target_tree.clear()

        # Fetch folders from the database
        folders = self.database_manager.get_all_folders()
        for folder in folders:
            folder_id, folder_name = folder
            folder_item = QTreeWidgetItem([folder_name])
            folder_item.setData(0, Qt.UserRole, folder_id)
            folder_item.setText(0, folder_name)
            folder_item.setText(1, str(folder_id))  # Updated this line
            self.target_tree.addTopLevelItem(folder_item)
             # Fetch articles in this folder
            articles = self.database_manager.get_articles_in_folder(folder_id)
            for article in articles:
                article_id, article_title = article
                article_item = QTreeWidgetItem([article_title])
                article_item.setData(0, Qt.UserRole, article_id)
                folder_item.addChild(article_item)
        self.target_tree.expandAll()

        return folders 


    def delete_article_button_clicked(self):
        selected_items = self.target_tree.selectedItems()
        if selected_items:
            selected_item = selected_items[0]

            article_id = selected_item.data(0, Qt.UserRole)  # Retrieve the article's ID
            article_title = selected_item.text(0)  # Retrieve the article's title

            print(f"Selected item '{selected_item}', ID '{article_id}', title '{article_title}'")
            if article_id is not None:  # If the selected item is an article
                  self.database_manager.delete_article(article_title)
                  # Remove the item from the tree
                  parent_item = selected_item.parent()
                  parent_item.removeChild(selected_item)
                  del selected_item
        else:
            QMessageBox.warning(self, "Invalid Selection", "Please select an article to delete.")


    def contextMenuEvent(self, event):
        menu = QMenu(self)
        set_delete_action = QAction("Delete Article", self)
        set_delete_action.triggered.connect(self.delete_article_button_clicked)
        menu.addAction(set_delete_action)

        # Show the context menu at the specified position
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == set_delete_action:
            self.delete_article_button_clicked()


# Removed
    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, 'New folder', 'Enter folder name:')
        if ok and folder_name.strip():
            # Add the new folder to the database and get the folder id
            folder_id = self.database_manager.add_new_folder(folder_name)
            print(f"Folder '{folder_name}' created with ID '{folder_id}'")

            # Refresh the tree view to reflect the updated folder structure
            self.load_folders()


 #   def update_folder_view(self):
 #       folders = self.folder_widget.load_folders()  # Get all the folders
 #       self.target_tree.clear()  # Clear the current items
 #       for id, name in folders:
 #           item = QTreeWidgetItem([name])
 #           self.target_tree.addTopLevelItem(item)

    def search_articles(self):
        search_string = self.search_bar.text()

        # Get all articles from the database
        all_articles = self.database_manager.fetch_articles()

        # Iterate over the articles and check if the search string is in the title or description
        search_results = []
        for date, headline, description in all_articles:
            if search_string.lower() in headline.lower() or search_string.lower() in description.lower():
                search_results.append((date, headline, description))

        # Clear the tree widget and add the search results
        self.tree.clear()
        for date, headline, description in search_results:
            self.add_headline(date, headline, description)
#Removed
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.acceptProposedAction()
             # Accept the drop event
#RRREMOVED
    def show_all_folders(self):
        all_folders = self.database_manager.get_all_folders()

        # Clear existing items in the tree widget
        self.tree.clear()

        # Add folders to the tree widget
        for folder_id, folder_name in all_folders:
            folder_item = QTreeWidgetItem([folder_name])
            folder_item.setData(0, Qt.UserRole, folder_id)
            self.tree.addTopLevelItem(folder_item)

        # Expand all folders
        self.tree.expandAll()

    def open_folder_window(self):
        self.folder_widget = FolderWidget(self)
        self.folder_window.show()  

#    def show_all_articles(self):
#        all_articles = self.database_manager.show_all_articles()

#        for date, headline, description in all_articles:
#            self.add_headline(date, headline, description)
#        QMessageBox.information(self, "Information", f"{len(all_articles)} articles have been added to the tree.")


    def keyPressEvent(self, event):
        if not self.target_tree.hasFocus():
            self.target_tree.setFocus()
        if event.key() == Qt.Key_D:
            self.delete_article_button_clicked()
        else:
            super().keyPressEvent(event)


    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_H:
            print("hello")
        elif event.key() in [Qt.Key_Enter, Qt.Key_Return]:
              self.open_article_dialog()

    def update_current_item_index(self):
         selected_items = self.tree.selectedItems()
         if selected_items:  # if there is a selection
            item = selected_items[0]  # get the first selected item
          #  print(item)
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

        # Show a notification
        notification_title = "New Article"
        notification_message = f"{headline}\n{description}"
        self.tray_icon.showMessage(notification_title, notification_message, QSystemTrayIcon.Information, 8000)  # Show the notification for 5 seconds

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

    def open_folder_window(self):
        self.folder_window = FolderWindow(self.folder_widget)
        self.folder_window.show() 

class DropTreeWidget(QTreeWidget):
    def __init__(self, parent=None, database_manager=None, main_window=None):
        self.database_manager = DatabaseManager()
        self.main_window = None  # Reference to the MyWindow instance
        super().__init__(parent)
        self.setAcceptDrops(True)

    def set_main_window(self, main_window):
        self.main_window = main_window

    def startDrag(self, event):
        items = self.selectedItems()

        if items:
            drag = QDrag(self)
            mimedata = self.model().mimeData(items)

            drag.setMimeData(mimedata)
            drag.exec_(Qt.MoveAction) 


    def dropEvent(self, event):
        source = event.source()

        if isinstance(source, QTreeWidget):
            items = source.selectedItems()
            parent_item = self.itemAt(event.pos())

            if parent_item:
                for item in items:
                    clone_item = item.clone()
                    parent_item.addChild(clone_item)

                    # Remove the item from the source tree
                    source.takeTopLevelItem(source.indexOfTopLevelItem(item))

                    # Print a message indicating that the article was dragged to the folder
                    date = item.text(0)
                    title = item.text(1)
                    description = item.text(2)
                    folder_name = parent_item.text(0)
                    folder_id = parent_item.text(1)
           #         print(f"Title '{title}', description '{description}', date '{date}', folderid {folder_id} foldername '{folder_name}'")

                    self.database_manager.save_article_to_folder(title, description, date, folder_id)
            event.accept()


            event.accept()
        else:
            event.ignore()  


    def dropMimeData(self, parent, index, data, action):
        if action == Qt.MoveAction:
            # Parse mime data to get item data
            item_data = data.data('application/x-qabstractitemmodeldatalist')
            stream = QDataStream(item_data, QIODevice.ReadOnly)
            while not stream.atEnd():
                row = stream.readInt32()
                col = stream.readInt32()
                map_items = stream.readInt32()
                for _ in range(map_items):
                    key = stream.readInt32()
                    value = stream.readQVariant()
                    if key == 0:  # Key 0 usually contains the item's text
                        new_item = QTreeWidgetItem([str(value)])
                        if parent is None:
                            # If the parent is None, add it as a top level item
                            self.addTopLevelItem(new_item)
                        else:
                            # Otherwise, add it as a child of the parent item
                            parent.addChild(new_item)
            return True
        return False


   # def delete_article_button_clicked(self):
   #     selected_items = self.main_window.target_tree.selectedItems()
   #     if selected_items:
   #         selected_item = selected_items[0]
#
#            article_id = selected_item.data(0, Qt.UserRole)  # Retrieve the article's ID
#            article_title = selected_item.text(0)  # Retrieve the article's title

 #           print(f"Selected item '{selected_item}', ID '{article_id}', title '{article_title}'")
 #           if article_id is not None:  # If the selected item is an article
 #                 self.database_manager.delete_article(article_title)
 #                 # Remove the item from the tree
 #                 parent_item = selected_item.parent()
 #                 parent_item.removeChild(selected_item)
  #                del selected_item
  #      else:
  #          QMessageBox.warning(self, "Invalid Selection", "Please select an article to delete.")


    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # Create the "Set Alert" action
        set_alert_action = QAction("Set Alert", self)
        set_alert_action.triggered.connect(self.set_alert)
        menu.addAction(set_alert_action)


#        set_delete_action = QAction("Delete Article", self)
#        set_delete_action.triggered.connect(self.delete_article_button_clicked)
#        menu.addAction(set_delete_action)

        # Show the context menu at the specified position
#        action = menu.exec_(self.mapToGlobal(event.pos()))
#        if action == set_delete_action:
#            self.delete_article_button_clicked()


        
    def set_alert(self):
        selected_items = self.target_tree.selectedItems()
        if selected_items:
            # Get the selected article's data and perform the necessary actions
            for item in selected_items:
                date = item.text(0)
                headline = item.text(1)
                description = item.text(2)
                # Perform your alert setup or logic here
                print(f"Set Alert: {date}, {headline}, {description}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_manager = DatabaseManager()
    monitor = NewsMonitor(database_manager)
    window = MyWindow(monitor, database_manager)  # Pass the database manager here
    window.show()
    sys.exit(app.exec_())


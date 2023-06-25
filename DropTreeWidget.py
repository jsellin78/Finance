class DropTreeWidget(QTreeWidget):
    def __init__(self, parent=None, database_manager=None, my_window=None):
        self.database_manager = database_manager
        self.my_window = my_window
        self.market_data = DatabaseManager()
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu) 

        self.database_manager.create_table_folder_states()
        self.database_manager.add_unique_constraint_to_folder_id()
        self.itemExpanded.connect(self.save_expanded_state)
        self.itemCollapsed.connect(self.save_collapsed_state)
        self.setHeaderLabel('Article titles')
        self.contextMenu = QMenu(self)
        self.writeAction = QAction('Write Text', self)


        self.markInterestingAction = QAction('Mark/Unmark as Interesting', self)
        self.contextMenu.addAction(self.markInterestingAction)
        self.markInterestingAction.triggered.connect(self.mark_as_interesting)


        self.delete_item = QAction('Delete Folder / Article', self)  # Create a "Delete Article" action
        self.contextMenu.addAction(self.delete_item)  # Add the action to the context menu
        self.delete_item.triggered.connect(self.delete_selected_item)  # Connect the action to the delete_article method


        self.new_folder = QAction('New Folder', self)  # Create a "Delete Article" action
        self.contextMenu.addAction(self.new_folder)  # Add the action to the context menu
        self.new_folder.triggered.connect(self.create_new_folderr)  # Connect the action to the delete_article method

        self.set_alert = QAction('Set Alert', self)  # Create a "Delete Article" action
        self.contextMenu.addAction(self.set_alert)  # Add the action to the context menu
        self.set_alert.triggered.connect(self.set_Alert)  # Connect the action to the delete_article method


        self.contextMenu.addAction(self.writeAction)
        self.writeAction.triggered.connect(self.write_text)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)
     
        self.contextMenu.setStyleSheet("""
            QMenu {
                background-color: #F5F5F5; /* sets background of the menu */
                color: #000000; /* sets text color */
                border: 1px solid #D9D9D9; /* sets border color */
            }
            QMenu::item:selected {
                background-color: #FF0000; /* sets background of selected item */
            }
            QMenu::item:hover {
                background-color: #ADD8E6; /* sets background when an item is hovered */
            }
        """)




    def save_expanded_state(self, item):
        folder_id = item.data(0, Qt.UserRole)
        print(f"Expanded folder with id {folder_id}")
        result = self.database_manager.update_folder_state_in_db(folder_id, True)
        if result:
            print(f"Successfully saved expanded state for folder id {folder_id}")
        else:
             print(f"Failed to save expanded state for folder id {folder_id}")

    def save_collapsed_state(self, item):
        folder_id = item.data(0, Qt.UserRole)
        print(f"Collapsed folder with id {folder_id}")
        result = self.database_manager.update_folder_state_in_db(folder_id, False)
        if result:
            print(f"Successfully saved collapsed state for folder id {folder_id}")
        else:
             print(f"Failed to save collapsed state for folder id {folder_id}")

    def set_Alert(self):
        selected_items = self.my_window.target_tree.selectedItems()
        article_id = self.get_selected_article_id()
        if selected_items:
            selected_item = selected_items[0]
            article_id = selected_item.data(0, Qt.UserRole)
            print(article_id)
            article_details = self.database_manager.get_article_details(article_id)

            if article_details is None:
                print(f"No details found for article with id {article_id}")
                return  

            id, article_title, article_description, article_date = article_details


            self.dialog = QDialog(self)
            self.dialog.setWindowTitle('Set Alert')

            self.dialog.setStyleSheet("background-color: black;")

            date_label = QLabel(f"Published Date: {article_date}", self.dialog)
            title_label = QLabel(f"Title: {article_title}", self.dialog)
            title_label.setWordWrap(True)  # Set WordWrap for title_label
            description_label = QLabel(f"Description: {article_description}", self.dialog)
            description_label.setWordWrap(True)

            self.datetime_field = QDateTimeEdit(self.dialog)
            self.datetime_field.setDateTime(QDateTime.currentDateTime())  
            self.datetime_field.setCalendarPopup(True)  # Enables a calendar popup for date selection
            self.datetime_field.setDisplayFormat("yyyy-MM-dd HH:mm")  
            self.datetime_field.setStyleSheet("""
            QAbstractItemView::item {
                color: yellow;  /* adjust this color according to your needs */
            }
            QCalendarWidget QTableView {
                alternate-background-color: #292929;
            }
            QCalendarWidget QTableView QHeaderView::section {
               background-color: black;
               color: yellow;  /* adjust this color according to your needs */
            }
            """)
            comment_label = QLabel('Add Comment', self.dialog)  
            self.comment_field = QTextEdit(self.dialog)  
            self.comment_field.setStyleSheet("""
                border: 1px solid grey;
            """)
            self.comment_field.setFixedHeight(100)  
            ok_button = QPushButton('OK', self.dialog)
            ok_button.clicked.connect(lambda: self.on_ok_button_clicked(article_id, article_title, article_description))
               

            layout = QVBoxLayout(self.dialog)
            layout.setSpacing(10)  # set spacing between widgets in the layout
            layout.setContentsMargins(10, 10, 10, 10)  # set margins around the layout
            layout.addWidget(date_label)
            layout.addWidget(title_label)
            layout.addWidget(description_label)
            layout.addWidget(comment_label)
            layout.addWidget(self.comment_field)
            layout.addWidget(self.datetime_field)
            layout.addWidget(ok_button)

            self.dialog.setLayout(layout)
            self.dialog.show()   

        # dynamically adjust the width of the description label based on the QDialog size
        description_label.setFixedWidth(int(self.dialog.width() * 0.8))

        # adjust the width of the description label when the QDialog is resized
        self.dialog.resizeEvent = lambda event: (
            description_label.setFixedWidth(self.dialog.width() * 0.8),
            title_label.setWordWrap(True),
            description_label.setWordWrap(True)
        )


    def run_remote_script(self, article_title, article_description, article_id, selected_date_time, alert_status, chat_id, comment_text):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the server's host key (not recommended for production)
        ssh.connect('192.168.1.120', port='2216', username='root', password='deduu')  # Substitute with your server's details
        try: 
            # Convert the datetime to a string, because we can only pass strings as arguments

            selected_date_time_str = selected_date_time.strftime('%Y%m%d%H%M')

            python_command = ' '.join([
                'python3',
                '/root/newstart/pyqtscripts/timer.py', 
                '--trigger_date=' + selected_date_time_str,
                '--title=' + shlex.quote(str(article_title)).replace('"', '\\"'),
                '--description=' + shlex.quote(str(article_description)).replace('"', '\\"'),
                '--comment=' + shlex.quote(str(comment_text)).replace('"', '\\"'),
                '&',
            ])
        
            command_str = f'tmux send-keys -t ifvalues \"{python_command}\" Enter'
            stdin, stdout, stderr = ssh.exec_command(command_str)  # Execute the command



            print("Output of the command:")
            print(stdout.read().decode())

            print("Errors of the command:")
            print(stderr.read().decode())

   #     ssh.exec_command(command_str)  # Execute the command
        finally: 
            ssh.close()


    def on_ok_button_clicked(self, article_id, article_title, article_description):
        selected_date_time = self.datetime_field.dateTime().toPyDateTime()
        print(f"Selected Date: {selected_date_time}")  # Print article text
        comment_text = self.comment_field.toPlainText()
        print(f"Comment_text: {comment_text}")  # Print article text
        chat_id = "123"
        self.dialog.close()
        print(f"Article title: {article_title}")  
        print(f"Article description: {article_description}")  
        self.database_manager.add_alert(article_id, selected_date_time, "PENDING", chat_id, comment_text)
        print(f"Article_id: {article_id}")  # Print article text
        self.run_remote_script(article_title, article_description, article_id, selected_date_time, "PENDING", chat_id, comment_text)


    def create_new_folderr(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle('New Folder')

        self.input_field = QLineEdit(self.dialog)
        ok_button = QPushButton('OK', self.dialog)
        ok_button.clicked.connect(self.add_new_folder)

        layout = QVBoxLayout(self.dialog)
        layout.addWidget(self.input_field)
        layout.addWidget(ok_button)

        self.dialog.setLayout(layout)
        self.dialog.show()

    def find_all_pending_alerts(self):
        # Fetch all pending alerts from the database
        pending_alerts = self.database_manager.get_pending_alerts()
        # Iterate through each pending alert and relaunch it
        for alert in pending_alerts:
            id, title, description, _, folder_id, _, _, _, trigger_date, alert_status, chat_id, comment = alert
            article_title = title
            article_description = description
            article_id = id
            selected_date_time = trigger_date
            comment_text = comment 

            if trigger_date > datetime.now():
               # If so, relaunch the alert
               self.run_remote_script(article_title, article_description, article_id, selected_date_time, "PENDING", chat_id, comment_text)

               time.sleep(random.uniform(1, 2))



    def mark_as_interesting(self):
        selected_items = self.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            article_id = selected_item.data(0, Qt.UserRole)
            # Fetch current state of the article
            is_interesting, image_path = self.database_manager.get_article_interesting_state(article_id)

            if is_interesting:
                # Already marked as interesting, so remove the mark
                selected_item.setIcon(0, QIcon())
                self.database_manager.unmark_as_interesting(article_id)
            else:
                # Not marked as interesting, so add the mark
                icon = QIcon(":/icons/RED.jpg")
                selected_item.setIcon(0, icon)
                self.database_manager.mark_as_interesting(article_id)


    def load_folders(self):
        self.my_window.target_tree.clear()

        folders = self.database_manager.get_all_folders()
        for folder in folders:
            folder_id, folder_name = folder
            folder_item = QTreeWidgetItem([folder_name])
            folder_item.setData(0, Qt.UserRole, folder_id)
            folder_item.setData(0, Qt.UserRole+1, "folder")  # <--- Add this line
            folder_item.setText(0, folder_name)
            folder_item.setText(1, str(folder_id))  # Updated this line
            self.my_window.target_tree.addTopLevelItem(folder_item)
             # Fetch articles in this folder
            articles = self.database_manager.get_articles_in_folder(folder_id)
            for article in articles:
                article_id, article_title, article_date, article_text, is_interesting, image_path = article
                print(f"Article text: {article_text}")  # Print article text
                article_item = QTreeWidgetItem([article_title, article_date])
                article_item.setData(0, Qt.UserRole, article_id)
                article_item.setData(0, Qt.UserRole+1, 'article')  # Make sure you're doing this for articles too
                article_item.setToolTip(0, article_text)  # Set the tooltip
                folder_item.addChild(article_item)
                if is_interesting:
                   article_item.setIcon(0, QIcon(image_path))
                folder_item.addChild(article_item)    

            # Set the initial expanded/collapsed state of the folder based on the database
            is_expanded = self.database_manager.get_folder_state(folder_id)
            if is_expanded is not None:  # Only attempt to set the state if a valid state was returned
                folder_item.setExpanded(is_expanded)
            else:
                 folder_item.setExpanded(True)
        return folders
#        self.my_window.target_tree.expandAll()



    def startDrag(self, event):
        items = self.my_window.target_tree.selectedItems()
       # items = self.selectedItems()
        if items:
            drag = QDrag(self)
            model = self.model()
            parent_index = self.my_window.target_tree.rootIndex()  # Assuming you want to use the root index
            indexes = [model.index(self.my_window.target_tree.indexOfTopLevelItem(item), 0) for item in items]
            mime_data = model.mimeData(indexes)

            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction) 

     
    def dropEvent(self, event):
        source = event.source()

        if isinstance(source, QTreeWidget):
            items = source.selectedItems()
            parent_item = self.itemAt(event.pos())

            if parent_item:
                for item in items:
                    # Check if the parent_item is not the same as the dragged item
                    if parent_item != item:
                        clone_item = item.clone()
                        parent_item.addChild(clone_item)

                        # Remove the item from the source tree
                        if item.parent() is not None:
                            item.parent().removeChild(item)
                        else:
                            source.invisibleRootItem().takeChild(source.indexOfTopLevelItem(item))

                        # Print a message indicating that the article was dragged to the folder

                        date = item.text(0)
                        title = item.text(1)
                        description = item.text(2)
                        folder_name = parent_item.text(0)
                        folder_id = parent_item.data(0, Qt.UserRole)
                        if folder_id is None:
                            folder_id = parent_item.text(1)
                        print(f"Title '{title}', description '{description}', date '{date}', folderid {folder_id}, foldername '{folder_name}'")
                        article_id = self.database_manager.save_article_to_folder(title, description, date, folder_id)

                        clone_item.setData(0, Qt.UserRole, article_id)
                        clone_item.setText(1, date)
                        clone_item.setText(0, title)

        event.accept()


    def dropMimeData(self, parent, index, data, action):
        if action == Qt.MoveAction:
            # Parse mime data to get item data
            item_data = data.data('application/x-qabstractitemmodeldatalist')
            stream = QDataStream(item_data, QIODevice.ReadOnly)
            while not stream.atEnd():
                #        row = stream.readInt32()
        #col = stream.readInt32()
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


    def get_selected_article_id(self):
        selected_items = self.my_window.target_tree.selectedItems()
        if selected_items:
           selected_item = selected_items[0]
           article_id = selected_item.data(0, Qt.UserRole) 
           return article_id
        return None


    def open_menu(self, position):
        self.contextMenu.exec_(self.viewport().mapToGlobal(position))

    def insert_text_to_database(self, article_id):
        article_text = self.text_editor.toPlainText()
        print(f"article_text = {article_text}")  # Debug print statement
        if article_text:  # Only update database if article_text is not empty
           self.database_manager.insert_text_to_database(article_id, article_text)
        else:
            print("No text entered. Article text not updated.")
        self.dialog.close()

      
    def write_text(self):
        article_id = self.get_selected_article_id()
        print(f"article_id = {article_id}")
        if article_id is None:
           # Optionally you can display a warning to the user.
           return
        # Fetch the existing text for the article
        existing_text = self.database_manager.get_article_text(article_id)

        self.dialog = QDialog(self)

        self.dialog.setWindowTitle("Write Text")

        self.text_editor = QTextEdit(self.dialog)
        self.text_editor.setPlainText(existing_text)  # Set the existing text

        self.insert_button = QPushButton("Insert", self.dialog)
        self.insert_button.clicked.connect(lambda: self.insert_text_to_database(article_id))

        self.layout = QVBoxLayout(self.dialog)
        self.layout.addWidget(self.text_editor)
        self.layout.addWidget(self.insert_button)
        self.dialog.setLayout(self.layout)
        self.load_folders()
        self.dialog.show()


    def add_new_folder(self):
        folder_name = self.input_field.text().strip()
        if folder_name:
           folder_id = self.database_manager.add_new_folder(folder_name)
           print(f"Folder '{folder_name}' created with ID '{folder_id}'")

           folder_item = QTreeWidgetItem([folder_name])

           folder_item.setData(0, Qt.UserRole, folder_id)

           self.my_window.target_tree.addTopLevelItem(folder_item)
        
           self.dialog.close()

    def delete_selected_item(self):
        selected_items = self.my_window.target_tree.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            print(F" selected_item '{selected_items}' ")
            item_type = selected_item.data(0, Qt.UserRole+1)  # Retrieve the type attribute
            print(F" item_type '{item_type}' ")

            if item_type == "folder":
                folder_id = selected_item.data(0, Qt.UserRole)
                self.database_manager.delete_folder(folder_id)

                # Remove the item from the tree
                index = self.indexOfTopLevelItem(selected_item) 
                self.takeTopLevelItem(index)
                print(f"Folder with ID '{folder_id}' deleted.")
                del selected_item
                self.load_folders()
            elif item_type == "article":
               # Delete the article
               article_id = selected_item.data(0, Qt.UserRole)
               self.database_manager.delete_article(article_id)

               # Remove the item from the tree
               parent_item = selected_item.parent()
               index = parent_item.indexOfChild(selected_item)
               parent_item.takeChild(index)
               print(f"Article with ID '{article_id}' deleted.")
               del selected_item


    def delete_articlee(self):
        selected_items = self.my_window.target_tree.selectedItems()
        if selected_items:
            selected_item = selected_items[0]

            article_id = selected_item.data(0, Qt.UserRole)  # Retrieve the article's ID
            article_title = selected_item.text(0)  # Retrieve the article's title

            print(f"Selected item '{selected_item}', ID '{article_id}', title '{article_title}'")
            if article_id is not None:  # If the selected item is an article
                  self.database_manager.delete_article(article_title)
                  # Remove the item from the tree
                  parent_item = selected_item.parent()
                #  parent_item.removeChild(selected_item)
                  del selected_item
                  self.load_folders()
        else:
            QMessageBox.warning(self, "Invalid Selection", "Please select an article to delete.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_manager = DatabaseManager()
    monitor = NewsMonitor(database_manager)
    window = MyWindow(monitor, database_manager)  
    market_data = MarketData()
    window.show()
    sys.exit(app.exec_())

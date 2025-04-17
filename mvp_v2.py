# import sys
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
#     QFileDialog, QLineEdit, QMessageBox
# )
# from PySide6.QtGui import QFont
# from PySide6.QtCore import Qt, QSize
# from uploader import run_sync  # imports our logic from uploader.py

# # GUI class for our Dropbox sync app
# class DropboxSyncApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Dropbox File Uploader")

#         # set default window size (now resizable)
#         self.resize(800, 600)

#         self.local_folder = ''  # holds the selected local folder
#         self.dropbox_folder_name = 'Test'  # default Dropbox folder

#         self.layout = QVBoxLayout()  # vertical stacking of widgets

#         # create widgets
#         self.label = QLabel("Select the local folder to sync:")
#         self.select_button = QPushButton("Browse Folder")
#         self.folder_display = QLabel("No folder selected")
#         self.dbx_label = QLabel("Enter Dropbox folder name:")
#         self.dbx_input = QLineEdit()
#         self.sync_button = QPushButton("Start Sync")

#         # placeholder text for Dropbox folder input
#         self.dbx_input.setPlaceholderText("e.g., Test")

#         # connect button clicks to methods
#         self.select_button.clicked.connect(self.browse_folder)
#         self.sync_button.clicked.connect(self.start_sync)

#         # add widgets to the layout
#         self.layout.addWidget(self.label)
#         self.layout.addWidget(self.select_button)
#         self.layout.addWidget(self.folder_display)
#         self.layout.addWidget(self.dbx_label)
#         self.layout.addWidget(self.dbx_input)
#         self.layout.addWidget(self.sync_button)

#         self.setLayout(self.layout)

#         # set a slightly larger base font
#         self.base_font_size = 14
#         self.adjust_font(self.base_font_size)

#     # called when window resizes — scales font size proportionally
#     def resizeEvent(self, event):
#         height = self.height()
#         scale_factor = height / 600  # new base height
#         new_font_size = max(int(self.base_font_size * scale_factor), 10)
#         self.adjust_font(new_font_size)

#     # applies the computed font size to all widgets
#     def adjust_font(self, size):
#         font = QFont("Arial", size)
#         for widget in [
#             self.label,
#             self.select_button,
#             self.folder_display,
#             self.dbx_label,
#             self.dbx_input,
#             self.sync_button
#         ]:
#             widget.setFont(font)

#     # handles folder selection
#     def browse_folder(self):
#         folder = QFileDialog.getExistingDirectory(self, "Select Folder")
#         if folder:
#             self.local_folder = folder
#             self.folder_display.setText(folder)

#     # handles sync logic after clicking "Start Sync"
#     def start_sync(self):
#         dbx_folder = self.dbx_input.text() or "Test"
#         if not self.local_folder:
#             QMessageBox.warning(self, "Error", "Please select a local folder.")
#             return

#         try:
#             run_sync(dropbox_folder=dbx_folder, local_path=self.local_folder)
#             QMessageBox.information(self, "Done", "Files synced successfully!")
#         except Exception as e:
#             QMessageBox.critical(self, "Sync Failed", str(e))


# # runs the GUI app
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DropboxSyncApp()
#     window.show()
#     sys.exit(app.exec())


import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                               QFileDialog, QLineEdit, QMessageBox)
from PySide6.QtGui import QFont
from uploader import run_sync
from establishConnection import connect_to_dropbox

class DropboxSyncApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dropbox File Uploader")
        self.resize(800, 600)

        self.local_folder = ''
        self.layout = QVBoxLayout()

        self.label = QLabel("Select the local folder to sync:")
        self.select_button = QPushButton("Browse Folder")
        self.folder_display = QLabel("No folder selected")
        self.dbx_label = QLabel("Enter Dropbox folder name:")
        self.dbx_input = QLineEdit("Test")
        self.sync_button = QPushButton("Start Sync")

        self.select_button.clicked.connect(self.browse_folder)
        self.sync_button.clicked.connect(self.start_sync)

        for widget in [self.label, self.select_button, self.folder_display,
                       self.dbx_label, self.dbx_input, self.sync_button]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)
        self.base_font_size = 14
        self.adjust_font(self.base_font_size)

    def resizeEvent(self, event):
        height = self.height()
        scale_factor = height / 600
        self.adjust_font(max(int(self.base_font_size * scale_factor), 10))

    def adjust_font(self, size):
        font = QFont("Arial", size)
        for widget in [self.label, self.select_button, self.folder_display,
                       self.dbx_label, self.dbx_input, self.sync_button]:
            widget.setFont(font)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.local_folder = folder
            self.folder_display.setText(folder)

    def start_sync(self):
        dbx_folder = self.dbx_input.text().strip() or "Test"
        if not self.local_folder:
            QMessageBox.warning(self, "Missing Folder", "Please select a local folder.")
            return

        dbx = connect_to_dropbox()
        if not dbx:
            return

        try:
            run_sync(dbx, dropbox_folder=dbx_folder, local_path=self.local_folder)
            QMessageBox.information(self, "Success", "Files synced successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Sync Failed", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropboxSyncApp()
    window.show()
    sys.exit(app.exec())
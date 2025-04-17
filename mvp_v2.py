import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                               QFileDialog, QLineEdit, QMessageBox)
from PySide6.QtGui import QFont
from uploader import run_sync
from establishConnection import connect_to_dropbox

# Main window class for the Dropbox sync app
class DropboxSyncApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dropbox File Uploader")
        self.resize(800, 600)

        # Internal state
        self.local_folder = ''
        self.layout = QVBoxLayout()

        # UI widgets
        self.label = QLabel("Select the local folder to sync:")
        self.select_button = QPushButton("Browse Folder")
        self.folder_display = QLabel("No folder selected")
        self.dbx_label = QLabel("Enter Dropbox folder name:")
        self.dbx_input = QLineEdit("Test")  # Default Dropbox parent folder
        self.sync_button = QPushButton("Start Sync")

        # Event handlers
        self.select_button.clicked.connect(self.browse_folder)
        self.sync_button.clicked.connect(self.start_sync)

        # Layout packing
        for widget in [self.label, self.select_button, self.folder_display,
                       self.dbx_label, self.dbx_input, self.sync_button]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)
        self.base_font_size = 14
        self.adjust_font(self.base_font_size)

    # Resize font when window is resized
    def resizeEvent(self, event):
        height = self.height()
        scale_factor = height / 600
        self.adjust_font(max(int(self.base_font_size * scale_factor), 10))

    def adjust_font(self, size):
        font = QFont("Arial", size)
        for widget in [self.label, self.select_button, self.folder_display,
                       self.dbx_label, self.dbx_input, self.sync_button]:
            widget.setFont(font)

    # Browse and select local folder using file dialog
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.local_folder = folder
            self.folder_display.setText(folder)

    # Start the sync process when user clicks the button
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

# Launch the GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropboxSyncApp()
    window.show()
    sys.exit(app.exec())

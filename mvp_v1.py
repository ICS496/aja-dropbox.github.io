import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QLineEdit, QMessageBox
)
from uploader_v2 import run_sync  # imports our logic from uploader.py

# GUI class for our Dropbox sync app
class DropboxSyncApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dropbox File Uploader")
        self.setFixedSize(400, 250)

        self.local_folder = ''  # will hold the selected local folder
        self.dropbox_folder_name = 'Test'  # default Dropbox folder name

        self.layout = QVBoxLayout()  # vertical layout for stacking widgets

        # label and button to select a folder on the local machine
        self.label = QLabel("Select the local folder to sync:")
        self.layout.addWidget(self.label)

        self.select_button = QPushButton("Browse Folder")
        self.select_button.clicked.connect(self.browse_folder)
        self.layout.addWidget(self.select_button)

        self.folder_display = QLabel("No folder selected")
        self.layout.addWidget(self.folder_display)

        # input box for specifying Dropbox folder name
        self.dbx_label = QLabel("Enter Dropbox folder name:")
        self.layout.addWidget(self.dbx_label)

        self.dbx_input = QLineEdit()
        self.dbx_input.setPlaceholderText("e.g., Test")  # example hint
        self.layout.addWidget(self.dbx_input)

        # button to start the sync process
        self.sync_button = QPushButton("Start Sync")
        self.sync_button.clicked.connect(self.start_sync)
        self.layout.addWidget(self.sync_button)

        self.setLayout(self.layout)

    # called when user clicks "Browse Folder"
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.local_folder = folder
            self.folder_display.setText(folder)  # updates label to show folder

    # called when user clicks "Start Sync"
    def start_sync(self):
        dbx_folder = self.dbx_input.text() or "Test"  # fallback if empty
        if not self.local_folder:
            # show error popup if no folder was selected
            QMessageBox.warning(self, "Error", "Please select a local folder.")
            return

        try:
            # runs our main sync logic from uploader.py
            run_sync(dropbox_folder=dbx_folder, local_path=self.local_folder)
            QMessageBox.information(self, "Done", "Files synced successfully!")  # popup success
        except Exception as e:
            # show any errors that might’ve occurred during sync
            QMessageBox.critical(self, "Sync Failed", str(e))


# runs the GUI app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropboxSyncApp()
    window.show()
    sys.exit(app.exec())

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QLineEdit, QMessageBox, QHBoxLayout, QToolButton, QTextEdit
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import QSize
from uploader_v2 import run_sync
from establish_connection import connect_to_dropbox
from datetime import datetime

class DropboxSyncApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dropbox File Uploader")
        self.resize(800, 600)

        self.local_folder = ''
        self.base_font_size = 14
        self.layout = QVBoxLayout()

        # --- ROW 1: Local folder label + text field + icon button ---
        self.label = QLabel("Select the local folder to sync:")

        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Enter or browse local folder...")
        self.folder_input.setMinimumWidth(400)

        self.folder_icon = QToolButton()
        self.folder_icon.setIcon(QIcon.fromTheme("folder"))
        self.folder_icon.setIconSize(QSize(24, 24))
        self.folder_icon.setToolTip("Browse Folder")
        self.folder_icon.clicked.connect(self.browse_folder)

        row1 = QHBoxLayout()
        row1.addWidget(self.label)
        row1.addWidget(self.folder_input, stretch=3)
        row1.addWidget(self.folder_icon)

        # --- ROW 2: Dropbox folder label + text field ---
        self.dbx_label = QLabel("Enter Dropbox folder name:")
        self.dbx_input = QLineEdit("Test")

        row2 = QHBoxLayout()
        row2.addWidget(self.dbx_label)
        row2.addWidget(self.dbx_input, stretch=3)

        # --- ROW 3: Sync button centered + padded ---
        self.sync_button = QPushButton("Start Sync")
        self.sync_button.setFixedWidth(150)
        self.sync_button.setStyleSheet("padding: 10px 20px;")
        self.sync_button.clicked.connect(self.start_sync)

        row3 = QHBoxLayout()
        row3.addStretch(1)
        row3.addWidget(self.sync_button)
        row3.addStretch(1)

        # --- ROW 4: Logs section ---
        self.log_label = QLabel("Logs:")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #f5f5f5; padding: 10px;")
        self.log_output.setMinimumHeight(200)
        self.log_output.setLineWrapMode(QTextEdit.NoWrap)

        # --- Assemble layout ---
        self.layout.addLayout(row1)
        self.layout.addLayout(row2)
        self.layout.addSpacing(20)
        self.layout.addLayout(row3)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.log_label)
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)
        self.adjust_font(self.base_font_size)

    def resizeEvent(self, event):
        height = self.height()
        scale_factor = height / 600
        self.adjust_font(max(int(self.base_font_size * scale_factor), 10))

    def adjust_font(self, size):
        font = QFont("Arial", size)
        for widget in [self.label, self.folder_input,
                       self.dbx_label, self.dbx_input, self.sync_button, self.log_label]:
            widget.setFont(font)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "SUCCESS": "#28a745",   # Green
            "FAILED": "#dc3545",    # Red
            "SKIPPED": "#6c757d",   # Gray
            "INFO": "#007bff"       # Blue
        }
        color = color_map.get(status, "#000000")

        # Table layout: message on the left, timestamp fully justified to the right
        html = f'''
        <table width="100%%" style="border-collapse: collapse;">
          <tr>
            <td style="color:{color}; font-weight: bold;">[{status}] {message}</td>
            <td style="text-align:right; color:gray; font-size:90%;">{timestamp}</td>
          </tr>
        </table>
        '''
        self.log_output.append(html)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def start_sync(self):
        self.log_output.clear()  # <-- Clear logs here
        self.local_folder = self.folder_input.text().strip()
        dbx_folder = self.dbx_input.text().strip() or "Test"

        if not self.local_folder:
            QMessageBox.warning(self, "Missing Folder", "Please select a local folder.")
            return

        dbx = connect_to_dropbox()
        if not dbx:
            return

        try:
            self.log("Starting sync...", "INFO")
            run_sync(dbx, dropbox_folder=dbx_folder, local_path=self.local_folder, logger=self.log)
            self.log("Sync completed successfully.", "SUCCESS")
            QMessageBox.information(self, "Success", "Files synced successfully!")
        except Exception as e:
            self.log(f"Sync failed: {e}", "FAILED")
            QMessageBox.critical(self, "Sync Failed", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropboxSyncApp()
    window.show()
    sys.exit(app.exec())

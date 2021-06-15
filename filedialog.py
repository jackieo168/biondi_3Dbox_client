import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from pathlib import Path


class FileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # text
        self.title = "Initialize a Case"
        
        # properties
        self.x = 300
        self.y = 300
        self.width = 400
        self.height = 150
        
        # central widget
        self.central_widget = QWidget()
        
        # layouts
        self.dlg_layout = QVBoxLayout()
        self.open_file_layout = QHBoxLayout()
        self.save_dir_layout = QHBoxLayout()
        self.form_layout = QFormLayout()

        # line edit
        self.open_file_entry = QLineEdit()
        self.save_dir_entry = QLineEdit()
        
        # buttons
        self.open_file_browse_btn = QPushButton("Browse")
        self.save_dir_browse_btn = QPushButton("Browse")
        self.dlg_btns = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        # initialize UI
        self.init_UI()

    def init_UI(self):
        """
        Initialize text/buttons for the main window.
        """
        # buttons
        self.dlg_btns.accepted.connect(self.on_ok_click)
        self.dlg_btns.rejected.connect(self.on_cancel_click)
        self.open_file_browse_btn.clicked.connect(self.on_open_file_click)
        self.save_dir_browse_btn.clicked.connect(self.on_save_file_click)

        # layouts
        self.open_file_layout.addWidget(self.open_file_entry)
        self.open_file_layout.addWidget(self.open_file_browse_btn)

        self.save_dir_layout.addWidget(self.save_dir_entry)
        self.save_dir_layout.addWidget(self.save_dir_browse_btn)
        
        self.form_layout.addRow("Array Path (.npy): ", self.open_file_layout)
        self.form_layout.addRow("Save Folder: ", self.save_dir_layout)

        self.dlg_layout.addLayout(self.form_layout)
        self.dlg_layout.addWidget(self.dlg_btns)

        # set file dialog properties
        self.setLayout(self.dlg_layout)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle(self.title)
        self.show()

    def on_ok_click(self):
        pass

    def on_cancel_click(self):
        pass

    def on_open_file_click(self):
        pass

    def on_save_file_click(self):
        pass
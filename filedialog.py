import sys
from PyQt5.QtWidgets import *
from filestate import FileState


class FileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filestate = FileState()

        # text
        self.title = "Initialize a Case"
        
        # properties
        self.x = 300
        self.y = 300
        self.width = 400
        self.height = 150
        
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
        self.open_file_browse_btn.clicked.connect(self.on_open_file_browse_btn_click)
        self.save_dir_browse_btn.clicked.connect(self.on_save_dir_browse_btn_click)

        # line edits
        self.open_file_entry.returnPressed.connect(self.on_open_file_enter)
        self.save_dir_entry.returnPressed.connect(self.on_save_dir_enter)

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

    def on_open_file_browse_btn_click(self):
        """
        when open file browse button is clicked.
        """
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "NumPy Files (*.npy)",
                        options=options)
        if filename:
            self.filestate.set_file_name( filename )
            self.refresh_UI()

    def on_save_dir_browse_btn_click(self):
        """
        when save dir browse button is clicked.
        """
        pass

    def on_open_file_enter(self):
        """
        when open file is inputted into line edit, and enter is pressed.
        """
        pass

    def on_save_dir_enter(self):
        """
        when save dir is inputted into line edit, and enter is pressed.
        """
        pass

    def on_ok_click(self):
        """
        when ok button is pressed, launch napari.
        """
        pass

    def on_cancel_click(self):
        """
        when cancel button is pressed, close dialog.
        """
        self.close()

    def refresh_UI(self):
        self.open_file_entry.setText(self.filestate.get_file_name())
        self.save_dir_entry.setText(self.filestate.get_save_dir())
    
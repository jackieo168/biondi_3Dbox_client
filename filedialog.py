import sys
from PyQt5.QtWidgets import *
from filestate import FileState
import numpy as np
import napari
import tkinter as tk
from app import Application

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
        self.dlg_btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

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
        # self.open_file_entry.returnPressed.connect(self.on_open_file_enter)
        # self.save_dir_entry.returnPressed.connect(self.on_save_dir_enter)

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

    def display_message(self, msg):
        """
        displays msg in message box widget.
        """
        mbox = QMessageBox()
        mbox.setWindowTitle("Warning")
        mbox.setText(msg)
        mbox.setIcon(QMessageBox.Warning)
        mbox.setStandardButtons(QMessageBox.Ok)
        _ = mbox.exec_()

    def on_open_file_browse_btn_click(self):
        """
        when open file browse button is clicked.
        """
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
                        self,
                        "Select Input Numpy Array",
                        ".",
                        "NumPy Files (*.npy)",
                        options=options)
        if filename:
            self.filestate.set_file_name( filename )
            self.refresh_UI()

    def on_save_dir_browse_btn_click(self):
        """
        when save dir browse button is clicked.
        TODO: is there a way to smartly combine this with on_open_file_browse_btn_click?
        ANSWER: yes, with self.sender(), but doing it in separate methods is ok
        """
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly
        savedir = QFileDialog.getExistingDirectory(
                        self,
                        "Select Save Directory",
                        ".",
                        options=options)
        if savedir:
            self.filestate.set_save_dir( savedir )
            self.refresh_UI()


    def check_paths(self):
        """
        used when enter is pressed within either of the line edits (means 'Ok').
        check that the paths are valid.
        """
        filename = self.open_file_entry.text()
        savedir = self.save_dir_entry.text()

        if self.filestate.is_valid(filename) and savedir:
            self.filestate.set_file_name(filename)
            self.filestate.set_save_dir(savedir)
            self.refresh_UI()
            return True

        if not self.filestate.is_valid(filename):
            self.display_message("Invalid file type (must be .npy) or file does not exist.\n")
            self.open_file_entry.setText("")
            self.refresh_UI()

        if not savedir:
            self.display_message("You must specify a directory to save your work.\n")

        return False

    def on_ok_click(self):
        """
        when ok button is pressed, launch napari.
        """
        # check once more that the paths in the line edit are valid
        valid_paths = self.check_paths()
        if valid_paths:
            self.hide()
            root = tk.Tk()
            app = Application(self.filestate, root)
            ### TO DO:
            ### saving

            ### SOME ISSUES: related to napari mostly
            ### Q: when selecting a column what if some biondi bodies are overlapping between columns?
            ### Q: do we want it so that after annotating the flattened image, users anotate the vertical slices individually?

    def on_cancel_click(self):
        """
        when cancel button is pressed, close dialog.
        """
        self.close()

    def refresh_UI(self):
        self.open_file_entry.setText(self.filestate.get_file_name())
        self.save_dir_entry.setText(self.filestate.get_save_dir())
    
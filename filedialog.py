import sys
from PyQt5.QtWidgets import *
from filestate import FileState
import numpy as np
import napari
# import tkinter as tk
from app import Application

class FileDialog(QDialog):
    def __init__(self, parent=None, existing_case=False):
        super().__init__(parent)

        self.parent = parent
        self.existing_case = existing_case

        self.filestate = FileState(self.existing_case)

        # text
        self.title = "Initialize a Case"
        if self.existing_case: self.title = "Continue an Existing Case"
        
        # properties
        self.x = 300
        self.y = 300
        self.width = 400
        self.height = 150
        
        # layouts
        self.dlg_layout = QVBoxLayout()
        self.source_img_layout = QHBoxLayout()
        # self.save_dir_layout = QHBoxLayout()
        self.sink_db_layout = QHBoxLayout()
        self.form_layout = QFormLayout()

        # line edit
        self.source_img_entry = QLineEdit()
        # self.save_dir_entry = QLineEdit()
        self.sink_db_entry = QLineEdit()
        
        # buttons
        self.source_img_browse_btn = QPushButton("Browse")
        # self.save_dir_browse_btn = QPushButton("Browse")
        self.sink_db_browse_btn = QPushButton("Browse")
        self.dlg_btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # if continuing an existing case
        if self.existing_case:
            self.source_db_layout = QHBoxLayout()
            self.source_db_entry = QLineEdit()
            self.source_db_browse_btn = QPushButton("Browse")

        # initialize UI
        self.init_UI()

    def init_UI(self):
        """
        Initialize text/buttons for the main window.
        """
        # buttons
        self.dlg_btns.setDefaultButton(QDialogButtonBox.Ok)
        self.dlg_btns.accepted.connect(self.on_ok_click)
        self.dlg_btns.rejected.connect(self.on_cancel_click)
        self.source_img_browse_btn.clicked.connect(self.on_source_img_browse_btn_click)
        # self.save_dir_browse_btn.clicked.connect(self.on_save_dir_browse_btn_click)
        self.sink_db_browse_btn.clicked.connect(self.on_sink_db_browse_btn_click)

        # line edits
        # self.source_img_entry.returnPressed.connect(self.on_open_file_enter)
        # self.save_dir_entry.returnPressed.connect(self.on_save_dir_enter)

        # layouts
        self.source_img_layout.addWidget(self.source_img_entry)
        self.source_img_layout.addWidget(self.source_img_browse_btn)

        # self.save_dir_layout.addWidget(self.save_dir_entry)
        # self.save_dir_layout.addWidget(self.save_dir_browse_btn)

        self.sink_db_layout.addWidget(self.sink_db_entry)
        self.sink_db_layout.addWidget(self.sink_db_browse_btn)
        
        self.form_layout.addRow("Image Array Path (.npy): ", self.source_img_layout)
        # if continuing an existing case
        if self.existing_case:
            self.source_db_browse_btn.clicked.connect(self.on_source_db_browse_btn_click)
            self.source_db_layout.addWidget(self.source_db_entry)
            self.source_db_layout.addWidget(self.source_db_browse_btn)
            self.form_layout.addRow("Source Database Path (.db)")
        # self.form_layout.addRow("Save Folder: ", self.save_dir_layout)
        self.form_layout.addRow("Save Database Path: ", self.sink_db_layout)

        self.dlg_layout.addLayout(self.form_layout)
        self.dlg_layout.addWidget(self.dlg_btns)


        # set file dialog properties
        self.setLayout(self.dlg_layout)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle(self.title)

    def display_warning_message(self, msg):
        """
        displays msg in message box widget.
        """
        # mbox = QMessageBox()
        # mbox.setWindowTitle("Warning")
        # mbox.setText(msg)
        # mbox.setIcon(QMessageBox.Warning)
        # mbox.exec()
        reply = QMessageBox.warning(self, 'Warning', msg,
                QMessageBox.Ok, QMessageBox.Ok)

    def display_yes_no_message(self, msg):
        reply = QMessageBox.question(self, 'Window Close', msg,
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def on_sink_db_browse_btn_click(self):
        '''
        when sink database browse button is clicked.
        '''
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog
        sink_db_filename, _ = QFileDialog.getOpenFileName(
                        self,
                        "Select Sink Database File",
                        ".",
                        "Database Files (*.db)",
                        options=options)

        if sink_db_filename:
            self.filestate.set_sink_db_filename( sink_db_filename )
            self.refresh_UI()


    def on_source_db_browse_btn_click(self):
        '''
        when source database browse button is clicked.
        '''
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog
        source_db_filename, _ = QFileDialog.getOpenFileName(
                        self,
                        "Select Source Database File",
                        ".",
                        "Database Files (*.db)",
                        options=options)
        if source_db_filename:
            self.filestate.set_source_db_filename( source_db_filename )
            self.refresh_UI()

    def on_source_img_browse_btn_click(self):
        """
        when open file browse button is clicked.
        """
        options = QFileDialog.Options() 
        options |= QFileDialog.DontUseNativeDialog
        source_img_filename, _ = QFileDialog.getOpenFileName(
                        self,
                        "Select Input Numpy Array",
                        ".",
                        "NumPy Files (*.npy)",
                        options=options)
        if source_img_filename:
            self.filestate.set_source_img_filename( source_img_filename )
            self.refresh_UI()

    # def on_save_dir_browse_btn_click(self):
    #     """
    #     when save dir browse button is clicked.
    #     TODO: is there a way to smartly combine this with on_source_img_browse_btn_click?
    #     ANSWER: yes, with self.sender(), but doing it in separate methods is ok
    #     """
    #     options = QFileDialog.Options() 
    #     options |= QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly
    #     savedir = QFileDialog.getExistingDirectory(
    #                     self,
    #                     "Select Save Directory",
    #                     ".",
    #                     options=options)
    #     if savedir:
    #         self.filestate.set_save_dir( savedir )
    #         self.refresh_UI()


    def check_paths(self):
        """
        used when enter is pressed within either of the line edits (means 'Ok').
        check that the paths are valid.
        """
        source_img_filename = self.source_img_entry.text()
        sink_db_filename = self.sink_db_entry.text()
        source_db_filename = ""

        source_img_filename_valid = self.filestate.is_valid(source_img_filename, ".npy")
        sink_db_filename_valid = self.filestate.is_valid(sink_db_filename, ".db")
        source_db_filename_valid = True
        
        all_paths_valid = source_img_filename_valid and sink_db_filename_valid 

        if self.existing_case:
            source_db_filename = self.source_db_entry.text()
            source_db_filename_valid = self.filestate.is_valid(source_db_filename, ".db")
            all_paths_valid = all_paths_valid and source_db_filename_valid
        
        if all_paths_valid:
            self.filestate.set_source_img_filename(source_img_filename)
            self.filestate.set_sink_db_filename(sink_db_filename)
            if self.existing_case:
                self.filestate.set_source_db_filename(source_db_filename)
            self.refresh_UI()
            return True

        if not source_img_filename_valid:
            self.display_warning_message("Invalid image file type (must be .npy) or file does not exist.\n")
            self.filestate.set_source_img_filename("")
        if not sink_db_filename_valid:
            self.display_warning_message("Invalid database file type (must be .db) or file does not exist.\n")
            self.filestate.set_sink_db_filename("")
        if self.existing_case and not source_db_filename_valid:
            self.display_warning_message("Invalid database file type (must be .db) or file does not exist.\n")
            self.filestate.set_source_db_filename("")

        self.refresh_UI()
        return False

        # reply = self.display_yes_no_message("If you chose an existing .db file, it will be overwritten. Do you wish to proceed?")

        # source_img_filename = self.source_img_entry.text()
        # # savedir = self.save_dir_entry.text()
        # save_db_name = self.sink_db_entry.text()
        # source_db_name = None

        # source_img_filename_valid = self.filestate.is_valid(source_img_filename, ".npy")


        # all_inputs_good = source_img_filename_valid and self.filestate.check_save_db(save_db_name) and savedir
        # if self.existing_case:
        #     source_db_name = self.source_db_entry.text()
        #     all_inputs_good = self.filestate.is_valid(source_db_name, ".db") and source_img_filename_valid and self.filestate.check_save_db(save_db_name) and savedir

        # if all_inputs_good:
        #     self.filestate.set_file_name(filename)
        #     self.filestate.set_save_dir(savedir)
        #     self.filestate.set_save_db_name(save_db_name)
        #     if self.existing_case: self.filestate.set_source_db(source_db_name)
        #     self.refresh_UI()
        #     return True

        # if not self.filestate.is_valid(filename):
        #     self.display_warning_message("Invalid image file type (must be .npy) or file does not exist.\n")
        #     self.filestate.set_file_name("")

        # if not savedir:
        #     self.display_warning_message("You must specify a directory to save your work.\n")
        #     self.filestate.set_save_dir("")

        # if self.existing_case and not self.filestate.is_valid(source_db_name, ".db"):
        #     self.display_warning_message("Invalid source database file type (must be .db) or file does not exist or data is in wrong format.\n")
        #     self.filestate.set_source_db(source_db_name)

        # self.refresh_UI()
        # return False

    def on_ok_click(self):
        """
        when ok button is pressed, launch app.
        """
        # check once more that the paths in the line edit are valid
        valid_paths = self.check_paths()
        if valid_paths:
            valid_paths = self.display_yes_no_message("If you chose an existing .db file, it will be overwritten. Do you wish to proceed?")

        if valid_paths:
            self.hide()
            # root = tk.Tk()
            self.app = Application(self.filestate, self.existing_case)
            self.app.showMaximized()
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
        """
        resets the text in the line edits, effectively "refreshing" the UI state.
        """
        self.source_img_entry.setText(self.filestate.get_source_img_filename())
        # self.save_dir_entry.setText(self.filestate.get_save_dir())
        self.sink_db_entry.setText(self.filestate.get_sink_db_filename())
        if self.existing_case: self.source_db_entry.setText(self.filestate.get_source_db_filename())    
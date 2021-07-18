from PyQt5.QtWidgets import *
from filestate import FileState
import numpy as np
from app import Application
import os
import re

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
        self.sink_dir_layout = QHBoxLayout()
        self.sink_db_name_layout = QHBoxLayout()
        self.form_layout = QFormLayout()

        # line edit
        self.source_img_entry = QLineEdit()
        self.sink_dir_entry = QLineEdit()
        self.sink_db_name_entry = QLineEdit()
        
        # buttons
        self.source_img_browse_btn = QPushButton("Browse")
        self.sink_dir_browse_btn = QPushButton("Browse")
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
        self.dlg_btns.accepted.connect(self.on_ok_click)
        self.dlg_btns.rejected.connect(self.on_cancel_click)
        self.source_img_browse_btn.clicked.connect(self.on_source_img_browse_btn_click)
        # self.save_dir_browse_btn.clicked.connect(self.on_save_dir_browse_btn_click)
        self.sink_dir_browse_btn.clicked.connect(self.on_sink_dir_browse_btn_click)

        # layouts
        self.source_img_layout.addWidget(self.source_img_entry)
        self.source_img_layout.addWidget(self.source_img_browse_btn)

        self.sink_dir_layout.addWidget(self.sink_dir_entry)
        self.sink_dir_layout.addWidget(self.sink_dir_browse_btn)

        self.sink_db_name_layout.addWidget(self.sink_db_name_entry)
        
        self.form_layout.addRow("Image Array Path (.npy): ", self.source_img_layout)
        # if continuing an existing case
        if self.existing_case:
            self.source_db_browse_btn.clicked.connect(self.on_source_db_browse_btn_click)
            self.source_db_layout.addWidget(self.source_db_entry)
            self.source_db_layout.addWidget(self.source_db_browse_btn)
            self.form_layout.addRow("Source Database Path (.db): ", self.source_db_layout)
        self.form_layout.addRow("Sink Directory (folder): ", self.sink_dir_layout)
        self.form_layout.addRow("Sink Database Name: ", self.sink_db_name_layout)

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
        reply = QMessageBox.warning(self, 'Warning', msg,
                QMessageBox.Ok, QMessageBox.Ok)

    def display_yes_no_message(self, msg):
        reply = QMessageBox.question(self, 'Warning', msg,
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def on_sink_dir_browse_btn_click(self):
        '''
        when sink dir browse button is clicked.
        '''
        dlg = QFileDialog()
        options = dlg.Options() 
        options |= QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly
        sink_dir = dlg.getExistingDirectory(
                        self,
                        "Select Sink Directory",
                        ".",
                        options=options)

        if sink_dir:
            self.filestate.set_sink_dir_name( sink_dir )
            self.refresh_UI()


    def on_source_db_browse_btn_click(self):
        '''
        when source database browse button is clicked.
        '''
        dlg = QFileDialog()
        options = dlg.Options() 
        options |= QFileDialog.DontUseNativeDialog
        source_db_filename, _ = dlg.getOpenFileName(
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
        dlg = QFileDialog()
        options = dlg.Options() 
        options |= QFileDialog.DontUseNativeDialog
        source_img_filename, _ = dlg.getOpenFileName(
                        self,
                        "Select Input Numpy Array",
                        ".",
                        "NumPy Files (*.npy)",
                        options=options)
        if source_img_filename:
            self.filestate.set_source_img_filename( source_img_filename )
            self.refresh_UI()


    def check_paths(self):
        """
        check that the paths are valid.
        """
        source_img_filename = self.source_img_entry.text()
        sink_dir_name = self.sink_dir_entry.text()
        sink_db_name_entry_text = self.sink_db_name_entry.text()
        db_ext = ".db" if not sink_db_name_entry_text.lower().endswith(".db") else ""
        sink_db_filename = os.path.join(sink_dir_name, sink_db_name_entry_text + db_ext) 
        source_db_filename = ""

        # print("source img filename: ", source_img_filename)
        # print("sink dir name: ", sink_dir_name)
        # print("sink db filename: ", sink_db_filename)

        source_img_filename_valid = self.filestate.is_valid(source_img_filename, ".npy")
        sink_dir_name_valid = self.filestate.is_valid(sink_dir_name, None)
        sink_db_filename_valid = self.filestate.is_valid(sink_db_filename, ".db")
        source_db_filename_valid = True
        
        # check source img valid: if it's an existing file, return True; else, return False
        # check sink dir valid: if it's an existing dir, then return True; else, return False (user has to create it already)
        # check sink db: if it's an existing db, return True; else, create db and return True
        all_paths_valid = source_img_filename_valid and sink_dir_name_valid and sink_db_filename_valid

        if self.existing_case:
            # print('checking if source db filename is valid')
            source_db_filename = self.source_db_entry.text()
            # print("source db filename: ", source_db_filename)
            source_db_filename_valid = self.filestate.is_valid(source_db_filename, ".db")
            all_paths_valid = all_paths_valid and source_db_filename_valid
        
        if all_paths_valid:
            # print("all paths are valid")
            self.filestate.set_source_img_filename(source_img_filename)
            self.filestate.set_sink_dir_name(sink_dir_name)
            self.filestate.set_sink_db_filename(sink_db_filename)
            if self.existing_case:
                self.filestate.set_source_db_filename(source_db_filename)
            self.refresh_UI()
            return True

        if not source_img_filename_valid:
            # print("source img filename invalid")
            self.display_warning_message("Invalid image file type (must be .npy) or file does not exist.\n")
            self.filestate.set_source_img_filename("")
        if not source_db_filename_valid: # only if existing case
            # print("source db filename invalid")
            self.display_warning_message("Invalid source database file type (must be .db) or file does not exist.\n")
            self.filestate.set_source_db_filename("")
        if not sink_dir_name_valid:
            # print("sink dir name invalid")
            self.display_warning_message("Invalid sink directory or directory does not exist.\n")
            self.filestate.set_sink_dir_name("")
        if not sink_db_filename_valid: # if the sink db is invalid and it's not because its something like ".db" or " .db"
            if sink_dir_name_valid and not re.match(r" *.db", sink_db_filename) and self.display_yes_no_message("Create file at " + sink_db_filename + "?"):
                # create file with read write permissions
                sink_db_file = open(sink_db_filename, "w+")
                sink_db_file.close()
                # set sink db filename
                self.filestate.set_sink_db_filename(sink_db_filename)
                self.refresh_UI()
                return True
            else:
                # print("sink db filename invalid")
                self.display_warning_message("Invalid sink database file type (must be .db) or file does not exist. Be sure to specify a name for the sink database.\n")
                self.filestate.set_sink_db_filename("")

        # print("paths invalid")
        self.refresh_UI()
        return False

    def on_ok_click(self):
        """
        when ok button is pressed, launch app.
        """
        # check once more that the paths in the line edit are valid
        valid_paths = self.check_paths()
        if valid_paths:
            valid_paths = self.display_yes_no_message("If you chose an existing .db file as a sink, it will be overwritten. If you are initiating a new case, the specified sink .db file will be replaced. Do you wish to proceed?")

        if valid_paths:
            self.hide()
            self.app = Application(self.filestate, self.existing_case)
            self.app.showMaximized()

    def on_cancel_click(self):
        """
        when cancel button is pressed, close dialog.
        """
        # self.parent.show()
        self.close()

    def refresh_UI(self):
        """
        resets the text in the line edits, effectively "refreshing" the UI state.
        """
        self.source_img_entry.setText(self.filestate.get_source_img_filename())
        self.sink_dir_entry.setText(self.filestate.get_sink_dir_name())
        self.sink_db_name_entry.setText(self.filestate.get_sink_db_filename())
        if self.existing_case: self.source_db_entry.setText(self.filestate.get_source_db_filename())    
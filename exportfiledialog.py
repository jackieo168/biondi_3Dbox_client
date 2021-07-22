import os
from messages import *
from PyQt5.QtWidgets import *
from pathlib import Path
import re

"""
The dialog for file browsing for export csv location.
"""


class ExportFileDialog(QDialog):
    def __init__(self, sink_db, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.sink_db = sink_db
        self.export_csv_dir = ""
        self.export_csv_path = ""

        # text
        self.title = "Export Annotations as .csv"

        # properties
        self.x = 300
        self.y = 300
        self.width = 400
        self.height = 150

        # layouts
        self.dlg_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.export_csv_dir_layout = QHBoxLayout()
        self.export_csv_name_layout = QHBoxLayout()

        # line edit
        self.export_csv_dir_entry = QLineEdit()
        self.export_csv_name_entry = QLineEdit()

        # buttons
        self.export_csv_dir_browse_btn = QPushButton("Browse")
        self.dlg_btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # initialize UI
        self.init_UI()

    def init_UI(self):
        """
        Initialize text/buttons for the file dialog.
        """
        # buttons
        self.dlg_btns.accepted.connect(self.on_ok_click)
        self.dlg_btns.rejected.connect(self.on_cancel_click)
        self.export_csv_dir_browse_btn.clicked.connect(self.on_export_csv_path_browse_btn_click)

        # layouts
        self.export_csv_dir_layout.addWidget(self.export_csv_dir_entry)
        self.export_csv_dir_layout.addWidget(self.export_csv_dir_browse_btn)

        self.export_csv_name_layout.addWidget(self.export_csv_name_entry)

        self.form_layout.addRow("Destination directory (folder): ", self.export_csv_dir_layout)
        self.form_layout.addRow(".csv File Name: ", self.export_csv_name_layout)

        self.dlg_layout.addLayout(self.form_layout)
        self.dlg_layout.addWidget(self.dlg_btns)

        # set file dialog properties
        self.setLayout(self.dlg_layout)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle(self.title)

    def on_export_csv_path_browse_btn_click(self):
        """
        when browse button clicked
        """
        dlg = QFileDialog()
        options = dlg.Options()
        options |= QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly
        export_dir = dlg.getExistingDirectory(
            self,
            "Select Export .csv Directory",
            ".",
            options=options
        )

        if export_dir:
            self.export_csv_dir = export_dir
            self.refresh_UI()

    def on_ok_click(self):
        """
        when ok is clicked.
        """
        # get line edit text
        export_csv_dir = self.export_csv_dir_entry.text().replace("\\", "/")
        export_csv_name_entry_text = self.export_csv_name_entry.text()
        csv_ext = ".csv" if not export_csv_name_entry_text.lower().endswith(".csv") else ""
        export_csv_path = os.path.join(export_csv_dir, export_csv_name_entry_text + csv_ext).replace("\\", "/")

        dir_path_obj = Path(export_csv_dir)
        csv_path_obj = Path(export_csv_path)

        dir_exists = dir_path_obj.exists()
        dir_is_dir = dir_path_obj.is_dir()

        csv_exists = csv_path_obj.exists() and csv_path_obj.is_file()
        csv_format_valid = export_csv_path.lower().endswith(".csv") and not re.match(r'\S*\/ *.csv', export_csv_path)

        dir_valid = dir_exists and dir_is_dir
        csv_valid = csv_exists and csv_format_valid

        valid = dir_valid and csv_valid

        if valid:
            self.export_csv_dir = export_csv_dir
            self.export_csv_path = export_csv_path
            self.refresh_UI()
            if csv_exists:
                valid = display_yes_no_message(self, "Provided .csv file already exists. Replace?")
        if valid:  # still
            self.sink_db.export_as_csv(self.export_csv_path)
            self.close()

        if not dir_valid:
            if not dir_exists:
                display_warning_message(self, "Provided directory does not exist.")
            elif not dir_is_dir:
                display_warning_message(self, "Provided directory format is invalid.")
            self.export_csv_dir = ""
        if not csv_valid:
            if dir_valid and not csv_exists and csv_format_valid and \
                    display_yes_no_message(self, "Create file at " + export_csv_path + "?"):
                try:
                    csv_file = open(export_csv_path, "w+")
                    csv_file.close()
                except IOError as error:
                    display_warning_message(self, "Failed to create provided .csv file: " + export_csv_path)
                else:
                    self.export_csv_path = export_csv_path
                    self.refresh_UI()
                    return
            elif not csv_format_valid:
                display_warning_message(self, "Be sure to specify a name for the .csv file.")
            self.export_csv_path = ""

        self.refresh_UI()

    def refresh_UI(self):
        """
        refresh the line edits.
        """
        self.export_csv_dir_entry.setText(self.export_csv_dir)
        self.export_csv_name_entry.setText(self.export_csv_path)

    def on_cancel_click(self):
        """
        when cancel is clicked.
        """
        self.close()

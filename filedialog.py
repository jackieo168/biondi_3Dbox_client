from filestate import FileState
from app import Application
import os
from messages import *
from constants import *
from PyQt5.QtWidgets import *

"""
The dialog for file browsing. Instantiated upon clicking a button in the opening window.
For 'Initiate New Case', file dialog contains source image entry, sink directory entry, and sink database name entry.
For 'Continue Existing Case', file dialog contains the same with the addition of source database entry.

Upon ok, file paths are checked. If valid, the main annotation application is opened.
"""


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

	def check_line_edits_and_refresh_filestate(self):
		"""
		check line edits for modifications and refresh the filestate accordingly.
		called on clicks to the browse buttons and ok, before refreshing UI.
		can be thought of in conjunction with refresh_UI().
		"""
		# line edit changes (other places where filestate is updated: browse button clicks, ok click)
		if self.source_img_entry.isModified():
			self.filestate.set_source_img_filename(self.source_img_entry.text().replace("\\", "/"))
		if self.existing_case and self.source_db_entry.isModified():
			self.filestate.set_source_db_filename(self.source_db_entry.text().replace("\\", "/"))
		if self.sink_dir_entry.isModified():
			self.filestate.set_sink_dir_name(self.sink_dir_entry.text().replace("\\", "/"))

	#################
	# BUTTON EVENTS #
	#################

	def on_sink_dir_browse_btn_click(self):
		"""
		when sink dir browse button is clicked.
		"""
		dlg = QFileDialog()
		options = dlg.Options()
		options |= QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly
		sink_dir = dlg.getExistingDirectory(
			self,
			"Select Sink Directory",
			".",
			options=options)

		if sink_dir:
			self.filestate.set_sink_dir_name(sink_dir)
			self.check_line_edits_and_refresh_filestate()
			self.refresh_UI()

	def on_source_db_browse_btn_click(self):
		"""
		when source database browse button is clicked.
		"""
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
			self.filestate.set_source_db_filename(source_db_filename)
			self.check_line_edits_and_refresh_filestate()
			self.refresh_UI()

	def on_source_img_browse_btn_click(self):
		"""
		when source file browse button is clicked.
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
			self.filestate.set_source_img_filename(source_img_filename)
			self.check_line_edits_and_refresh_filestate()
			self.refresh_UI()

	############
	# OK CLICK #
	############

	def check_paths(self):
		"""
		check that the paths are valid and refresh the filestate and UI when necessary.
		"""
		self.check_line_edits_and_refresh_filestate()
		# paths
		source_img_filename = self.source_img_entry.text().replace("\\", "/")
		sink_dir_name = self.sink_dir_entry.text().replace("\\", "/")
		sink_db_name_entry_text = self.sink_db_name_entry.text()
		db_ext = ".db" if not sink_db_name_entry_text.lower().endswith(".db") else ""
		sink_db_filename = os.path.join(sink_dir_name, sink_db_name_entry_text + db_ext).replace("\\", "/")
		source_db_filename = ""

		# check validity
		source_img_filename_valid = self.filestate.is_valid(source_img_filename, SOURCE_IMG)
		sink_dir_name_valid = self.filestate.is_valid(sink_dir_name, SINK_DIR)
		sink_db_filename_valid = self.filestate.is_valid(sink_db_filename, SINK_DB)
		source_db_filename_valid = True

		all_paths_valid = source_img_filename_valid and sink_dir_name_valid and sink_db_filename_valid

		if self.existing_case:
			source_db_filename = self.source_db_entry.text()
			source_db_filename_valid = self.filestate.is_valid(source_db_filename, SOURCE_DB)
			all_paths_valid = all_paths_valid and source_db_filename_valid

		if all_paths_valid:
			self.filestate.set_source_img_filename(source_img_filename)
			self.filestate.set_sink_dir_name(sink_dir_name)
			self.filestate.set_sink_db_filename(sink_db_filename)
			if self.existing_case:
				self.filestate.set_source_db_filename(source_db_filename)
			self.refresh_UI()
			return True

		# in the case of invalidity
		if not source_img_filename_valid:
			if not self.filestate.source_img_file_exists:
				display_warning_message(self, "Provided source image file at does not exist.")
			elif not self.filestate.source_img_file_format_valid:
				display_warning_message(self, "Provided source image file type is invalid (must be .npy).")
			self.filestate.set_source_img_filename("")
		if not source_db_filename_valid:  # only if existing case
			if not self.source_db_file_exists:
				display_warning_message(self, "Provided source database file does not exist.")
			elif not self.filestate.source_db_file_format_valid:
				display_warning_message(self, "Provided source database file type is invalid (must be .db)")
			self.filestate.set_source_db_filename("")
		if not sink_dir_name_valid:
			if not self.filestate.sink_dir_exists:
				display_warning_message(self, "Provided sink directory does not exist.")
			elif not self.sink_dir_format_valid:
				display_warning_message(self, "Provided sink directory format is invalid.")
			self.filestate.set_sink_dir_name("")
		if not sink_db_filename_valid:
			if sink_dir_name_valid and not self.filestate.sink_db_file_preexists and \
					self.filestate.sink_db_file_format_valid and \
					display_yes_no_message(self, "Create file at " + sink_db_filename + "?"):
				# create file with read write permissions
				###########################################
				try:
					sink_db_file = open(sink_db_filename, "w+")
					sink_db_file.close()
				except IOError as error:
					display_warning_message(self, "Failed to create provided sink database file: " + error)
				###########################################
				# set sink db filename
				else:
					self.filestate.set_sink_db_filename(sink_db_filename)
					self.refresh_UI()
					return True
			elif not self.filestate.sink_db_file_format_valid:
				display_warning_message(self, "Be sure to specify a name for the sink database.")
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
			if self.existing_case:
				if self.filestate.get_source_db_filename() != self.filestate.get_sink_db_filename():
					valid_paths = display_yes_no_message(self,
														 "Sink database is different from source database. Any new "
														 "annotations you add will be added to the sink database "
														 "only. Proceed?")
				else:
					valid_paths = display_yes_no_message(self,
														 "Sink database is the same as source database. Source "
														 "database will be modified. Proceed?")
			elif self.filestate.sink_db_file_preexists:
				valid_paths = display_yes_no_message(self,
													 "Sink database already exists and will be cleared of any table "
													 "named \'annotations\' before being used. Proceed?")

		if valid_paths:  # still
			self.hide()
			self.app = Application(filestate=self.filestate, parent=self, existing_case=self.existing_case)
			self.app.showMaximized()

	################
	# CANCEL CLICK #
	################

	def on_cancel_click(self):
		"""
		when cancel button is pressed, close dialog.
		"""
		# self.parent.show()
		self.close()

	##############
	# REFRESH UI #
	##############

	def refresh_UI(self):
		"""
		resets the text in the line edits, effectively "refreshing" the UI state.
		"""
		self.source_img_entry.setText(self.filestate.get_source_img_filename())
		self.sink_dir_entry.setText(self.filestate.get_sink_dir_name())
		self.sink_db_name_entry.setText(self.filestate.get_sink_db_filename())
		if self.existing_case: self.source_db_entry.setText(self.filestate.get_source_db_filename())

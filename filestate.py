from constants import *
"""
The filestate.
Contains information on the source img file path, source db file path,
sink db file path, and sink dir path of the currently running application.
"""


class FileState:
	def __init__(self, existing_case=False):
		"""
		Initializes the filename and save directory
		"""
		self.source_img_filename = ""
		self.source_db_filename = ""
		self.sink_dir_name = ""
		self.sink_db_filename = ""
		self.existing_case = existing_case

		self.source_img_file_exists = False
		self.source_img_file_format_valid = False
		self.source_db_file_exists = False
		self.source_db_file_format_valid = False
		self.sink_db_file_preexists = False
		self.sink_db_file_format_valid = False
		self.sink_dir_exists = False
		self.sink_dir_format_valid = False

	def is_valid(self, path, type=None):
		"""
		checks that the path specified is valid and sets appropriate filestate variables.
		"""
		path_obj = Path(path)
		exists = path_obj.exists()
		is_file = path_obj.is_file()
		is_dir = path_obj.is_dir()

		# check if sink dir valid. Should call is_valid on sink dir before calling on sink db.
		if type == SINK_DIR:
			self.sink_dir_exists = exists  # could be a file
			self.sink_dir_format_valid = is_dir
			return self.sink_dir_exists and self.sink_dir_format_valid

		# check cases for file
		if type == SOURCE_IMG:
			self.source_img_file_exists = exists and is_file
			self.source_img_file_format_valid = path.lower().endswith(".npy")
			return self.source_img_file_exists and self.source_img_file_format_valid
		if type == SOURCE_DB:
			self.source_db_file_exists = exists and is_file
			self.source_db_file_format_valid = path.lower().endswith(".db")
			return self.source_db_file_exists and self.source_db_file_format_valid
		if type == SINK_DB:
			self.sink_db_file_preexists = exists and is_file
			self.sink_db_file_format_valid = path.lower().endswith(".db") and not re.match(r'\S* *.db', path)
			return self.sink_db_file_preexists and self.sink_db_file_format_valid

		return False

	###################
	# GETTERS/SETTERS #
	###################

	def set_sink_db_filename(self, sink_db_filename):
		self.sink_db_filename = sink_db_filename

	def set_source_db_filename(self, source_db_filename):
		self.source_db_filename = source_db_filename

	def set_source_img_filename(self, source_img_filename):
		self.source_img_filename = source_img_filename

	def set_sink_dir_name(self, sink_dir_name):
		self.sink_dir_name = sink_dir_name

	def get_sink_db_filename(self):
		return self.sink_db_filename

	def get_source_db_filename(self):
		return self.source_db_filename

	def get_source_img_filename(self):
		return self.source_img_filename

	def get_sink_dir_name(self):
		return self.sink_dir_name

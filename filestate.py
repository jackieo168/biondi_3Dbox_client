# the Model
from pathlib import Path

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

	def is_valid(self, path, extension):
		"""
		returns True if the path refers to an existing file with extension
		or existing directory.
		"""
		path_obj = Path(path)
		exists = path_obj.exists()
		is_file = path_obj.is_file()
		is_dir = path_obj.is_dir()
		if exists and is_file:
			return path.lower().endswith(extension)
		else:
			return exists and is_dir

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
# the Model

class FileState:
	def __init__(self, existing_case=False):
		"""
		Initializes the filename and save directory
		"""
		self.filename = None
		self.savedir = None
		self.source_db_name = None 
		self.save_db_name = None
		self.existing_case = existing_case

	def is_valid(self, filename, extension):
		"""
		returns True if the file exists and can be
		opened.  Returns False otherwise.
		"""
		try: 
			file = open( filename, 'r' )
			file.close()
			return True and filename.lower().endswith(extension)
		except:
			return False

	def set_file_name( self, filename ):
		'''
		sets the member filename to the value of the argument
		if the file exists.  Otherwise resets the filename.
		'''
		if self.is_valid( filename ):
			self.filename = filename
		else:
			self.filename = None
            
	def get_file_name( self ):
		'''
		Returns the name of the file name member.
		'''
		return self.filename

	def set_save_dir(self, savedir):
		'''
		sets the the member savedir to the value of the argument.
		'''
		self.savedir = savedir

	def get_save_dir(self):
		'''
		Returns the name of the save directory member.
		'''
		return self.savedir
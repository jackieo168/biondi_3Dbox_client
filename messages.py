from PyQt5.QtWidgets import *

def display_warning_message(parent, msg):
	"""
	displays warning msg in message box widget.
	"""
	reply = QMessageBox.warning(parent, 'Warning', msg, 
				QMessageBox.Ok, QMessageBox.Ok)

def display_yes_no_message(parent, msg):
	'''
	displays yes/no question msg in message box widget.
	returns True if Yes clicked, False o.w.
	'''
	reply = QMessageBox.question(parent, 'Warning', msg,
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
	if reply == QMessageBox.Yes:
		return True
	else:
		return False
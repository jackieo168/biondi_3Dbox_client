# import tkinter as tk 
# from tkinter import ttk
# from PIL import Image, ImageTk
import os
import numpy as np

# importing Qt widgets
from PyQt5.QtWidgets import * 
import sys
  
# importing pyqtgraph as pg
import pyqtgraph as pg
from PyQt5.QtGui import *

class Application(QWidget):
	def __init__(self, filestate):
		super().__init__()
		self.filestate = filestate
		self.layout = QVBoxLayout()

		# text
		self.title = "3D Biondi Body Client"

		# properties
		self.x = 100
		self.y = 100
		self.width = 600
		self.height = 500

		# components (widgets)
		self.img_plot = pg.ImageView()

		# IMAGE ARRAY
		input_array = np.load(self.filestate.get_file_name())
		input_array = input_array/np.max(input_array)
		self.input_array_zmax = np.max(input_array, axis=0)

		# initialize UI
		self.init_UI()
		
	def init_UI(self):
		"""
		Initialize text/buttons for the main window.
		"""
		self.setWindowTitle(self.title)
		self.setGeometry(self.x, self.y, self.width, self.height)

		self.img_plot.setImage(self.input_array_zmax)
		self.layout.addWidget(self.img_plot)
		

		self.setLayout(self.layout)
		# self.img_plot.show()
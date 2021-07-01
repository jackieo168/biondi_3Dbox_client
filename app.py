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

from boundingbox import BoundingBox

class Application(QMainWindow):
	def __init__(self, filestate):
		super().__init__()
		self.filestate = filestate
		self.layout = QHBoxLayout()
		self.bbox_num = 0

		# text
		self.title = "3D Biondi Body Client"

		# properties
		self.x = 100
		self.y = 100
		self.width = 950
		self.height = 950

		# components (widgets)
		self.statusBar()
		self.central_widget = QWidget()
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
		# set up global config options for pyqtgraph
		# pg.setConfigOptions(imageAxisOrder='row-major')

		# set up central widget
		self.img_plot.setImage(self.input_array_zmax, autoRange=True, )
		self.layout.addWidget(self.img_plot)
		self.central_widget.setLayout(self.layout)
		self.central_widget.setMouseTracking(True)

		# set up window properties
		self.setWindowTitle(self.title)
		self.setGeometry(self.x, self.y, self.width, self.height)
		self.setCentralWidget(self.central_widget)

		self.img_plot_item = self.img_plot.getImageItem()
		# self.img_plot.scene.sigMouseClicked.connect(self.mousePressEvent)
		# pg.QtGui.QApplication.processEvents()
		# self.img_plot.sigMouseDrag.connect(mouseDragEvent)
		# self.img_plot.show() called by caller

	# override
	# def keyPressEvent(self, event):
	# 	# x = event.x()
	# 	# y = event.y()
	# 	# self.statusBar().showMessage('x= ' + str(x) + ', y= ' + str(y))
	# 	self.bbox_num += 1
		# self.latest_added_bbox = BoundingBox(self.bbox_num, self.input_array_zmax, self.img_plot, 0,0)
		# self.img_plot.addItem(self.latest_added_bbox.bbox)
		# self.latest_added_bbox.bbox.sigRegionChanged.connect(self.latest_added_bbox.getArraySlice)

	# def mouseHoverEvent(self, event):
	# 	mouse_pos = event.pos()
	# 	x = mouse_pos.x()
	# 	y = mouse_pos.y()
	# 	items = self.img_plot.scene.items(mouse_pos)
	# 	print(items)

	def mousePressEvent(self, event):
		self.statusBar().showMessage('bbox detected')
		mouse_pos = event.pos()
		x = mouse_pos.x()
		y = mouse_pos.y()
		items = self.img_plot.scene.items(mouse_pos)
		print(items)
		bboxes_at_cursor = [item for item in items if isinstance(item, BoundingBox)]
		# has_handle = any(isinstance(item, pg.graphicsItems.ROI.Handle) for item in items)
		if bboxes_at_cursor:
			self.statusBar().showMessage('bbox detected')
			bbox_at_cursor = bboxes_at_cursor[0] # always choose the top box
			bbox_at_cursor.sigRegionChanged.connect(bbox_at_cursor.get_array_slice)
		# if has_handle:
		# 	self.statusBar().showMessage('bbox handle detected')
		# else: # draw bbox
		# 	self.statusBar().showMessage('drawing bbox')
		# 	self.bbox_num += 1
		# 	added_bbox = BoundingBox(self.bbox_num, self.input_array_zmax, self.img_plot, x,y)
		# 	self.img_plot.addItem(added_bbox)
		# 	# added_bbox.sigRegionChanged.connect(added_bbox.get_array_slice)

	def keyPressEvent(self,event):
		self.statusBar().showMessage('bbox added')
		self.bbox_num += 1
		added_bbox = BoundingBox(self.bbox_num, self.input_array_zmax, self.img_plot, 0,0)
		self.img_plot.addItem(added_bbox)
		# added_bbox.sigRegionChanged.connect(added_bbox.get_array_slice)
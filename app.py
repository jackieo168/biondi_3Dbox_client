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
		self.central_widget = QWidget()
		self.status_bar = self.statusBar()

		# IMAGE ARRAY
		input_array = np.load(self.filestate.get_file_name())
		input_array = input_array/np.max(input_array)
		self.input_array_zmax = np.max(input_array, axis=0)

		# components cont'd (image plot widget)
		self.img_plot = pg.PlotItem()

		# initialize UI
		self.init_UI()
		
	def init_UI(self):
		"""
		Initialize text/buttons for the main window.
		"""
		# set up global config options for pyqtgraph
		# pg.setConfigOptions(imageAxisOrder='row-major')

		# set up central widget
		self.img_plot.enableAutoScale()		
		self.img_view = pg.ImageView(view=self.img_plot) # create image view widget with view as the image plot widget
		self.img_view.setImage(self.input_array_zmax) # set its image
		self.layout.addWidget(self.img_view) # add image view widget to layout
		self.central_widget.setLayout(self.layout)

		# set up window properties
		self.setWindowTitle(self.title)
		self.setGeometry(self.x, self.y, self.width, self.height)
		self.setCentralWidget(self.central_widget)

		# image view 
		self.img_view.scene.sigMouseClicked.connect(self.mouseClicked)
		self.img_view_item = self.img_view.getImageItem()
		
	def mouseHoverEvent(self, items):
		'''
		Just used to detect if an object is under the mouse.
		'''
		self.status_bar.showMessage('')
		obj_detected = any(not isinstance(item, pg.ImageItem) for item in items)
		if obj_detected:
			self.status_bar.showMessage('object detected')

	def mouseClicked(self, event):
		'''
		For adding bboxes or changing existing bboxes.
		'''
		self.status_bar.showMessage('')
		mouse_pos = event.scenePos()
		img_pos = self.img_view_item.mapFromScene(mouse_pos)
		x = img_pos.x()
		y = img_pos.y()
		items = self.img_view.scene.items(mouse_pos)
		print(items)
		bboxes_at_cursor = [item for item in items if isinstance(item, BoundingBox)]
		if bboxes_at_cursor:
			self.status_bar.showMessage('bbox detected')
		else:
			self.statusBar().showMessage('adding bbox')
			self.bbox_num += 1
			added_bbox = BoundingBox(self.bbox_num, self.input_array_zmax, self.img_view, x,y)
			self.img_view.addItem(added_bbox)
			added_bbox.sigRegionChanged.connect(added_bbox.get_array_slice)
			added_bbox.sigRemoveRequested.connect(self.remove_item_from_plot)

	def remove_item_from_plot(self):
		self.img_plot.removeItem(self.sender())


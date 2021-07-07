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
		self.layout = QGridLayout()
		self.bbox_num = 0
		self.latest_clicked_bbox = None
		self.side_view_mode = 0 # 1 or 2 depending on orientation, 0 if selector not clicked

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
		self.change_side_view_btn = QPushButton('Change Side View')

		# IMAGE ARRAY
		self.input_array = np.load(self.filestate.get_file_name())
		self.input_array = self.input_array/np.max(self.input_array)
		self.input_array_zmax = np.max(self.input_array, axis=0)

		# components cont'd (image plot widget)
		self.img_plot = pg.PlotItem()
		self.top_view_plot = pg.PlotItem()
		self.top_scan_view_plot = pg.PlotItem()
		self.side_view_plot = pg.PlotItem()

		# initialize UI
		self.init_UI()
		
	def init_UI(self):
		"""
		Initialize text/buttons for the main window.
		"""
		# set up global config options for pyqtgraph
		pg.setConfigOptions(imageAxisOrder='row-major')

		# set up central widget
		self.img_plot.enableAutoScale()		
		self.img_view = pg.ImageView(view=self.img_plot) # create image view widget with view as the image plot widget
		self.img_view.setImage(self.input_array_zmax) # set its image
		
		self.top_view_plot.enableAutoScale()
		self.top_img_view = pg.ImageView(view=self.top_view_plot)

		self.top_scan_view_plot.enableAutoScale()
		self.top_scan_img_view = pg.ImageView(view=self.top_scan_view_plot)

		self.side_view_plot.enableAutoScale()
		self.side_img_view = pg.ImageView(view=self.side_view_plot)

		# add to layout
		self.layout.addWidget(self.img_view, 0, 0, 2, 2)
		self.layout.addWidget(self.top_img_view, 0, 2, 1, 1)
		self.layout.addWidget(self.top_scan_img_view, 1, 2, 1, 1)
		self.layout.addWidget(self.side_img_view, 0, 3, 2, 1)
		self.layout.addWidget(self.change_side_view_btn,2 ,3)

		self.central_widget.setLayout(self.layout)

		# set up window properties
		self.setWindowTitle(self.title)
		self.setGeometry(self.x, self.y, self.width, self.height)
		self.setCentralWidget(self.central_widget)

		# image view 
		self.img_view.scene.sigMouseClicked.connect(self.mouseClicked)
		self.img_view_item = self.img_view.getImageItem()

		# buttons
		self.change_side_view_btn.clicked.connect(self.change_side_view_btn_clicked)
		
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
		For adding bboxes or changing existing bboxes in the main image view.
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
			self.latest_clicked_bbox = bboxes_at_cursor[0] # take top-most bbox
			self.latest_clicked_bbox.get_array_slice()
			row_start = self.latest_clicked_bbox.row_start 
			row_end = self.latest_clicked_bbox.row_end 
			col_start = self.latest_clicked_bbox.col_start 
			col_end = self.latest_clicked_bbox.col_end
			self.top_img_view.setImage(self.input_array_zmax[row_start:row_end,col_start:col_end,:])
			self.img_chunk = self.input_array[:,row_start:row_end,col_start:col_end,:]
			self.top_scan_img_view.setImage(self.img_chunk)
			self.side_view_1 = np.max(self.img_chunk, axis=1)
			self.side_view_2 = np.max(self.img_chunk, axis=2)
			self.side_view_mode = 1
			self.side_img_view.setImage(self.side_view_1)
		else:
			self.statusBar().showMessage('adding bbox')
			self.bbox_num += 1
			added_bbox = BoundingBox(self.bbox_num, self.input_array_zmax, self.img_view, x,y)
			self.img_view.addItem(added_bbox)
			added_bbox.sigRegionChanged.connect(added_bbox.get_array_slice)
			added_bbox.sigRemoveRequested.connect(self.remove_item_from_plot)

	def remove_item_from_plot(self):
		'''
		When the appropriate right click context menu item is selected, removes the 
		item from the main image plot.
		'''
		self.img_plot.removeItem(self.sender())

	def change_side_view_btn_clicked(self):
		'''
		Button to change side view of selected area.
		Does nothing if a selected area is not clicked on.
		'''
		if self.side_view_mode == 1:
			self.side_view_mode = 2
			self.side_img_view.setImage(self.side_view_2)
		elif self.side_view_mode == 2:
			self.side_view_mode = 1
			self.side_img_view.setImage(self.side_view_1)
		


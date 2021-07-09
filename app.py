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
		self.input_array_depth, self.input_array_height, self.input_array_width, self.input_array_num_ch = self.input_array.shape 
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

		# image items
		self.img_view_item = self.img_view.getImageItem() 

		# mouse events
		self.img_view.scene.sigMouseClicked.connect(self.main_plot_mouse_clicked)
		self.side_img_view.scene.sigMouseClicked.connect(self.side_view_plot_mouse_clicked)

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

	def main_plot_mouse_clicked(self, event):
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
		if bboxes_at_cursor: # SHOW THE DIFFERENT VIEWS FOR THE SELECTED DATA
			self.status_bar.showMessage('bbox detected')
			self.clear_top_and_side_views()
			self.latest_clicked_bbox = bboxes_at_cursor[0] # take top-most bbox
			self.refresh_top_and_side_views()
		else: # DRAW THE BBOX
			self.statusBar().showMessage('adding bbox')
			self.clear_top_and_side_views()
			self.draw_new_bbox(x, y)
			

	def draw_new_bbox(self, x, y):
		'''
		add a new bbox at specified x, y coordinates in main image view.
		'''
		self.bbox_num += 1
		added_bbox = BoundingBox(self.bbox_num, self.input_array_zmax, self.img_view, x,y)
		self.img_view.addItem(added_bbox)
		added_bbox.sigRegionChanged.connect(added_bbox.get_array_slice)
		added_bbox.sigRemoveRequested.connect(self.remove_item_from_img_plot)

	def refresh_top_and_side_views(self):
		'''
		update top and side views with respective views of selected data.
		'''
		# get the bbox's bounds
		self.latest_clicked_bbox.get_array_slice()
		row_start = self.latest_clicked_bbox.row_start 
		row_end = self.latest_clicked_bbox.row_end 
		col_start = self.latest_clicked_bbox.col_start 
		col_end = self.latest_clicked_bbox.col_end

		# set the images in each of the views (top_img_view, top_scan_img_view, side_view_1, side_view_2)
		self.top_img_view.setImage(self.input_array_zmax[row_start:row_end,col_start:col_end,:])
		self.img_chunk = self.input_array[:,row_start:row_end,col_start:col_end,:]
		self.top_scan_img_view.setImage(self.img_chunk)
		self.side_view_1 = np.max(self.img_chunk, axis=1)
		self.side_view_2 = np.max(self.img_chunk, axis=2)
		self.side_view_mode = 1
		self.side_img_view.setImage(self.side_view_1)

		self.show_v_bounds()

	def show_v_bounds(self):
		# show v_bounds if any 
		for v_bound in self.latest_clicked_bbox.get_associated_v_bounds():
			self.side_img_view.addItem(v_bound)

	def clear_top_and_side_views(self):
		'''
		called when mouse has clicked away from the current bbox to draw a new one in the main plot.
		clears the views and other related variables.
		'''
		self.top_img_view.clear()
		self.top_scan_img_view.clear()
		self.side_img_view.clear()
		self.side_view_mode = 0
		self.side_view_1 = None 
		self.side_view_2 = None 
		self.img_chunk = None

		if self.latest_clicked_bbox:
			self.clear_v_bounds()

	def clear_v_bounds(self):
		# clear v_bounds if any 
		for v_bound in self.latest_clicked_bbox.get_associated_v_bounds():
			self.side_img_view.removeItem(v_bound)

	def side_view_plot_mouse_clicked(self, event):
		'''
		called when mouse clicks on side_img_view
		'''
		self.side_img_view_item = self.side_img_view.getImageItem()
		mouse_pos = event.scenePos()
		img_pos = self.side_img_view_item.mapFromScene(mouse_pos)
		y = img_pos.y()
		self.add_v_bound(y)
		

	def add_v_bound(self, y):
		'''
		adds vertical bounding lines to side_img_view
		'''
		self.status_bar.showMessage('')
		num_v_bounds = self.latest_clicked_bbox.get_num_associated_v_bounds()
		if num_v_bounds < 2:
			self.latest_clicked_bbox.increment_num_associated_v_bounds()
			# add a vertical bound
			self.status_bar.showMessage('adding vertical bounds')
			v_bound = pg.InfiniteLine(pos=y, angle=0, movable=True)
			self.latest_clicked_bbox.add_associated_v_bound(v_bound) 
			self.side_img_view.addItem(v_bound)
		# else, do nothing

	def remove_item_from_img_plot(self):
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
		


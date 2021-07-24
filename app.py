from PyQt5.QtWidgets import *
import numpy as np
import pyqtgraph as pg
from boundingbox import BoundingBox
from database import Database
import sqlite3
from messages import *
from exportfiledialog import ExportFileDialog

"""
Main Application Window:
- main image view: displays plot of max z-projection of input 4d tensor image (.npy)
- top view: displays selected portion of image
- top scan view: same as top view but has a slider that allows you to scan through all layers of selected portion
- side view: displays vertical side view (z-axis) of selected portion of image
	- change side view button: allows you to view the different side views of the image slice

Usage:
- to add bbox, click on the main image view. adjust bbox dimensions by dragging its handles.
- to add vertical bounds, click on a bbox, then click on the side view. a horizontal line will be added where you click.

Everything change is saved to the specified sink database.
DOES NOT SUPPORT CONCURRENT RUNS (i.e. different annotation sessions). YOU CAN ONLY ANNOTATE 1 IMAGE AT A TIME.
"""


class Application(QMainWindow):
	def __init__(self, filestate, parent=None, existing_case=False):
		super().__init__(parent)
		self.parent = parent
		self.filestate = filestate

		# connect to source db if existing case
		self.existing_case = existing_case
		if self.existing_case:
		    self.est_source_db_connection()

		# determine current bbox_num
		self.bbox_num = 0
		if self.existing_case:
		    self.bbox_num = self.read_next_bbox_num_from_source_db()

		# latest clicked bbox and prev clicked bbox
		self.latest_clicked_bbox = None
		self.prev_clicked_bbox = None

		# side view orientation mode
		self.side_view_mode = 0  # 1 or 2 depending on orientation, 0 if selector not clicked

		# main layout
		self.layout = QGridLayout()

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
		self.export_btn = QPushButton('Export')

		# IMAGE ARRAY
		self.input_array = np.load(self.filestate.get_source_img_filename())
		self.input_array_depth, self.input_array_height, self.input_array_width, self.input_array_num_ch = self.input_array.shape
		self.input_array = self.input_array / np.max(self.input_array)
		self.input_array_zmax = np.max(self.input_array, axis=0)

		# components cont'd (image plot widget)
		self.img_plot = pg.PlotItem()
		self.top_view_plot = pg.PlotItem()
		self.top_scan_view_plot = pg.PlotItem()
		self.side_view_plot = pg.PlotItem()

		# initialize bbox_id: bbox object dictionary
		self.bbox_by_id_dict = {}

		# initialize UI
		self.init_UI()

		# initialize database. source db is read in init_UI().
		try:
			self.sink_db = Database(self.filestate.get_sink_db_filename())
			if not self.existing_case:
				# clear contents of any preexisting annotations table
				self.sink_db = Database(self.filestate.get_sink_db_filename(), True)
			self.status_bar.showMessage("sink db connection successfully established.")
		except sqlite3.Error as error:
			self.handle_sink_db_sqlite_error(error)

	def init_UI(self):
		"""
		Initialize text/buttons for the main window.
		"""
		# set up global config options for pyqtgraph
		pg.setConfigOptions(imageAxisOrder='row-major')

		# set up image views
		self.img_plot.setTitle("Main Image View")
		self.img_view = pg.ImageView(name="Main Image View",
									 view=self.img_plot)  # create image view widget with view as the image plot widget
		self.img_view.setImage(self.input_array_zmax)  # set its image

		self.top_view_plot.setTitle("Top Image View")
		self.top_img_view = pg.ImageView(name="Top Image View", view=self.top_view_plot)

		self.top_scan_view_plot.setTitle("Top Scan Image View")
		self.top_scan_img_view = pg.ImageView(name="Top Scan Image View", view=self.top_scan_view_plot)

		self.side_view_plot.setTitle("Side Image View")
		self.side_img_view = pg.ImageView(name="Side Image View", view=self.side_view_plot)

		# add image views to layout
		self.layout.addWidget(self.export_btn, 0, 3)
		self.layout.addWidget(self.img_view, 1, 0, 2, 2)
		self.layout.addWidget(self.top_img_view, 1, 2, 1, 1)
		self.layout.addWidget(self.top_scan_img_view, 2, 2, 1, 1)
		self.layout.addWidget(self.side_img_view, 1, 3, 2, 1)
		self.layout.addWidget(self.change_side_view_btn, 3, 3)

		self.central_widget.setLayout(self.layout)

		# set up window properties
		self.setWindowTitle(self.title)
		self.setGeometry(self.x, self.y, self.width, self.height)
		self.setCentralWidget(self.central_widget)

		# image items
		self.img_view_item = self.img_view.getImageItem()

		# set up mouse events for various image views
		self.img_view.scene.sigMouseClicked.connect(self.main_view_mouse_clicked)
		self.side_img_view.scene.sigMouseClicked.connect(self.side_view_mouse_clicked)

		# set up button events
		self.change_side_view_btn.clicked.connect(self.change_side_view_btn_clicked)
		self.export_btn.clicked.connect(self.on_export_btn_clicked)

		# load in bboxes and vbounds if existing case
		if self.existing_case:
			self.load_annotations_from_source_db()

	#####################
	# BBOX DICT METHODS #   (not used)
	#####################

	def add_or_update_bbox_dict(self, bbox):
		"""
		add to or update the bbox_by_id_dict
		"""
		self.bbox_by_id_dict[bbox.get_bbox_num()] = bbox

	def delete_from_bbox_dict(self, bbox):
		"""
		delete from the bbox_by_id_dict
		"""
		removed_bbox = self.bbox_by_id_dict.pop(bbox.get_bbox_num())
		return removed_bbox

	def get_bbox_from_id(self, bbox_id):
		"""
		get bbox from bbox_id
		"""
		try:
			return self.bbox_by_id_dict[bbox_id]
		except KeyError as error:
			print("bbox with id " + str(bbox_id) + " does not exist: ", error)

	#####################
	# SOURCE DB METHODS #
	#####################

	def est_source_db_connection(self):
		"""
		establish connection to source database if this is an existing case.
		"""
		source_db_filename = self.filestate.get_source_db_filename()
		try:
			self.source_db_conn = sqlite3.connect(source_db_filename)
			self.source_db_cur = self.source_db_conn.cursor()
		except sqlite3.Error as error:
			self.handle_source_db_sqlite_error(error)

	def handle_source_db_sqlite_error(self, error=None):
		"""
		handler for source db sqlite errors
		"""
		# self.status_bar.showMessage("Source database error: " + error)
		if error: print("Source database error: ", error)
		self.source_db_cur.close()
		self.source_db_conn.close()
		self.close()

	def read_next_bbox_num_from_source_db(self):
		"""
		get the latest bbox number from source db
		"""
		try:
			res = self.source_db_cur.execute("SELECT MAX(bbox_id) FROM annotations")
			return res.fetchone()[0]
		except sqlite3.Error as error:
			self.handle_source_db_sqlite_error(error)

	def load_annotations_from_source_db(self):
		"""
		read and draw bboxes from source db
		"""
		self.status_bar.showMessage("loading annotations from source db")
		try:
			res = self.source_db_cur.execute("SELECT * from annotations")
			rows = res.fetchall()
			for row in rows:
				# BoundingBox(self.bbox_num, self.input_array_zmax, self.img_view, x,y)
				bbox_id, row_start, row_end, col_start, col_end, z_start, z_end = row
				bbox = BoundingBox(bbox_id, self.input_array_zmax, self.img_view, col_start, row_start)
				bbox.setPen(width=1, color='y')
				bbox_row_size = row_end - row_start
				bbox_col_size = col_end - col_start
				bbox.setSize([bbox_col_size, bbox_row_size])
				z_start_bound = self.get_vboundline_from_yvalue(z_start)
				z_end_bound = self.get_vboundline_from_yvalue(z_end)
				bbox.add_associated_v_bound(z_start_bound)
				bbox.add_associated_v_bound(z_end_bound)
				self.add_bbox_to_main_view(bbox)
			self.status_bar.showMessage("annotations successfully loaded from source db")
			self.source_db_cur.close()
			self.source_db_conn.close()
		except sqlite3.Error as error:
			self.handle_source_db_sqlite_error(error)

	def get_vboundline_from_yvalue(self, y):
		"""
		return InfiniteLine corresponding to input y value
		"""
		v_bound = None
		if y != 'NULL':
			v_bound = pg.InfiniteLine(pos=y, angle=0, movable=True)
		return v_bound

	###################
	# SINK DB METHODS #
	###################

	def handle_sink_db_sqlite_error(self, error=None):
		"""
		handler for sink db sqlite errors
		"""
		# self.status_bar.showMessage("Sink database error: " + error)
		if error: print("Sink database error: ", error)
		self.close()

	def add_or_update_sink_database(self):
		"""
		add or update sink db with current information on the latest interacted-with annotation.
		called when bbox is added(drawn), dragged, changed in size and when vbounds are added, dragged.
		"""

		self.latest_clicked_bbox.update_bbox_vertices()
		try:
			annotation = self.latest_clicked_bbox.get_parameters()
			self.sink_db.add_or_update_annotation(annotation)
		except sqlite3.Error as error:
			self.handle_sink_db_sqlite_error(error)

	def delete_from_sink_database(self, bbox):
		"""
		deletes bbox from sink db.
		called when bbox is deleted.
		"""
		annotation = bbox.get_parameters()
		bbox_id = annotation[0]
		try:
			self.sink_db.delete_annotation(bbox_id)
		except sqlite3.Error as error:
			self.handle_sink_db_sqlite_error(error)

	#############
	# MAIN VIEW #
	#############

	def main_view_mouse_clicked(self, event):
		"""
		For adding bboxes or changing existing bboxes in the main image view.
		"""
		self.status_bar.showMessage("")
		mouse_pos = event.scenePos()
		img_pos = self.img_view_item.mapFromScene(mouse_pos)
		x = img_pos.x()
		y = img_pos.y()
		items = self.img_view.scene.items(mouse_pos)
		# print(items)
		bboxes_at_cursor = [item for item in items if isinstance(item, BoundingBox)]
		self.clear_top_and_side_views()
		if bboxes_at_cursor:  # SHOW THE DIFFERENT VIEWS FOR THE SELECTED DATA
			self.update_latest_clicked_bbox(bboxes_at_cursor[0])  # take top-most bbox
			self.status_bar.showMessage('bbox ' + str(self.latest_clicked_bbox.get_bbox_num()) + ' clicked')
			self.refresh_top_and_side_views()
		else:  # DRAW THE BBOX
			self.status_bar.showMessage('drawing new bbox')
			self.draw_new_bbox(x, y)

	def draw_new_bbox(self, x, y):
		"""
		construct and add a new bbox at specified x, y coordinates in main image view.
		"""
		self.bbox_num += 1
		self.update_latest_clicked_bbox(BoundingBox(self.bbox_num, self.input_array_zmax, self.img_view, x, y))
		self.add_or_update_sink_database()
		self.add_bbox_to_main_view(self.latest_clicked_bbox)

	def add_bbox_to_main_view(self, bbox):
		"""
		adds bbox to main image view and sets up its signals.
		"""
		self.img_view.addItem(bbox)
		bbox.sigRegionChangeFinished.connect(self.on_bbox_region_change_finished)
		bbox.sigRemoveRequested.connect(self.remove_item_from_main_img_plot)

	def on_bbox_region_change_finished(self):
		"""
		called when a bbox's region is changed.
		fixes bug where changing a bbox's region doesn't update self.latest_clicked_box
		"""
		self.update_latest_clicked_bbox(self.sender())
		self.status_bar.showMessage("Changing bounds of bbox " + str(self.latest_clicked_bbox.get_bbox_num()))
		self.add_or_update_sink_database()

	def remove_item_from_main_img_plot(self):
		"""
		When the appropriate right click context menu item is selected, removes the
		item from the main image plot.
		"""
		self.status_bar.showMessage("removed bbox")
		bbox = self.sender()  # bbox
		self.update_latest_clicked_bbox(bbox)  # update latest clicked bbox even though it's removed
		self.img_plot.removeItem(bbox)
		self.clear_top_and_side_views()
		self.delete_from_sink_database(bbox)

	def update_latest_clicked_bbox(self, bbox):
		"""
		Sets the prev clicked bbox to the prev bbox that was interacted with.
		Changes its style to be 'unselected'.
		Sets the latest clicked bbox to the currently selected/modified bbox.
		Sets its style to be 'selected'.
		"""
		if self.latest_clicked_bbox:  # can be deleted
			self.latest_clicked_bbox.setPen(width=1, color='y')
		self.prev_clicked_bbox = self.latest_clicked_bbox
		self.latest_clicked_bbox = bbox
		self.latest_clicked_bbox.setPen(width=3, color='g')


	######################
	# TOP AND SIDE VIEWS #
	######################

	def refresh_top_and_side_views(self):
		"""
		update top and side views with respective views of selected data.
		"""
		# get the bbox's bounds
		self.latest_clicked_bbox.update_bbox_vertices()
		bbox_id, row_start, row_end, col_start, col_end, z_start, z_end = self.latest_clicked_bbox.get_parameters()

		# set the images in each of the views (top_img_view, top_scan_img_view, side_view_1, side_view_2)
		self.top_img_view.setImage(self.input_array_zmax[row_start:row_end, col_start:col_end, :])
		self.img_chunk = self.input_array[:, row_start:row_end, col_start:col_end, :]
		self.top_scan_img_view.setImage(self.img_chunk)
		self.side_view_1 = np.max(self.img_chunk, axis=1)
		self.side_view_2 = np.max(self.img_chunk, axis=2)
		self.side_view_mode = 1
		self.side_img_view.setImage(self.side_view_1)

		self.show_v_bounds()

	def show_v_bounds(self):
		"""
		show v_bounds if any
		"""
		for v_bound in self.latest_clicked_bbox.get_associated_v_bounds():
			self.side_img_view.addItem(v_bound)

	def clear_top_and_side_views(self):
		"""
		called when mouse has clicked away from the current bbox to draw a new one in the main plot.
		clears the views and other related variables.
		"""
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
		"""
		clear v_bounds if any
		"""
		for v_bound in self.latest_clicked_bbox.get_associated_v_bounds():
			self.side_img_view.removeItem(v_bound)

	#############
	# SIDE VIEW #
	#############

	def side_view_mouse_clicked(self, event):
		"""
		called when mouse clicks on side_img_view
		"""
		self.side_img_view_item = self.side_img_view.getImageItem()
		mouse_pos = event.scenePos()
		img_pos = self.side_img_view_item.mapFromScene(mouse_pos)
		y = round(img_pos.y())
		self.draw_new_v_bound(y)

	def draw_new_v_bound(self, y):
		"""
		adds vertical (z-axis) bounding lines to side_img_view
		y (position) is rounded.
		"""
		self.status_bar.showMessage('')
		num_v_bounds = self.latest_clicked_bbox.get_num_associated_v_bounds()
		if num_v_bounds < 2:
			# add a vertical bound
			self.status_bar.showMessage('adding vbounds for bbox ' + str(self.latest_clicked_bbox.get_bbox_num()))
			v_bound = pg.InfiniteLine(pos=y, angle=0, movable=True)
			self.latest_clicked_bbox.add_associated_v_bound(v_bound)
			self.add_or_update_sink_database()
			self.add_v_bound_to_side_view(v_bound)
		# else, do nothing

	def add_v_bound_to_side_view(self, v_bound):
		"""
		Adds vbound to side view and sets up its signals.
		"""
		self.side_img_view.addItem(v_bound)
		v_bound.sigPositionChangeFinished.connect(self.on_vbound_position_changed_finished)

	def on_vbound_position_changed_finished(self):
		"""
		when vbound position is changed via dragging.
		fixes bug where an adjusted vbound doesn't have its value rounded.
		"""
		# set the bound's value to the rounded number
		v_bound= self.sender()
		v_bound_value = v_bound.value()
		v_bound.setValue(round(v_bound_value))
		self.status_bar.showMessage("Adjusting vbounds of bbox " + str(self.latest_clicked_bbox.get_bbox_num()))
		self.add_or_update_sink_database()

	def change_side_view_btn_clicked(self):
		"""
		Button to change side view of selected area.
		Does nothing if a selected area is not clicked on.
		"""
		if self.side_view_mode == 1:
			self.side_view_mode = 2
			self.side_img_view.setImage(self.side_view_2)
		elif self.side_view_mode == 2:
			self.side_view_mode = 1
			self.side_img_view.setImage(self.side_view_1)

	def on_export_btn_clicked(self):
		"""
		button to export annotations as .csv.
		"""
		export_file_dlg = ExportFileDialog(self.sink_db, self)
		export_file_dlg.show()

	#########
	# CLOSE #
	#########

	def closeEvent(self, event):
		"""
		upon closing window
		"""
		reply = QMessageBox.question(self, 'Window Close',
									 'Are you sure you want to close the window? (Current work will be saved.)',
									 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
			self.sink_db.save_and_close()
			# print('Window closed')
		else:
			event.ignore()

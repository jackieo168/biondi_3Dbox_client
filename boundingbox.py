import pyqtgraph as pg

class BoundingBox(pg.RectROI):
	def __init__(self, bbox_num, img, img_view, x, y):
		self.bbox_num = bbox_num
		self.img = img
		self.img_view = img_view
		self.img_view_item = self.img_view.getImageItem()
		self.init_x = x 
		self.init_y = y 
		self.num_associated_v_bounds = 0
		super().__init__([self.init_x, self.init_y], size=[20,20], rotatable=False, resizable=True, removable=True)
		# self.bbox = pg.RectROI([self.y, self.x], size=[10,10])

		# ## handles scaling horizontally around center
		self.addScaleHandle([1, 0.5], [0, 0.5]) #append the box with dragable handles
		self.addScaleHandle([0, 0.5], [1, 0.5]) #for nice resizing purposes

		## handles scaling vertically from opposite edge
		self.addScaleHandle([0.5, 0], [0.5, 1])
		self.addScaleHandle([0.5, 1], [0.5, 0])

		## handles scaling both vertically and horizontally
		self.addScaleHandle([0, 0], [1, 1])
		self.addScaleHandle([0, 1], [1, 0])
		self.addScaleHandle([1, 0], [0, 1])
		self.addScaleHandle([1, 1], [0, 0])

	def get_array_slice(self):
		self.selected_data_zproj = self.getArrayRegion(self.img, self.img_view_item, returnMappedCoords=True)
		self.selected_data_zproj_slice = self.getArraySlice(self.img, self.img_view_item, returnSlice=True)
		selected_data_zproj_slice_obj = self.selected_data_zproj_slice[0]
		selected_data_zproj_slice_obj_0 = selected_data_zproj_slice_obj[0]
		selected_data_zproj_slice_obj_1 = selected_data_zproj_slice_obj[1]
		self.row_start = selected_data_zproj_slice_obj_0.start
		self.row_end = selected_data_zproj_slice_obj_0.stop
		self.col_start = selected_data_zproj_slice_obj_1.start
		self.col_end = selected_data_zproj_slice_obj_1.stop

	def get_bbox_num(self):
		return self.bbox_num

	def get_num_associated_v_bounds(self):
		return self.num_associated_v_bounds

	def increment_num_associated_v_bounds(self):
		self.num_associated_v_bounds += 1

	def decrement_num_associated_v_bounds(self):
		self.num_associated_v_bounds -= 1
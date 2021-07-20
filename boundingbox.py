import pyqtgraph as pg

class BoundingBox(pg.RectROI):
	def __init__(self, bbox_num, img, img_view, x, y):
		self.bbox_num = bbox_num
		self.img = img # numpy array
		self.img_view = img_view
		self.img_view_item = self.img_view.getImageItem()
		init_x = x 
		init_y = y 
		self.num_associated_v_bounds = 0
		self.associated_v_bounds = []
		super().__init__([init_x, init_y], size=[20,20], rotatable=False, resizable=True, removable=True)

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
		# self.selected_data_zproj = self.getArrayRegion(self.img, self.img_view_item, returnMappedCoords=True)
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

	def add_associated_v_bound(self, v_bound):
		if v_bound:
			self.associated_v_bounds.append(v_bound)
			self.increment_num_associated_v_bounds()

	def get_associated_v_bounds(self):
		return self.associated_v_bounds

	def get_parameters(self):
		'''
		bbox_id, row_start, row_end, col_start, col_end, z_start, z_end of annotation
		'''
		z_start, z_end = 'NULL', 'NULL'
		if self.num_associated_v_bounds > 0:
			z_start = self.associated_v_bounds[0].value()
		if self.num_associated_v_bounds == 2:
			z_end = self.associated_v_bounds[1].value()
		return (self.bbox_num, self.row_start, self.row_end, self.col_start, self.col_end, z_start, z_end)
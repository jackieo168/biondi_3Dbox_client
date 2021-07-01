import pyqtgraph as pg

class BoundingBox():
	def __init__(self,  bbox_num,img, img_plot, x, y):
		self.bbox_num = bbox_num
		self.img = img
		self.img_plot = img_plot
		self.img_plot_item = self.img_plot.getImageItem()
		self.x = x 
		self.y = y 
		self.bbox = pg.RectROI([self.y, self.x], size=[10,10])

		# ## handles scaling horizontally around center
		self.bbox.addScaleHandle([1, 0.5], [0, 0.5]) #append the box with dragable handles
		self.bbox.addScaleHandle([0, 0.5], [1, 0.5]) #for nice resizing purposes

		## handles scaling vertically from opposite edge
		self.bbox.addScaleHandle([0.5, 0], [0.5, 1])
		self.bbox.addScaleHandle([0.5, 1], [0.5, 0])

		## handles scaling both vertically and horizontally
		self.bbox.addScaleHandle([0, 0], [1, 1])
		self.bbox.addScaleHandle([0, 1], [1, 0])
		self.bbox.addScaleHandle([1, 0], [0, 1])
		self.bbox.addScaleHandle([1, 1], [0, 0])

	def getArraySlice(self):
		print(self.bbox.getArraySlice(self.img, self.img_plot_item, returnSlice=True))
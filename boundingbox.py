import pyqtgraph as pg

class BoundingBox():
	def __init__(self, x, y):
		self.x = x 
		self.y = y 
		self.bbox = pg.ROI([self.x, self.y])

		## handles scaling horizontally around center
		self.bbox.addScaleHandle([1, 0.5], [0.5, 0.5]) #append the box with dragable handles
		self.bbox.addScaleHandle([0, 0.5], [0.5, 0.5]) #for nice resizing purposes

		## handles scaling vertically from opposite edge
		self.bbox.addScaleHandle([0.5, 0], [0.5, 1])
		self.bbox.addScaleHandle([0.5, 1], [0.5, 0])

		## handles scaling both vertically and horizontally
		self.bbox.addScaleHandle([1, 1], [0, 0])
		self.bbox.addScaleHandle([0, 0], [1, 1])
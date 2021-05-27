import napari
from skimage.data import cells3d
cells = cells3d()[30, 1]  # get some data
viewer = napari.view_image(cells, colormap='magma')
napari.run()
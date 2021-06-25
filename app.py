import tkinter as tk 
from tkinter import ttk
from PIL import Image, ImageTk
import os
import numpy as np
import napari

class Application(tk.Frame):
	def __init__(self, filestate, master):
		# launch napari w/ instructions screen
		self.master = master
		self.filestate = filestate

		input_array = np.load(self.filestate.get_file_name())
		input_array = input_array/np.max(input_array)
		input_array_zmax = np.max(input_array, axis=0)
		viewer = napari.Viewer(ndisplay=2)
		new_image_layer = viewer.add_image(input_array_zmax)
		new_shapes_layer = viewer.add_shapes(
			[[0,0],[0,0],[0,0],[0,0]],
			shape_type = 'rectangle',
			face_color = 'transparent',
			edge_width = 8,
			edge_color = 'lime',
			name = 'bboxes')
		# new_image_layer = viewer.add_image(input_array[:,100:200,100:200,:], rgb=True, blending='additive')
		main_window = viewer.window._qt_window
		qt_viewer = viewer.window.qt_viewer
		main_window.setGeometry(300,300,300,300)
		main_window.show()
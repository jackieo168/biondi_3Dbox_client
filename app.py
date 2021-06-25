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
		# self.master = master
		# # tk.Frame.__init__(self, master)
		# frame = tk.Frame(self.master)
		# frame.pack()

		# bottomframe = tk.Frame(self.master)
		# bottomframe.pack( side = 'bottom' )

		# redbutton = tk.Button(frame, text="Red", fg="red")
		# redbutton.pack( side = 'left')

		# greenbutton = tk.Button(frame, text="Brown", fg="brown")
		# greenbutton.pack( side = 'left' )

		# bluebutton = tk.Button(frame, text="Blue", fg="blue")
		# bluebutton.pack( side = 'left' )

		# blackbutton = tk.Button(bottomframe, text="Black", fg="black")
		# blackbutton.pack( side = 'bottom')
		# self.WIDTH, self.HEIGHT = 900, 900
		# self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
		# self.rect_id = None
		# self.path = "dog.jpg"

		# self.master = master
		# window = self.master
		# window.title("Select Area")
		# window.geometry('%sx%s' % (self.WIDTH, self.HEIGHT))
		# window.configure(background='grey')

		# img = ImageTk.PhotoImage(Image.open(self.path))
		# self.canvas = tk.Canvas(window, width=img.width(), height=img.height(),
		#                    borderwidth=0, highlightthickness=0)
		# self.canvas.pack(expand=True)
		# self.canvas.img = img  # Keep reference in case this code is put into a function.
		# self.canvas.create_image(0, 0, image=img, anchor=tk.NW)

		# # Create selection rectangle (invisible since corner points are equal).
		# self.rect_id = self.canvas.create_rectangle(self.topx, self.topy, self.topx, self.topy,
		#                                   dash=(2,2), fill='', outline='white')

		# self.canvas.bind('<Button-1>', self.get_mouse_posn)
		# self.canvas.bind('<B1-Motion>', self.update_sel_rect)
		# tk.Button(window, text="Quit", command=window.destroy).pack()

		# window.mainloop()
		# self.master.geometry("580x100")
		# self.master.title("Tile Sampling Tool")

		# w1 = f"Welcome to the Tile Sampling  Tool!\nIf you are returning to a previous session, please click on the \"Open Previous Folder\" button.\nIf you are starting a new session, please create an empty folder and select it using the \"Initiate Folder\" button."

		# self.welcome_label1 = tk.Label(self.master, text = w1)
		# self.welcome_label1.grid(row = 0, column = 2, sticky = 'nswe')

		# self.button_frame = tk.Frame(self.master)
		# self.button_frame.grid(row = 4, column = 2, sticky = 'ns')

		# self.find_image_button = tk.Button(self.button_frame, text="Open Previous Folder")
		# self.find_image_button.pack(side = "left", padx = 2 , pady = 2)

		# self.initiate_folder_button = tk.Button(self.button_frame, text = "Initiate Folder")
		# self.initiate_folder_button.pack(side = "left", padx = 2 , pady = 2)

		# self.case_type = tk.StringVar()
		# self.case_type.set("biondi")
		# self.master.mainloop()

	# def get_mouse_posn(self, event):
	# 	self.topx, self.topy = event.x, event.y

	# def update_sel_rect(self, event):
	# 	self.botx, self.boty = event.x, event.y
	# 	self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)  # Update selection rect.

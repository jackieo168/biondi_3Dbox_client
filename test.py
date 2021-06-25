# from __future__ import print_function
# """
# Do a mouseclick somewhere, move the mouse to some destination, release
# the button.  This class gives click- and release-events and also draws
# a line or a box from the click-point to the actual mouseposition
# (within the same axes) until the button is released.  Within the
# method 'self.ignore()' it is checked whether the button from eventpress
# and eventrelease are the same.

# """
# from matplotlib.widgets import RectangleSelector
import numpy as np
# import matplotlib.pyplot as plt


# def on_select(eclick, erelease):
#     'eclick and erelease are the press and release events'
#     x1, y1 = eclick.xdata, eclick.ydata
#     x2, y2 = erelease.xdata, erelease.ydata
#     print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
#     print(" The button you used were: %s %s" % (eclick.button, erelease.button))

# def on_select1(eclick, erelease):
#     'eclick and erelease are the press and release events'
#     x1, y1 = eclick.xdata, eclick.ydata
#     x2, y2 = erelease.xdata, erelease.ydata
#     print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
#     print(" The button you used were: %s %s" % (eclick.button, erelease.button))


# def toggle_selector(event):
#     print(' Key pressed.')
#     if event.key in ['Q', 'q'] and toggle_selector.RS.active:
#         print(' RectangleSelector deactivated.')
#         toggle_selector.RS.set_active(False)
#     if event.key in ['A', 'a'] and not toggle_selector.RS.active:
#         print(' RectangleSelector activated.')
#         toggle_selector.RS.set_active(True)


# fig, ax = plt.subplots()                 # make a new plotting range
# fig.set_size_inches(12,12)
# rectprops = dict(edgecolor="lime",fill=False, linewidth=3)
arr = np.load('data/A18-1 HuChP ThS + Hoechst 2 spacer 40x.npy')
arr = arr/np.max(arr)
z_arr = np.max(arr, axis=0)
# # print(z_arr[:10,:10,:])
# plt.imshow(z_arr)

# print("\n      click  -->  release")

# # drawtype is 'box' or 'line' or 'none'
# toggle_selector.RS = RectangleSelector(ax, on_select,
#                                        drawtype='box', useblit=True,
#                                        button=[1, 3],  # don't use middle button
#                                        minspanx=5, minspany=5,
#                                        rectprops = rectprops,
#                                        spancoords='pixels',
#                                        interactive=True)
# RectangleSelector(ax, on_select1,
#                    drawtype='box', useblit=True,
#                    button=[1, 3],  # don't use middle button
#                    minspanx=5, minspany=5,
#                    rectprops = rectprops,
#                    spancoords='pixels',
#                    interactive=True)
# plt.connect('key_press_event', toggle_selector)
# plt.show()

import pyqtgraph as pg
import pyqtgraph.examples as pge
# from PIL import Image

# img = Image.fromarray(z_arr)
pg.image(z_arr)

if __name__ == '__main__':
    pg.mkQApp().exec_()

# # # from __future__ import print_function
# # # """
# # # Do a mouseclick somewhere, move the mouse to some destination, release
# # # the button.  This class gives click- and release-events and also draws
# # # a line or a box from the click-point to the actual mouseposition
# # # (within the same axes) until the button is released.  Within the
# # # method 'self.ignore()' it is checked whether the button from eventpress
# # # and eventrelease are the same.

# # # """
# # # from matplotlib.widgets import RectangleSelector
# # import numpy as np
# # # import matplotlib.pyplot as plt


# # # def on_select(eclick, erelease):
# # #     'eclick and erelease are the press and release events'
# # #     x1, y1 = eclick.xdata, eclick.ydata
# # #     x2, y2 = erelease.xdata, erelease.ydata
# # #     print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
# # #     print(" The button you used were: %s %s" % (eclick.button, erelease.button))

# # # def on_select1(eclick, erelease):
# # #     'eclick and erelease are the press and release events'
# # #     x1, y1 = eclick.xdata, eclick.ydata
# # #     x2, y2 = erelease.xdata, erelease.ydata
# # #     print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
# # #     print(" The button you used were: %s %s" % (eclick.button, erelease.button))


# # # def toggle_selector(event):
# # #     print(' Key pressed.')
# # #     if event.key in ['Q', 'q'] and toggle_selector.RS.active:
# # #         print(' RectangleSelector deactivated.')
# # #         toggle_selector.RS.set_active(False)
# # #     if event.key in ['A', 'a'] and not toggle_selector.RS.active:
# # #         print(' RectangleSelector activated.')
# # #         toggle_selector.RS.set_active(True)


# # # fig, ax = plt.subplots()                 # make a new plotting range
# # # fig.set_size_inches(12,12)
# # # rectprops = dict(edgecolor="lime",fill=False, linewidth=3)
# # arr = np.load('data/A18-1 HuChP ThS + Hoechst 2 spacer 40x.npy')
# # arr = arr/np.max(arr)
# # z_arr = np.max(arr, axis=0)
# # # # print(z_arr[:10,:10,:])
# # # plt.imshow(z_arr)

# # # print("\n      click  -->  release")

# # # # drawtype is 'box' or 'line' or 'none'
# # # toggle_selector.RS = RectangleSelector(ax, on_select,
# # #                                        drawtype='box', useblit=True,
# # #                                        button=[1, 3],  # don't use middle button
# # #                                        minspanx=5, minspany=5,
# # #                                        rectprops = rectprops,
# # #                                        spancoords='pixels',
# # #                                        interactive=True)
# # # RectangleSelector(ax, on_select1,
# # #                    drawtype='box', useblit=True,
# # #                    button=[1, 3],  # don't use middle button
# # #                    minspanx=5, minspany=5,
# # #                    rectprops = rectprops,
# # #                    spancoords='pixels',
# # #                    interactive=True)
# # # plt.connect('key_press_event', toggle_selector)
# # # plt.show()

# # import pyqtgraph as pg
# # import pyqtgraph.examples as pge
# # # from PIL import Image

# # # img = Image.fromarray(z_arr)
# # # i = pg.image(z_arr)
# # i = pg.ImageView()
# # i.setImage(z_arr)
# # i.show()
# # r1 = pg.ROI([0,0],[10,10])
# # i.addItem(r1)

# # ## handles scaling horizontally around center
# # r1.addScaleHandle([1, 0.5], [0.5, 0.5]) #append the box with dragable handles
# # r1.addScaleHandle([0, 0.5], [0.5, 0.5]) #for nice resizing purposes

# # ## handles scaling vertically from opposite edge
# # r1.addScaleHandle([0.5, 0], [0.5, 1])
# # r1.addScaleHandle([0.5, 1], [0.5, 0])

# # ## handles scaling both vertically and horizontally
# # r1.addScaleHandle([1, 1], [0, 0])
# # r1.addScaleHandle([0, 0], [1, 1])

# # r2 = pg.ROI([0,0],[20,20])
# # i.addItem(r2)

# # ## handles scaling horizontally around center
# # r2.addScaleHandle([1, 0.5], [0.5, 0.5]) #append the box with dragable handles
# # r2.addScaleHandle([0, 0.5], [0.5, 0.5]) #for nice resizing purposes

# # ## handles scaling vertically from opposite edge
# # r2.addScaleHandle([0.5, 0], [0.5, 1])
# # r2.addScaleHandle([0.5, 1], [0.5, 0])

# # ## handles scaling both vertically and horizontally
# # r2.addScaleHandle([1, 1], [0, 0])
# # r2.addScaleHandle([0, 0], [1, 1])

# # if __name__ == '__main__':
# #     pg.mkQApp().exec_()
# # import sys
# # from PyQt5 import QtWidgets, QtCore, QtGui

# # class MyWidget(QtWidgets.QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setGeometry(30,30,600,400)
# #         self.begin = QtCore.QPoint()
# #         self.end = QtCore.QPoint()
# #         self.show()

# #     def paintEvent(self, event):
# #         qp = QtGui.QPainter(self)
# #         br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))  
# #         qp.setBrush(br)   
# #         qp.drawRect(QtCore.QRect(self.begin, self.end))       

# #     def mousePressEvent(self, event):
# #         self.begin = event.pos()
# #         self.end = event.pos()
# #         self.update()

# #     def mouseMoveEvent(self, event):
# #         self.end = event.pos()
# #         self.update()

# #     def mouseReleaseEvent(self, event):
# #         self.begin = event.pos()
# #         self.end = event.pos()


# # if __name__ == '__main__':
# #     app = QtWidgets.QApplication(sys.argv)
# #     window = MyWidget()
# #     window.show()
# #     app.aboutToQuit.connect(app.deleteLater)
# #     sys.exit(app.exec_())

# """Rect Tracker class for Python Tkinter Canvas"""

# def groups(glist, numPerGroup=2):
#     result = []

#     i = 0
#     cur = []
#     for item in glist:
#         if not i < numPerGroup:
#             result.append(cur)
#             cur = []
#             i = 0

#         cur.append(item)
#         i += 1

#     if cur:
#         result.append(cur)

#     return result

# def average(points):
#     aver = [0,0]
    
#     for point in points:
#         aver[0] += point[0]
#         aver[1] += point[1]
        
#     return aver[0]/len(points), aver[1]/len(points)

# class RectTracker:
    
#     def __init__(self, canvas):
#         self.canvas = canvas
#         self.item = None
        
#     def draw(self, start, end, **opts):
#         """Draw the rectangle"""
#         return self.canvas.create_rectangle(*(list(start)+list(end)), **opts)
        
#     def autodraw(self, **opts):
#         """Setup automatic drawing; supports command option"""
#         self.start = None
#         self.canvas.bind("<Button-1>", self.__update, '+')
#         self.canvas.bind("<B1-Motion>", self.__update, '+')
#         self.canvas.bind("<ButtonRelease-1>", self.__stop, '+')
        
#         self._command = opts.pop('command', lambda *args: None)
#         self.rectopts = opts
        
#     def __update(self, event):
#         if not self.start:
#             self.start = [event.x, event.y]
#             return
        
#         if self.item is not None:
#             self.canvas.delete(self.item)
#         self.item = self.draw(self.start, (event.x, event.y), **self.rectopts)
#         self._command(self.start, (event.x, event.y))
        
#     def __stop(self, event):
#         self.start = None
#         self.canvas.delete(self.item)
#         self.item = None
        
#     def hit_test(self, start, end, tags=None, ignoretags=None, ignore=[]):
#         """
#         Check to see if there are items between the start and end
#         """
#         ignore = set(ignore)
#         ignore.update([self.item])
        
#         # first filter all of the items in the canvas
#         if isinstance(tags, str):
#             tags = [tags]
        
#         if tags:
#             tocheck = []
#             for tag in tags:
#                 tocheck.extend(self.canvas.find_withtag(tag))
#         else:
#             tocheck = self.canvas.find_all()
#         tocheck = [x for x in tocheck if x != self.item]
#         if ignoretags:
#             if not hasattr(ignoretags, '__iter__'):
#                 ignoretags = [ignoretags]
#             tocheck = [x for x in tocheck if x not in self.canvas.find_withtag(it) for it in ignoretags]
        
#         self.items = tocheck
        
#         # then figure out the box
#         xlow = min(start[0], end[0])
#         xhigh = max(start[0], end[0])
        
#         ylow = min(start[1], end[1])
#         yhigh = max(start[1], end[1])
        
#         items = []
#         for item in tocheck:
#             if item not in ignore:
#                 x, y = average(groups(self.canvas.coords(item)))
#                 if (xlow < x < xhigh) and (ylow < y < yhigh):
#                     items.append(item)
    
#         return items

# def main():
#     from random import shuffle
    
#     canv = Canvas(width=500, height=500)
#     canv.create_rectangle(50, 50, 250, 150, fill='red')
#     canv.pack(fill=BOTH, expand=YES)
    
#     rect = RectTracker(canv)
#     # draw some base rectangles
#     rect.draw([50,50], [250, 150], fill='red', tags=('red', 'box'))
#     rect.draw([300,300], [400, 450], fill='green', tags=('gre', 'box'))
    
#     # just for fun
#     x, y = None, None
#     def cool_design(event):
#         global x, y
#         kill_xy()
        
#         dashes = [3, 2]
#         x = canv.create_line(event.x, 0, event.x, 1000, dash=dashes, tags='no')
#         y = canv.create_line(0, event.y, 1000, event.y, dash=dashes, tags='no')
        
#     def kill_xy(event=None):
#         canv.delete('no')
    
#     canv.bind('<Motion>', cool_design, '+')
    
#     # command
#     def onDrag(start, end):
#         global x,y
#         items = rect.hit_test(start, end)
#         for x in rect.items:
#             if x not in items:
#                 canv.itemconfig(x, fill='grey')
#             else:
#                 canv.itemconfig(x, fill='blue')
    
#     rect.autodraw(fill="", width=2, command=onDrag)
    
#     mainloop()

# if __name__ == '__main__':
#     try:
#         from tkinter import *
#     except ImportError:
#         from Tkinter import *
#     main()
# from PyQt5.QtWidgets import *
# app = QApplication([])
# button = QPushButton('Click')
# def on_button_clicked():
#     alert = QMessageBox()
#     alert.setText('You clicked the button!')
#     alert.exec()

# button.clicked.connect(on_button_clicked)
# button.show()
# app.exec()

# -*- coding: utf-8 -*-
"""
This example demonstrates the creation of a plot with a customized
AxisItem and ViewBox. 
"""
 
 
# import initExample ## Add path to library (just for examples; you do not need this)
 
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time
 
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = max(values)-min(values)
        #if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        if rng < 3600*24:
            string = '%H:%M:%S'
            label1 = '%b %d -'
            label2 = ' %b %d, %Y'
        elif rng >= 3600*24 and rng < 3600*24*30:
            string = '%d'
            label1 = '%b - '
            label2 = '%b, %Y'
        elif rng >= 3600*24*30 and rng < 3600*24*30*24:
            string = '%b'
            label1 = '%Y -'
            label2 = ' %Y'
        elif rng >=3600*24*30*24:
            string = '%Y'
            label1 = ''
            label2 = ''
        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
        try:
            label = time.strftime(label1, time.localtime(min(values)))+time.strftime(label2, time.localtime(max(values)))
        except ValueError:
            label = ''
        #self.setLabel(text=label)
        return strns
 
class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)
         
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
             
    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)
 
 
app = pg.mkQApp()
 
axis = DateAxis(orientation='bottom')
vb = CustomViewBox()
 
pw = pg.PlotWidget(viewBox=vb, axisItems={'bottom': axis}, enableMenu=False, title="PlotItem with custom axis and ViewBox<br>Menu disabled, mouse behavior changed: left-drag to zoom, right-click to reset zoom")
dates = np.arange(8) * (3600*24*356)
pw.plot(x=dates, y=[1,6,2,4,3,5,6,8], symbol='o')
pw.show()
pw.setWindowTitle('pyqtgraph example: customPlot')
 
r = pg.PolyLineROI([(0,0), (10, 10)])
pw.addItem(r)
app.exec()
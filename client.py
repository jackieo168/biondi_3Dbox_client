# import napari
# from skimage.data import cells3d
# cells = cells3d()[30, 1]  # get some data
# viewer = napari.view_image(cells, colormap='magma')
# napari.run()
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Test Window"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.init()

    def init(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

app = QApplication([])
window = Window()
window.show()
print("WINDOW IS SHOWN.")
app.exec_()

   
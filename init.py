import sys
import napari
import numpy as np
from PyQt5.QtWidgets import * 
from filedialog import FileDialog

# window pops up with "Continue on Existing Case", "Initiate a New Case"
# "Initiate New Case" --> .npy path, save folder (or default)
# "Continue on Existing Case" --> opens last saved session
# first show max intense flourescence z projection
# users annotate these first
# then they specify the rest of the box
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # text
        self.title = "3D Biondi Body Client"
        self.description = """<h1>3D Biondi Body Client</h1>
                            <body>Continue on Existing Case: Continue work on a previous case. </body> 
                            <body> Initiate New Case: Create a new case </body>"""
        
        # properties
        self.x = 300
        self.y = 300
        self.width = 400
        self.height = 150

        # components (widgets)
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.existing_btn = QPushButton('Continue on Existing Case', self)
        self.new_btn = QPushButton('Initiate New Case', self)
        
        # initialize UI
        self.init_UI()

    def init_UI(self):
        """
        Initialize text/buttons for the main window.
        """

        # set up central widget
        self.layout.addWidget(QLabel(self.description))

        self.layout.addWidget(self.existing_btn)
        self.existing_btn.clicked.connect(self.button_clicked)

        self.layout.addWidget(self.new_btn)
        self.new_btn.clicked.connect(self.button_clicked)

        self.central_widget.setLayout(self.layout)

        # set up window properties 
        self.statusBar()
        self.setCentralWidget(self.central_widget)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle(self.title)
        self.show()

    def button_clicked(self):
        """
        Button event handler.
        """
        self.hide()
        sender = self.sender()
        if sender.text() == 'Initiate New Case':
            self.statusBar().showMessage('Initiating New Case')
            file_dlg = FileDialog(self)
        elif sender.text() == 'Continue on Existing Case':
            # TODO
            pass


def main():
    # construct app
    app = QApplication([])
    app.setStyle('Fusion')

    # construct and show main window
    m = MainWindow()

    # run
    sys.exit(app.exec_())


if __name__=="__main__":
    main()
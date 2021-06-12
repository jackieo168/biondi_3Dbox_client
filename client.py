import sys
import napari
import numpy as np 
from PyQt5.QtWidgets import *

# window pops up with "Continue on Existing Case", "Initiate a New Case"
# "Initiate New Case" --> .npy path, save folder (or default)
# "Continue on Existing Case" --> opens last saved session
# first show max intense flourescence z projection
# users annotate these first
# then they specify the rest of the box
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # vertical layout, add text/buttons for home screen
        window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome"))
        existing_btn = QPushButton('Continue on Existing Case', self)
        new_btn = QPushButton('Initiate New Case', self)
        layout.addWidget(existing_btn)
        layout.addWidget(new_btn)
        window.setLayout(layout)

        existing_btn.clicked.connect(self.buttonClicked)
        new_btn.clicked.connect(self.buttonClicked)

        self.statusBar()
        self.setCentralWidget(window)
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle("3D Biondi Body Client")
        self.show()

    def buttonClicked(self, e):
        sender = self.sender()
        if sender.text() == 'Initiate New Case':
            self.statusBar().showMessage('Initiating New Case')


def main():
    # construct app
    app = QApplication([])
    app.setStyle('Fusion')

    # main screen
    m = Main()

    # run
    sys.exit(app.exec_())


if __name__=="__main__":
    main()

# test_arr1 = np.load("data/A18-1 HuChP ThS + Hoechst 2 spacer 40x.npy")
# # test_arr2 = np.load("data/UCI-9-18 HuChP ThS + Hoechst 2 spacer 40x 3.npy")
# # test_arr3 = np.load("data/UCI-43-18 HuChP ThS + Hoechst 2 spacer 40x 2.npy")
# test_arr1_max = np.max(test_arr1, axis=0)
# # test_arr2_max = np.max(test_arr2, axis=0)
# # test_arr3_max = np.max(test_arr3, axis=0)
# viewer = napari.Viewer()
# image_layer1 = viewer.add_image(test_arr1_max, name='sample1',rgb=True)
# # image_layer2 = viewer.add_image(test_arr2_max, name='sample2',rgb=True)
# # image_layer3 = viewer.add_image(test_arr3_max, name='sample3',rgb=True)

# # shapes_layer = viewer.add_shapes(
# #     face_color='transparent',
# #     edge_color='green',
# #     name='bounding box',
# # )
# napari.run()

# """
# Perform a segmentation and annotate the results with
# bounding boxes and text
# """
# from skimage import data
# from skimage.filters import threshold_otsu
# from skimage.segmentation import clear_border
# from skimage.measure import label, regionprops_table
# from skimage.morphology import closing, square, remove_small_objects


# def segment(image):
#     """Segment an image using an intensity threshold determined via
#     Otsu's method.

#     Parameters
#     ----------
#     image : np.ndarray
#         The image to be segmented

#     Returns
#     -------
#     label_image : np.ndarray
#         The resulting image where each detected object labeled with a unique integer.
#     """
#     # apply threshold
#     thresh = threshold_otsu(image)
#     bw = closing(image > thresh, square(4))

#     # remove artifacts connected to image border
#     cleared = remove_small_objects(clear_border(bw), 20)

#     # label image regions
#     label_image = label(cleared)

#     return label_image


# def make_bbox(bbox_extents):
#     """Get the coordinates of the corners of a
#     bounding box from the extents

#     Parameters
#     ----------
#     bbox_extents : list (4xN)
#         List of the extents of the bounding boxes for each of the N regions.
#         Should be ordered: [min_row, min_column, max_row, max_column]

#     Returns
#     -------
#     bbox_rect : np.ndarray
#         The corners of the bounding box. Can be input directly into a
#         napari Shapes layer.
#     """
#     minr = bbox_extents[0]
#     minc = bbox_extents[1]
#     maxr = bbox_extents[2]
#     maxc = bbox_extents[3]

#     bbox_rect = np.array(
#         [[minr, minc], [maxr, minc], [maxr, maxc], [minr, maxc]]
#     )
#     bbox_rect = np.moveaxis(bbox_rect, 2, 0)

#     return bbox_rect


# def circularity(perimeter, area):
#     """Calculate the circularity of the region

#     Parameters
#     ----------
#     perimeter : float
#         the perimeter of the region
#     area : float
#         the area of the region

#     Returns
#     -------
#     circularity : float
#         The circularity of the region as defined by 4*pi*area / perimeter^2
#     """
#     circularity = 4 * np.pi * area / (perimeter ** 2)

#     return circularity


# # load the image and segment it
# # image = data.coins()[50:-50, 50:-50]
# image = test_arr1_max[:,:,0]
# print(image.shape)
# label_image = segment(image)

# # create the properties dictionary
# # properties = regionprops_table(
# #     label_image, properties=('label', 'bbox', 'perimeter', 'area')
# # )
# # properties['circularity'] = circularity(
# #     properties['perimeter'], properties['area']
# # )

# # # create the bounding box rectangles
# # bbox_rects = make_bbox([properties[f'bbox-{i}'] for i in range(4)])

# # # specify the display parameters for the text
# # text_parameters = {
# #     'text': 'label: {label}\ncirc: {circularity:.2f}',
# #     'size': 12,
# #     'color': 'green',
# #     'anchor': 'upper_left',
# #     'translation': [-3, 0],
# # }

# # initialise viewer with coins image
# viewer = napari.view_image(label_image, name='coins', rgb=False)

# # # add the labels
# # label_layer = viewer.add_labels(label_image, name='segmentation')

# # shapes_layer = viewer.add_shapes(
# #     bbox_rects,
# #     face_color='transparent',
# #     edge_color='green',
# #     properties=properties,
# #     text=text_parameters,
# #     name='bounding box',
# # )

# napari.run()
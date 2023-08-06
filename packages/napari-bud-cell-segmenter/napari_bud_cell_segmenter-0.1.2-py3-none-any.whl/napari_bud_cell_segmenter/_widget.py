"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING
from scipy import ndimage

import pathlib
import numpy as np
from qtpy import QtCore
from skimage import io, measure
from skimage.filters import threshold_otsu as sk_threshold_otsu, gaussian, sobel
from skimage.segmentation import watershed
from skimage.measure import label
from skimage.morphology import local_minima
from skimage.feature import blob_dog, blob_log, blob_doh

import magicgui
from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QGridLayout
import pandas as pd
#from napari_segment_blobs_and_things_with_membranes import thresholded_local_minima_seeded_watershed

if TYPE_CHECKING:
    import napari

class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
    
        # Preprocessing Widgets 
        bud_button = QPushButton("Draw Bud", self)
        bud_button.clicked.connect(self._draw_bud)
        
        mask_button = QPushButton("Create Mask", self)
        mask_button.clicked.connect(self._add_mask)

        # Layout 
        #self.preprocessing_layout=QGridLayout()
        self.preprocessing_layout=QVBoxLayout()
        self.preprocessing_layout.setSpacing(15)
        self.preprocessing_layout.setContentsMargins(10, 10, 10, 10)
        self.preprocessing_layout.setAlignment(QtCore.Qt.AlignBottom)
        
        # Adding the widgets to the layout
        self.preprocessing_layout.addWidget(bud_button)#, 0, 0)
        self.preprocessing_layout.addWidget(mask_button)#, 1, 0)
        self.setLayout(self.preprocessing_layout)

        #self.viewer.window.add_dock_widget(self._segment_seeded_watershed, area ='right', name = "Cells Segmentation")

    
    def _draw_bud(self, button):        
        self.viewer.add_shapes(name='bud', shape_type='polygon', face_color='darkorange', edge_color='darkorange', opacity=0.2)
        

    def _add_mask(self, button):

        # Create shape of the same size as the channel data
        data = self.viewer.layers[0].data
        mask_shape =  np.shape(np.squeeze(data))
        print("\nmask_shape: ", mask_shape)

        # Compute the mask
        bud_mask = self.viewer.layers['bud'].to_masks(mask_shape = mask_shape)
        print("\nbud_mask_shape: ",  np.shape(bud_mask))
        bud_mask = np.squeeze(bud_mask)
        print("\nbud_mask_shape: ",  np.shape(bud_mask))

        # Cropp the channels according to the mask
        #data = self.viewer.layers["ch4"].data
        #print("data_shape:", np.shape(data))

        ch1_cropped = np.zeros(np.shape(data))
        ch2_cropped = np.zeros(np.shape(data))
        ch3_cropped = np.zeros(np.shape(data))
        ch4_cropped = np.zeros(np.shape(data))

        ch1_cropped[bud_mask] = self.viewer.layers["ch1"].data[bud_mask]
        ch2_cropped[bud_mask] = self.viewer.layers["ch2"].data[bud_mask]
        ch3_cropped[bud_mask] = self.viewer.layers["ch3"].data[bud_mask]
        ch4_cropped[bud_mask] = self.viewer.layers["ch4"].data[bud_mask]

        # Compute distance map and add it to the viewer
        bud_distancemap = ndimage.distance_transform_edt(bud_mask)
        self.viewer.add_image(bud_mask, visible=False)
        self.viewer.add_image(ch1_cropped, colormap="red", visible=False)
        self.viewer.add_image(ch2_cropped, colormap="green", visible=False)
        self.viewer.add_image(ch3_cropped, colormap="blue", visible=False)
        self.viewer.add_image(ch4_cropped, colormap="gray", visible=True)
        self.viewer.add_image(bud_distancemap, visible=False)

        # Activate ch4_cropped layer 
        #self.viewer.layers.selection.active = self.viewer.layers["ch4_cropped"]


class ManualCorrectionsQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
    
        # Manual correction Widgets 
        correction_button = QPushButton("Manual Corrections", self)
        correction_button.clicked.connect(self._manual_corrections)

        merge_button = QPushButton("Merge", self)
        merge_button.clicked.connect(self._merge_labels)

        split_button = QPushButton("Split", self)
        split_button.clicked.connect(self._split_labels)

        # Layout 
        self.correction_layout=QVBoxLayout()
        self.correction_layout.setSpacing(15)
        self.correction_layout.setContentsMargins(10, 10, 10, 10)
        self.correction_layout.setAlignment(QtCore.Qt.AlignBottom)
        
        # Adding the widgets to the layout
        self.correction_layout.addWidget(correction_button)
        self.correction_layout.addWidget(merge_button)
        self.correction_layout.addWidget(split_button)
        self.setLayout(self.correction_layout)

    def _manual_corrections(self, button):
        points_layer = self.viewer.add_points([])
        points_layer.mode = 'ADD'

    def _merge_labels(self, button):

        # Select the point and label layers
        points_layer = self.viewer.layers['Points']
        labels_layer = self.viewer.layers["segment_seeded_watershed result"]
       
        # Access the point and label layers's data 
        points = points_layer.data
        labels = np.asarray(labels_layer.data)

        label_ids = [labels.item(tuple([int(j) for j in i])) for i in points]

        # Replace labels with minimum of the selected labels
        new_label_id = min(label_ids)
        for l in label_ids:
            if l != new_label_id:
                labels[labels == l] = new_label_id

        labels_layer.data = labels
        points_layer.data = []

    def _split_labels(self, button):
        
        # Select the point and label layers
        points_layer = self.viewer.layers['Points']
        labels_layer = self.viewer.layers["segment_seeded_watershed result"]

        # Access the point and label layers's data 
        labels = np.asarray(labels_layer.data)
        points = points_layer.data

        label_ids = [labels.item(tuple([int(j) for j in i])) for i in points]

        # make a binary image first
        binary = np.zeros(labels.shape, dtype=bool)
        new_label_id = min(label_ids)
        for l in label_ids:
            binary[labels == l] = True

        # origin: https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_watershed.html
        from scipy import ndimage as ndi
        from skimage.segmentation import watershed
        #from skimage.feature import peak_local_max

        #distance = ndi.distance_transform_edt(binary)
        #coords = peak_local_max(distance, footprint=np.ones((3, 3)), labels=binary)
        mask = np.zeros(labels.shape, dtype=bool)
        for i in points:
            #mask[tuple(points)] = True
            mask[tuple([int(j) for j in i])] = True

        markers, _ = ndi.label(mask)
        new_labels = watershed(binary, markers, mask=binary)
        labels[binary] = new_labels[binary] + labels.max()

        labels_layer.data = labels
        points_layer.data = []




@magic_factory(call_button="Load", filename={"label": "Select a .tiff file:"})
def load_data(filename=pathlib.Path()) -> "napari.types.LayerDataTuple":
    """
    Widget to select a multichannel .tiff image to be loaded. 
    Splits the images in the different channels and add them to the viewer. 

    Returns
    -------
    list[napari.types.LayerDataTuple]
        list of tuple of (data, meta, 'labels') for consumption by napari
    """
    
    # Image Loading and reshaping
    im_ori = io.imread(filename)
    im_ori = np.transpose(im_ori, (2,0,1))
    im_ori = np.reshape(im_ori, (1, 4, np.shape(im_ori)[1], np.shape(im_ori)[2]))
    print("np.shape(im_ori): ", np.shape(im_ori))
    
    # Image Splitting
    list_channels = [im_ori[0,0,:,:], im_ori[0,1,:,:], im_ori[0,2,:,:], im_ori[0,3,:,:]]
    list_layer_type = 'image'
    list_metadata = [{'name': "ch1", 'colormap': "red"},
                     {'name': "ch2", 'colormap': "green"},
                     {'name': "ch3", 'colormap': "blue"},
                     {'name': "ch4", 'colormap': "gray"}]
    
    # Return a list of LayerDataTuple
    layer_list = []
    for idx in range(len(list_channels)):
        layer_list.append((list_channels[idx], list_metadata[idx], 'image'))

    return layer_list


@magic_factory(call_button="Segment")
#def local_minima_seeded_watershed(image:"napari.types.ImageData", spot_sigma: float = 10, outline_sigma: float = 0) -> "napari.types.LabelsData":
def segment_seeded_watershed(image:"napari.types.ImageData", spot_sigma: float = 10, outline_sigma: float = 0) -> "napari.types.LabelsData":
    """
    Segment cells in images with fluorescently marked membranes.
    The two sigma parameters allow tuning the segmentation result. The first sigma controls how close detected cells
    can be (spot_sigma) and the second controls how precise segmented objects are outlined (outline_sigma). Under the
    hood, this filter applies two Gaussian blurs, local minima detection and a seeded watershed.
    See also
    --------
    .. [1] https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_watershed.html
    """

    image = np.asarray(image)
    spot_blurred = gaussian(image, sigma=spot_sigma)
    spots = label(local_minima(spot_blurred))

    if outline_sigma == spot_sigma:
        outline_blurred = spot_blurred
    else:
        outline_blurred = gaussian(image, sigma=outline_sigma)

    return watershed(outline_blurred, spots)

@magic_factory(call_button="Detect blobs")
def detect_blobs(image:"napari.types.ImageData", max_sigma: float = 20, threshold: float = 0.01)-> "napari.types.LayerDataTuple":
    
    # https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.blob_log
    # Normalize the image between 0 and 1 before detection 
    image_normalized = (image - np.min(image)) / (np.max(image) - np.min(image))

    # Compute Laplacian of Gaussian (raddi in the 3rd column)
    blobs_log = blob_log(image_normalized, max_sigma=max_sigma, num_sigma=1, threshold=threshold)
    #blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2) 

    data_layer = []
    for blob in blobs_log:
        data_layer.append(blob[0:2])
    data_layer = np.array(data_layer)

    print("blobs_log[0,:]: ", blobs_log[0,:])
    print("data_layer: ", np.shape(data_layer))
    print("data_layer[0,:]: ", data_layer[0,:])

    # Create a new point layer 
    points_layer = (data_layer, {}, 'points')
    
    return points_layer

@magic_factory(call_button="Statistics")
def disp_statitics(labels:"napari.types.LabelsData", image:"napari.types.ImageData"):
    info_table = pd.DataFrame(
    measure.regionprops_table(
        labels,
        intensity_image=image,
        properties=['label', 'slice', 'area', 'perimeter', 'centroid', 'mean_intensity'])
    ).set_index('label')

    print(info_table.head())
    


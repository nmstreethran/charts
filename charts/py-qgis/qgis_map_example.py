# import libraries
import os
from glob import glob
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsProcessingFeedback
)
from qgis import processing
from processing.core.Processing import Processing

# create a reference to the QgsApplication
# setting the second argument to False disables the GUI
qgs = QgsApplication([], True)

# load providers
qgs.initQgis()

# initialise processing
Processing.initialize()

# get the project instance
project = QgsProject.instance()

# set feedback
feedback = QgsProcessingFeedback()


# function to add raster layer to project
def add_raster_layer(layer_path, layer_title=None):
    """Add a raster data layer to the map
    Parameters:
    -----------
    `layer_path`: layer's file path \
    `layer_title`: optional layer title
    """
    rlayer = QgsRasterLayer(layer_path, layer_title)
    if not rlayer.isValid():
        print("Layer invalid! " + str(rlayer))
    else:
        project.addMapLayer(rlayer)


# function to add vector layer to project
def add_vector_layer(layer_path, layer_title=None):
    """Add a vector data layer to the map
    Parameters:
    -----------
    `layer_path`: layer's file path \
    `layer_title`: optional layer title
    """
    vlayer = QgsVectorLayer(layer_path, layer_title, "ogr")
    if not vlayer.isValid():
        print("Layer invalid! " + str(vlayer))
    else:
        project.addMapLayer(vlayer)


# add list of rasters
rlist = glob(os.path.join("data", "isle_of_may", "*.tif"))
for raster in rlist:
    add_raster_layer(raster, os.path.split(raster)[1][:4])

# add vector layers
add_vector_layer(os.path.join("data", "layer.shp"))
add_vector_layer(
    os.path.join("data", "data.gpkg|layername=layer"), "boundary_line"
)

# set raster style using QML file
for raster in rlist:
    params = {
        "INPUT": raster,
        "STYLE": "py-qgis/colombia_relief_colours.qml"
    }
    processing.run("native:setlayerstyle", params, feedback=feedback)

# save the project
project.write(os.path.join("py-qgis", "example_map.qgz"))

# remove the provider and layer registries from memory
qgs.exitQgis()

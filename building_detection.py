# Building extraction 

## https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/expressions.html


import requests
import json
from qgis.core import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *
import qgis.analysis
import processing

# I K-Means Filter

rasterLyr = QgsRasterLayer("/home/administrator/Desktop/Python_Projects_Harald/Data/Madrid/LayerStackMadrid_Sentinel2.tif", "Madrid")

parameters = {'GRIDS': rasterLyr, 
                'METHOD': 1, 
                'NCLUSTER': 7,
                'MAXITER': 5,
                'STATISTICS': "/home/administrator/Desktop/Python_Projects_Harald/Data/Results/statistics",
                'CLUSTER': "/home/administrator/Desktop/Python_Projects_Harald/Data/Results/kmean"}

processing.runAndLoadResults('saga:kmeansclusteringforgrids', parameters)


#II Filter all values representing buildings using the raster calculator

rasterLyr = QgsRasterLayer("/home/administrator/Desktop/Python_Projects_Harald/Data/Results/kmean.tif", "kmean")

parameters = {'LAYERS': rasterLyr, 
                'EXPRESSION': "kmean@1 = 1", 
                'OUTPUT': "/home/administrator/Desktop/Python_Projects_Harald/Data/Results/filtered.tif"}

processing.runAndLoadResults('qgis:rastercalculator', parameters)




# Convert result to geotiff

rasterLyr = QgsRasterLayer("/home/administrator/Desktop/Python_Projects_Harald/Data/Results/kmean.sdat", "kmean")

parameters = {'INPUT': rasterLyr, 
                'OUTPUT': "/home/administrator/Desktop/Python_Projects_Harald/Data/Results/kmean.tif"}

processing.runAndLoadResults('gdal:translate', parameters)




#II Morphological filter

rasterLyr = QgsRasterLayer("/home/administrator/Desktop/Python_Projects_Harald/Data/Madrid/LayerStackMadrid_Sentinel2.tif", "Madrid")
rasterLyr.isValid()

parameters = {'INPUT': rasterLyr, 
                'MODE': 1, 
                'RADIUS': 1,
                'METHOD': 3,
                'RESULT': "/home/administrator/Desktop/Python_Projects_Harald/Data/Results/temp"}

#Python identifiers to define the parameters can be looked up in the toolbox
#The output for the SAGA filter are in the format sdat, this can be converted to geotiff

processing.runAndLoadResults('saga:morphologicalfilter', parameters)

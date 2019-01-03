# Building extraction 

## https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/expressions.html

#TO DO: Add the path to the QGGIS specific python interpretor


#Ressources: 
#https://geoscripting-wur.github.io/PythonWeek/

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Harald
"""

'''
#Setup PyQGIS to use with external IDE
QgsApplication.setPrefixPath("/usr", True)
# Load providers
QgsApplication.initQgis()
# Show setting of parameters
'''


# Prepare the environment and initialize processing to call from external IDE e.g. Spyder or PyCharm 

from qgis.core import *
import sys
import qgis.analysis
sys.path.append('/usr/share/qgis/python/plugins')
#Initialize Processing
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *
import processing
#from processing.core.Processing import Processing


#Find path to python interpretpr
import sys

print(sys.executable)

#Set the QGIS prefix to work outside QGIS
qgis_prefix="/usr" 

# I K-Means Filter

test = QgsRasterLayer("/home/administrator/Desktop/Python_Projects_Harald/Data/Madrid/LayerStackMadrid_Sentinel2.tif", "Madrid")

parameters = {'GRIDS': test, 
                'METHOD': 1, 
                'NCLUSTER': 7,
                'MAXITER': 5,
                'STATISTICS': "/home/administrator/Desktop/Python_Projects_Harald/Data/Results/statistics",
                'CLUSTER': "/home/administrator/Desktop/Python_Projects_Harald/Data/Results/test"}

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

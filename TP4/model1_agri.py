"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32208
"""
        
#Una vez añadido el raster layer, vamos a processing toolbox para crear el primer modelo. 

#Setup necesario para poder correr los comando fuera de qgis

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing

#seteamos 

mainpath = "/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/input"
suitin = "{}/SUIT/suit/hdr.adf".format(mainpath)
adm2in = "{}/gadm41_USA_shp/gadm41_USA_2.shp".format(mainpath)
outpath = "{}/_output/counties_agrisuit.csv".format(mainpath)
junkpath = "{}/_output/junk".format(mainpath)
junkfile = "{}/_output/junk/agrisuit.tif".format(mainpath)
if not os.path.exists(mainpath + "/_output"):
    os.mkdir(mainpath + "/_output")
if not os.path.exists(junkpath):
    os.mkdir(junkpath)



#Se crean los algoritmos

class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Agrisuit', 'agrisuit', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Counties', 'counties', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonal', 'Zonal', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}
        
# definimos WGS 84 SR
crs_wgs84 = QgsCoordinateReferenceSystem("epsg:4326")

#######################################
######### Warp (reproject)#############

#Reproyectamos el shp suit, lo cual es muy importante en mapas porque les da distintas formas y tamaños. 
#Nombramos al nuevo raster como agrisuit.


        alg_params = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': 'suit_e05c7935_08a7_4538_aaea_f43e3f359bf5',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Nearest Neighbour
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),#esta es la coordenada agregada.
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Agrisuit']
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Agrisuit'] = outputs['WarpReproject']['OUTPUT']
        return results
    
#######################################
######### Drop field(s)################

#Limpiamos el shapefile de los Estados de Estados Unidos junto a sus counties dropeando variables que no vamos a necesitar. 
#No le ponemos no,bre a la nueva base, no es necesario.

        alg_params = {
            'COLUMN': ['GID_0','NAME_0','GID_1','GID_2','HASC_2','CC_2','TYPE_2','NL_NAME 2','VARNAME_2','NL_NAME_1','NL_NAME_2',' ENGTYPE_2'],
            'INPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/input/gadm41_USA_shp/gadm41_USA_2.shp',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

    
####################################################
######### Add autoincremental field ################


#Usamos autoincremental tool y vamos a enumerar a partir de la base con las variables dropeadas.
#Creamos un layer que se llama 'counties'.

        alg_params = {
            'FIELD_NAME': 'cid',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['DropFields']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Counties']
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Counties'] = outputs['AddAutoincrementalField']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

###########################################
######### Zonal statistics ################

#Para hacer estadísticas de raster usamos el algorimo 'zonal statistics'.
# A partir del input layer counties y del raster layer agrisuit tomamos el promedio de las el promedio de las estadísticas del raster en los counties.
# Nombramos a esta nueva layer como Zonal que es una tabla con estadísticas. 

        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Incremented_3450c202_4909_4f3e_9750_85d8671a535f',
            'INPUT_RASTER': 'OUTPUT_cddc91f2_8132_4115_89ee_22eaa352e96d',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Zonal']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Zonal'] = outputs['ZonalStatistics']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        
###################################################################
# write to CSV
###################################################################
# Esto fue extraído de clean 
print('outputting the data')

with open(outpath, 'w') as output_file:
    fieldnames = [field.name() for field in counties_fields_autoid.fields()]
    line = ','.join(name for name in fieldnames) + '\n'
    output_file.write(line)
    for f in counties_fields_autoid.getFeatures():
        line = ','.join(str(f[name]) for name in fieldnames) + '\n'
        output_file.write(line)

print('DONE!')

    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()

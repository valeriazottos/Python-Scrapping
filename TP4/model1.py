"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32208
"""
# seteamos los  paths de inputs y  outputs
mainpath = "/Users/magibbons/Desktop/Herramientas/Clae5/input"
outpath = "{}/output".format(mainpath)


#Setup necesario para poder correr los comando fuera de qgis
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

#Primero agregamos el shapefile de langa.shp como layer 

#########################################
######## Fix geometries ###############


#arregalmos la geormetría para procesar el shapefile de idiomas
#lo guardamos con el nommbre de fix_geo

        alg_params = {
            'INPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/input/langa/langa.shp',
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['FixGeometries']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

################################################
######## Add autoincremental field ###############

#Usamos commo input layer a FixGeometries, vamos a llamarlo al nombre de campo como GID y seteamos que el valor arranque desde 1. 
#Llamamos a la layer 'autoinc_id'
# Con esto logramos que estén enumerados los tipos de idiomas.

        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AddAutoincrementalField']['OUTPUT']
        return results

#########################################
######## Field calculator###############

#Agarramos la última base trabajada para agregarle una columna que tenga la cantidad de idiomas hablados por país.
#la nombramos length y pedimos que el field name se llame 'length'y que no tenga más de 2 dígitos.
#llamamos a la variable 'length(NAME_PROP)' 
#nombramos a la nueva base como length

        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Integer
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': 'Incremented_5f216592_418f_41a3_874c_1000c1894022',
            'OUTPUT': parameters['Length']
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        
########################################
######## Feature filter###############

#se toma como input layer a length
#queremos que el output name sea = menor_a_11 ya que los valores que adquirirá la variable son aquellos en que la variable length<11.

        alg_params = {
            'INPUT': 'Calculated_3f216ae1_ec9c_4130_b22f_829446a1f10b',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FeatureFilter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FeatureFilter']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
        
        
#########################################
######## Field calculator###############

#tomar como input layer a 'OUTPUT_menor_a_11'
#llamamos a la variable lnm, con field length de 10.
#seleccionar string como resulltado de field type.
#usamos la expresión "NAME_PROP".
#nombramos a la nueva layer como 'field_calc'



        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lnm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # String
            'FORMULA': '"NAME_PROP"',
            'INPUT': 'menor_a_11_4fd0d0ce_ac57_4e02_ad5a_403da5a0ac73',
            'OUTPUT': parameters['Field_calc']
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

#########################################
######## Drop field(s) ##################

#borramos columnas que no vamos a necesitar a partir de 'field_calc'.
#llamamos a la nueva layer como wldsout.
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': 'Calculated_7b6b91ad_2f15_442d_98f6_8916ed88256f',
            'OUTPUT': parameters['Wldsout']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
       
#######################################################
#############Para exportar a csv#######################

        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'wldsout',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/output/clean.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)



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

#comentarios  estructuras guiados por el trabajo en: sebastianhohmann/gis_course

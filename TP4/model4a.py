"""
Model exported as python.
Name : model4a
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

class Model4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Fix geometries - countries: usamos la base clean.shp, la corregimos a través de la herramienta fix geometries en QGIS y lo renombramos fixgeo_countries.
        alg_params = {
            'INPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Vector overlay--> Intersection: unimos ambos(fixgeo_wlds y fixgeo_countries). De la input layer (fixgeo_wlds) nos quedamos con la variable GID y de la overlay layer (fixgeo_countries) nos quedamos con la variable ADMIN. Nombramos a esta intersección como "intersection"
        # Esto lo que hace es que en cada país nos cuenta la cantidad de áreas que intersecan ambas variables: contar por cada país cuantos idiomas aparecen
        alg_params = {
            'INPUT': 'Fixed_geometries_ebe6d4e3_d8f4_4710_99e1_b56449d9af28',
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': 'Fixed_geometries_2392ecc8_28aa_4b77_9943_53895797ff01',
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        outputs['Intersection'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Intersection']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Fix geometries - wlds: usamos la base clean.shp, la corregimos a través de la herramienta fix geometries en QGIS y lo renombramos fixgeo_wlds.
        alg_params = {
            'INPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/output/clean.shp',
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        outputs['FixGeometriesWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['FixGeometriesWlds']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Statistics by categories : usamos como output: "intersection" (capa creada previamente), y calculamos el campo ADMIN--> lo llamamos outputcsv. Lo que genera esto es una tabla que calcula cuantas veces estaba en la base de languages cada uno de los países (languages by country).
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': 'Intersection_ab0ae4b2_b9d9_4231_97d4_caed37a04dd5',
            'OUTPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/output/languages_by_country.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model4a'

    def displayName(self):
        return 'model4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4a()


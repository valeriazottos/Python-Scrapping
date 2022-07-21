"""
Model exported as python.
Name : model4b
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorDestination('Distout', 'distout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Nearout', 'nearout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Country_centroids', 'country_centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust_dropfields', 'nearest_cat_adjust_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixegeo_countries', 'fixegeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined', 'centroids_nearest_coast_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_distance_joined', 'centroids_nearest_coast_distance_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_w_coord', 'centroids_w_coord', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}

        # Extract by attribute
        alg_params = {
            'FIELD': 'distance',
            'INPUT': 'Vertices_e2d3c689_9247_456b_95af_13e7ec7be064',
            'OPERATOR': 2,  # >
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtractByAttribute']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes - lat_lon_drop
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': 'Remaining_fields_93de1f30_4209_4a4c_bbc4_034b7f895911',
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['AddGeometryAttributesLat_lon_drop'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AddGeometryAttributesLat_lon_drop']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Centroids
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': 'Fixed_geometries_81c5284c_bce7_4057_a71b_843998c64e07',
            'OUTPUT': parameters['Country_centroids']
        }
        outputs['Centroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Country_centroids'] = outputs['Centroids']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # v.distance
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,  # auto
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': 'Added_geom_info_1ffb65aa_0b9f_4f0a_a89e_6ccff4be9c1f',
            'from_type': [0,1,3],  # point,line,area
            'to': 'Remaining_fields_7738e368_1eb4_4636_ac47_231a2bfff38a',
            'to_column': '',
            'to_type': [0,1,3],  # point,line,area
            'upload': [0],  # cat
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Field calculator - cent_lat
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'ycoord')",
            'INPUT': 'Extracted__attribute__2693c1ed_7ae7_4013_80ff_e5bcf53dbb35',
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['FieldCalculatorCent_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['FieldCalculatorCent_lat']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Field calculator - cat adjust
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': "attribute($currentfeature, 'cat')-1",
            'INPUT': 'from_output_69bbf966_d762_467d_89b0_f4a86493e3bc',
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['FieldCalculatorCatAdjust'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['FieldCalculatorCatAdjust']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Drop field(s) - centroids_coast_joined
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': 'Joined_layer_44034d24_0d10_4045_9cc7_bc4516c4dd6f',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['DropFieldsCentroids_coast_joined'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['DropFieldsCentroids_coast_joined']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Drop field(s) - centroids_w_coord
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': 'Added_geom_info_1ffb65aa_0b9f_4f0a_a89e_6ccff4be9c1f',
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['DropFieldsCentroids_w_coord'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['DropFieldsCentroids_w_coord']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - centroids y coast
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': 'Remaining_fields_31e2ea90_fedc_4fdf_b4db_19112aa36736',
            'INPUT_2': 'Remaining_fields_6197dab1_fa02_4907_8c47_06da29dc6dd3',
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['JoinAttributesByFieldValueCentroidsYCoast'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['JoinAttributesByFieldValueCentroidsYCoast']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': 'Centroids_498eaa86_4596_4e93_8e12_f658405b5480',
            'OUTPUT': parameters['Centroids_w_coord']
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_w_coord'] = outputs['AddGeometryAttributes']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Field calculator - coast_lon
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'xcoord')",
            'INPUT': 'Calculated_dc45eb97_0b77_43de_8105_10b16f0e8b87',
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['FieldCalculatorCoast_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['FieldCalculatorCoast_lon']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Extract vertices
        alg_params = {
            'INPUT': 'Joined_layer_e36e26be_2a2f_4cc7_9ec1_0494d1d6d1f1',
            'OUTPUT': parameters['Extract_vertices']
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Fix geometries - countries
        alg_params = {
            'INPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixegeo_countries']
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixegeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Fix geometries - coast
        alg_params = {
            'INPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/input/ne_10m_coastline/ne_10m_coastline.shp',
            'OUTPUT': parameters['Fixgeo_coast']
        }
        outputs['FixGeometriesCoast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['FixGeometriesCoast']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Drop field(s) - cent_lat_lon
        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': 'Calculated_1febcb44_99b7_4ad6_8df0_54b413eb9914',
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        outputs['DropFieldsCent_lat_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['DropFieldsCent_lat_lon']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'xcoord')",
            'INPUT': 'Calculated_935323a0_aa0a_403b_b68d_ec8afcdb4f82',
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Drop field(s) - fixgeo_coast
        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': 'Fixed_geometries_41af6722_536f_4c86_aed8_1dde5e9411a3',
            'OUTPUT': parameters['Coastout']
        }
        outputs['DropFieldsFixgeo_coast'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['DropFieldsFixgeo_coast']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Drop field(s) - add_coast_lon
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_fd73bf0a_3d83_4f09_be3d_7e5ca750ef1e',
            'OUTPUT': '/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/Clae 4/output/csvout.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFieldsAdd_coast_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Drop field(s) - cat_adjust
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_b7db16d1_69b1_490c_98a6_2fda30dec724',
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        outputs['DropFieldsCat_adjust'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['DropFieldsCat_adjust']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': 'output_cb82fa8d_2c81_4389_bc51_8ca9fa3242f5',
            'INPUT_2': 'Remaining_fields_a674d71a_77bf_4cf7_a619_b70b11914fd7',
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_distance_joined']
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_distance_joined'] = outputs['JoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Field calculator - add_geo_coast
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'ycoord')",
            'INPUT': 'Added_geom_info_2f8384cb_dd6a_44cc_8d46_3eed4b8a6254',
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['FieldCalculatorAdd_geo_coast'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['FieldCalculatorAdd_geo_coast']['OUTPUT']
        return results

    def name(self):
        return 'model4b'

    def displayName(self):
        return 'model4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4b()

# # -*- coding: utf-8 -*-
# import inspect
# import json  # noqa: F401
# import os  # noqa: F401
# import shutil
# import time
# import unittest
# from os import environ

# import pandas as pd
# from configparser import ConfigParser  # py2

# from GenericsAPI.GenericsAPIImpl import GenericsAPI
# from GenericsAPI.GenericsAPIServer import MethodContext
# from GenericsAPI.authclient import KBaseAuth as _KBaseAuth
# from DataFileUtil.DataFileUtilClient import DataFileUtil
# from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
# from Workspace.WorkspaceClient import Workspace as workspaceService


# class GenericsAPITest(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         token = environ.get('KB_AUTH_TOKEN', None)
#         config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
#         cls.cfg = {}
#         config = ConfigParser()
#         config.read(config_file)
#         for nameval in config.items('GenericsAPI'):
#             cls.cfg[nameval[0]] = nameval[1]
#         # Getting username from Auth profile for token
#         authServiceUrl = cls.cfg['auth-service-url']
#         auth_client = _KBaseAuth(authServiceUrl)
#         user_id = auth_client.get_user(token)
#         # WARNING: don't call any logging methods on the context object,
#         # it'll result in a NoneType error
#         cls.ctx = MethodContext(None)
#         cls.ctx.update({'token': token,
#                         'user_id': user_id,
#                         'provenance': [
#                             {'service': 'GenericsAPI',
#                              'method': 'please_never_use_it_in_production',
#                              'method_params': []
#                              }],
#                         'authenticated': 1})
#         cls.wsURL = cls.cfg['workspace-url']
#         cls.wsClient = workspaceService(cls.wsURL)
#         cls.serviceImpl = GenericsAPI(cls.cfg)
#         cls.scratch = cls.cfg['scratch']
#         cls.callback_url = os.environ['SDK_CALLBACK_URL']

#         cls.gfu = GenomeFileUtil(cls.callback_url)
#         cls.dfu = DataFileUtil(cls.callback_url)

#         suffix = int(time.time() * 1000)
#         cls.wsName = "test_GenericsAPI_" + str(suffix)
#         cls.wsClient.create_workspace({'workspace': cls.wsName})
#         cls.prepare_data()

#     @classmethod
#     def tearDownClass(cls):
#         if hasattr(cls, 'wsName'):
#             cls.wsClient.delete_workspace({'workspace': cls.wsName})
#             print('Test workspace was deleted')

#     @classmethod
#     def prepare_data(cls):

#         # upload genome object
#         genbank_file_name = 'minimal.gbff'
#         genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
#         shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

#         genome_object_name = 'test_Genome'
#         cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
#                                                     'workspace_name': cls.wsName,
#                                                     'genome_name': genome_object_name,
#                                                     'generate_ids_if_needed': 1
#                                                     })['genome_ref']

#         # upload AttributeMapping object
#         workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
#         object_type = 'KBaseExperiments.AttributeMapping'
#         attribute_mapping_object_name = 'test_attribute_mapping'
#         attribute_mapping_data = {'instances': {'test_instance_1': ['1-1', '1-2', '1-3'],
#                                                 'test_instance_2': ['2-1', '2-2', '2-3'],
#                                                 'test_instance_3': ['3-1', '3-2', '3-3']},
#                                   'attributes': [{'attribute': 'test_attribute_1',
#                                                   'attribute_ont_ref': 'attribute_ont_ref_1',
#                                                   'attribute_ont_id': 'attribute_ont_id_1'},
#                                                  {'attribute': 'test_attribute_2',
#                                                   'attribute_ont_ref': 'attribute_ont_ref_2',
#                                                   'attribute_ont_id': 'attribute_ont_id_2'},
#                                                  {'attribute': 'test_attribute_3',
#                                                   'attribute_ont_ref': 'attribute_ont_ref_3',
#                                                   'attribute_ont_id': 'attribute_ont_id_3'}],
#                                   'ontology_mapping_method': 'user curation'}
#         save_object_params = {
#             'id': workspace_id,
#             'objects': [{'type': object_type,
#                          'data': attribute_mapping_data,
#                          'name': attribute_mapping_object_name}]
#         }

#         dfu_oi = cls.dfu.save_objects(save_object_params)[0]
#         cls.attribute_mapping_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

#         cls.col_ids = ['instance_1', 'instance_2', 'instance_3', 'instance_4']
#         cls.row_ids = ['WRI_RS00050_CDS_1', 'WRI_RS00065_CDS_1', 'WRI_RS00070_CDS_1']
#         cls.values = [[0.1, 0.2, 0.3, 0.4],
#                       [0.3, 0.4, 0.5, 0.6],
#                       [None, None, None, None]]
#         cls.row_mapping = {'WRI_RS00050_CDS_1': 'test_instance_1',
#                            'WRI_RS00065_CDS_1': 'test_instance_2',
#                            'WRI_RS00070_CDS_1': 'test_instance_3'}
#         cls.col_mapping = {'instance_1': 'test_instance_1',
#                            'instance_2': 'test_instance_2',
#                            'instance_3': 'test_instance_3',
#                            'instance_4': 'test_instance_3'}
#         cls.feature_mapping = {'WRI_RS00050_CDS_1': 'WRI_RS00050_CDS_1',
#                                'WRI_RS00065_CDS_1': 'WRI_RS00065_CDS_1',
#                                'WRI_RS00070_CDS_1': 'WRI_RS00070_CDS_1'}

#         # upload ExpressionMatrix object
#         object_type = 'KBaseMatrices.ExpressionMatrix'
#         expression_matrix_object_name = 'test_expression_matrix'
#         expression_matrix_data = {'scale': 'log2',
#                                   'type': 'level',
#                                   'col_attributemapping_ref': cls.attribute_mapping_ref,
#                                   'col_mapping': cls.col_mapping,
#                                   'row_attributemapping_ref': cls.attribute_mapping_ref,
#                                   'row_mapping': cls.row_mapping,
#                                   'feature_mapping': cls.feature_mapping,
#                                   'data': {'row_ids': cls.row_ids,
#                                            'col_ids': cls.col_ids,
#                                            'values': cls.values
#                                            },
#                                   'genome_ref': cls.genome_ref}
#         save_object_params = {
#             'id': workspace_id,
#             'objects': [{'type': object_type,
#                          'data': expression_matrix_data,
#                          'name': expression_matrix_object_name}]
#         }

#         dfu_oi = cls.dfu.save_objects(save_object_params)[0]
#         cls.expression_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

#         expression_matrix_object_name = 'test_expression_matrix_no_attribute_mapping'
#         expression_matrix_data = {'scale': 'log2',
#                                   'type': 'level',
#                                   'data': {'row_ids': cls.row_ids,
#                                            'col_ids': cls.col_ids,
#                                            'values': cls.values
#                                            }}
#         save_object_params = {
#             'id': workspace_id,
#             'objects': [{'type': object_type,
#                          'data': expression_matrix_data,
#                          'name': expression_matrix_object_name}]
#         }

#         dfu_oi = cls.dfu.save_objects(save_object_params)[0]
#         cls.expression_matrix_nc_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

#         # upload FitnessMatrix object
#         object_type = 'KBaseMatrices.FitnessMatrix'
#         fitness_matrix_object_name = 'test_fitness_matrix'
#         fitness_matrix_data = {'scale': 'log2',
#                                'type': 'level',
#                                'row_attributemapping_ref': cls.attribute_mapping_ref,
#                                'row_mapping': cls.row_mapping,
#                                'data': {'row_ids': cls.row_ids,
#                                         'col_ids': cls.col_ids,
#                                         'values': cls.values
#                                         }}
#         save_object_params = {
#             'id': workspace_id,
#             'objects': [{'type': object_type,
#                          'data': fitness_matrix_data,
#                          'name': fitness_matrix_object_name}]
#         }

#         dfu_oi = cls.dfu.save_objects(save_object_params)[0]
#         cls.fitness_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

#         # upload DifferentialExpressionMatrix object
#         object_type = 'KBaseMatrices.DifferentialExpressionMatrix'
#         diff_expr_matrix_object_name = 'test_diff_expr_matrix'
#         diff_expr_matrix_data = {'scale': 'log2',
#                                  'type': 'level',
#                                  'col_attributemapping_ref': cls.attribute_mapping_ref,
#                                  'col_mapping': cls.col_mapping,
#                                  'data': {'row_ids': cls.row_ids,
#                                           'col_ids': cls.col_ids,
#                                           'values': cls.values
#                                           }}
#         save_object_params = {
#             'id': workspace_id,
#             'objects': [{'type': object_type,
#                          'data': diff_expr_matrix_data,
#                          'name': diff_expr_matrix_object_name}]
#         }

#         dfu_oi = cls.dfu.save_objects(save_object_params)[0]
#         cls.diff_expr_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

#     def getWsClient(self):
#         return self.__class__.wsClient

#     def getWsName(self):
#         return self.__class__.wsName

#     def getImpl(self):
#         return self.__class__.serviceImpl

#     def getContext(self):
#         return self.__class__.ctx

#     def start_test(self):
#         testname = inspect.stack()[1][3]
#         print('\n*** starting test: ' + testname + ' **')

#     def fail_fetch_data(self, params, error, exception=ValueError,
#                         contains=False):
#         with self.assertRaises(exception) as context:
#             self.getImpl().fetch_data(self.ctx, params)
#         if contains:
#             self.assertIn(error, str(context.exception.args))
#         else:
#             self.assertEqual(error, str(context.exception.args[0]))

#     def check_fetch_data_output(self, returnVal):
#         self.assertTrue('data_matrix' in returnVal)
#         data_matrix = json.loads(returnVal.get('data_matrix'))

#         col_ids = list(data_matrix.keys())
#         self.assertCountEqual(col_ids, self.col_ids)
#         for col_id in col_ids:
#             self.assertCountEqual(list(data_matrix.get(col_id).keys()), self.row_ids)

#     def check_export_matrix_output(self, returnVal):
#         self.assertTrue('shock_id' in returnVal)

#         result_dir = os.path.join(self.scratch, 'export_matrix_result')
#         if not os.path.exists(result_dir):
#             os.makedirs(result_dir)

#         shock_to_file_params = {
#             'shock_id': returnVal.get('shock_id'),
#             'file_path': result_dir,
#             'unpack': 'unpack'}
#         shock_file = self.dfu.shock_to_file(shock_to_file_params)['file_path']
#         df = pd.read_excel(shock_file[:-4], None)

#         return list(df.keys())

#     def test_bad_fetch_data_params(self):
#         self.start_test()
#         invalidate_params = {'missing_obj_ref': 'obj_ref'}
#         error_msg = '"obj_ref" parameter is required, but missing'
#         self.fail_fetch_data(invalidate_params, error_msg)

#     def test_fetch_data(self):
#         self.start_test()
#         params = {'obj_ref': self.expression_matrix_ref}
#         returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
#         self.check_fetch_data_output(returnVal)

#         params = {'obj_ref': self.fitness_matrix_ref}
#         returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
#         self.check_fetch_data_output(returnVal)

#         params = {'obj_ref': self.diff_expr_matrix_ref}
#         returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
#         self.check_fetch_data_output(returnVal)

#         params = {'obj_ref': self.expression_matrix_ref,
#                   'generics_module': {'data': 'FloatMatrix2D'}}
#         returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
#         self.check_fetch_data_output(returnVal)

#     def test_export_matrix(self):
#         self.start_test()
#         params = {'obj_ref': self.expression_matrix_nc_ref}
#         returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
#         sheet_names = self.check_export_matrix_output(returnVal)
#         self.assertCountEqual(sheet_names, ['data', 'metadata'])

#         params = {'obj_ref': self.expression_matrix_ref}
#         returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
#         sheet_names = self.check_export_matrix_output(returnVal)
#         self.assertCountEqual(sheet_names, ['data', 'col_mapping', 'row_mapping', 'metadata'])

#         params = {'obj_ref': self.fitness_matrix_ref}
#         returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
#         sheet_names = self.check_export_matrix_output(returnVal)
#         self.assertCountEqual(sheet_names, ['data', 'row_mapping', 'metadata'])

#         params = {'obj_ref': self.diff_expr_matrix_ref}
#         returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
#         sheet_names = self.check_export_matrix_output(returnVal)
#         self.assertCountEqual(sheet_names, ['data', 'col_mapping', 'metadata'])

#     def test_validate_data(self):
#         self.start_test()

#         # testing unique
#         data = {'data': {'row_ids': ['same_row_id', 'same_row_id'],
#                          'col_ids': ['same_col_id', 'same_col_id']}}
#         obj_type = 'KBaseMatrices.ExpressionMatrix-3.0'

#         params = {'obj_type': obj_type,
#                   'data': data}
#         returnVal = self.getImpl().validate_data(self.ctx, params)[0]
#         self.assertFalse(returnVal.get('validated'))
#         expected_failed_constraints = ['data.row_ids', 'data.col_ids']
#         self.assertCountEqual(expected_failed_constraints,
#                               returnVal.get('failed_constraints').get('unique'))

#         # testing contains
#         data = {'data': {'row_ids': ['same_row_id', 'unknown_row_id'],
#                          'col_ids': ['same_col_id', 'unknown_col_id']},
#                 'row_mapping': {'same_row_id': 'instance_1'},
#                 'col_mapping': {'same_col_id': 'instance_1'},
#                 'row_attributemapping_ref': self.attribute_mapping_ref,
#                 'col_attributemapping_ref': self.attribute_mapping_ref,
#                 'genome_ref': self.genome_ref}
#         obj_type = 'KBaseMatrices.ExpressionMatrix-3.0'
#         params = {'obj_type': obj_type,
#                   'data': data}
#         returnVal = self.getImpl().validate_data(self.ctx, params)[0]
#         self.assertFalse(returnVal.get('validated'))

#         expected_failed_constraints = ['data.row_ids row_mapping',
#                                        'data.col_ids col_mapping',
#                                        'values(row_mapping) row_attributemapping_ref:instances',
#                                        'values(col_mapping) col_attributemapping_ref:instances',
#                                        'data.row_ids genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id']
#         self.assertCountEqual(expected_failed_constraints,
#                               returnVal.get('failed_constraints').get('contains'))

#     def test_import_matrix_from_excel(self):
#         self.start_test()

#         obj_type = 'ExpressionMatrix'
#         params = {'obj_type': obj_type,
#                   'matrix_name': 'test_ExpressionMatrix',
#                   'workspace_name': self.wsName,
#                   'input_file_path': os.path.join('data', 'test_import.xlsx'),
#                   'genome_ref': self.genome_ref,
#                   'scale': 'log2',
#                   }
#         returnVal = self.getImpl().import_matrix_from_excel(self.ctx, params)[0]
#         self.assertTrue('matrix_obj_ref' in returnVal)
#         self.assertTrue('report_name' in returnVal)
#         self.assertTrue('report_ref' in returnVal)

#         obj = self.dfu.get_objects(
#             {'object_refs': [returnVal['matrix_obj_ref']]}
#         )['data'][0]['data']
#         self.assertCountEqual(obj['search_attributes'],
#                               ["Scientist | Marie Currie", "Instrument | Old Faithful"])
#         self.assertEqual(obj['description'], 'test_desc')
#         self.assertEqual(obj['scale'], 'log2')
#         self.assertEqual(obj['col_normalization'], 'test_col_normalization')
#         self.assertEqual(obj['row_normalization'], 'test_row_normalization')

#     def test_import_matrix_from_csv(self):
#         self.start_test()

#         obj_type = 'MetaboliteMatrix'
#         params = {'obj_type': obj_type,
#                   'matrix_name': 'test_MetaboliteMatrix',
#                   'workspace_name': self.wsName,
#                   'input_file_path': os.path.join('data', 'generic_data.csv'),
#                   'scale': 'log2',
#                   'biochemistry_ref': 'kbase/default',
#                   'description': "a biochem matrix",
#                   }
#         returnVal = self.getImpl().import_matrix_from_excel(self.ctx, params)[0]
#         self.assertIn('matrix_obj_ref', returnVal)
#         self.assertIn('report_name', returnVal)
#         self.assertIn('report_ref', returnVal)
#         obj = self.dfu.get_objects(
#             {'object_refs': [returnVal['matrix_obj_ref']]}
#         )['data'][0]['data']
#         self.assertIn('biochemistry_ref', obj)
#         self.assertIn('description', obj)
#         self.assertEqual(obj['description'], 'a biochem matrix')

#     def test_bad_import_matrix_params(self):
#         self.start_test()

#         with self.assertRaisesRegex(ValueError, "parameter is required, but missing"):
#             params = {'obj_type': 'ExpressionMatrix',
#                       'matrix_name': 'test_ExpressionMatrix',
#                       'workspace_name': self.wsName,
#                       'input_file_path': os.path.join('data', 'test_import.xlsx'),
#                       }
#             returnVal = self.getImpl().import_matrix_from_excel(self.ctx, params)[0]

#         with self.assertRaisesRegex(ValueError, "Unknown matrix object type"):
#             params = {'obj_type': 'foo',
#                       'matrix_name': 'test_ExpressionMatrix',
#                       'workspace_name': self.wsName,
#                       'input_file_path': os.path.join('data', 'test_import.xlsx'),
#                       'scale': 'log2'
#                       }
#             returnVal = self.getImpl().import_matrix_from_excel(self.ctx, params)[0]

#         with self.assertRaisesRegex(ValueError, "Unknown scale type"):
#             params = {'obj_type': 'ExpressionMatrix',
#                       'matrix_name': 'test_ExpressionMatrix',
#                       'workspace_name': self.wsName,
#                       'input_file_path': os.path.join('data', 'test_import.xlsx'),
#                       'scale': 'foo'
#                       }
#             returnVal = self.getImpl().import_matrix_from_excel(self.ctx, params)[0]

#         with self.assertRaisesRegex(ValueError, "input_shock_id or input_file_path"):
#             params = {'obj_type': 'ExpressionMatrix',
#                       'matrix_name': 'test_ExpressionMatrix',
#                       'workspace_name': self.wsName,
#                       'scale': 'log2'
#                       }
#             returnVal = self.getImpl().import_matrix_from_excel(self.ctx, params)[0]



#     def test_search_matrix(self):
#         self.start_test()

#         params = {'matrix_obj_ref': self.expression_matrix_ref,
#                   'workspace_name': self.wsName}
#         returnVal = self.getImpl().search_matrix(self.ctx, params)[0]
#         self.assertTrue('report_name' in returnVal)
#         self.assertTrue('report_ref' in returnVal)

#     def test_filter_matrix_rows(self):
#         self.start_test()

#         params = {'matrix_obj_ref': self.expression_matrix_ref,
#                   'workspace_name': self.wsName,
#                   'filter_ids': 'WRI_RS00065_CDS_1,WRI_RS00070_CDS_1',
#                   'filtered_matrix_name': 'filtered_test_matrix_rows'}
#         returnVal = self.getImpl().filter_matrix(self.ctx, params)[0]
#         self.assertTrue('report_name' in returnVal)
#         self.assertTrue('report_ref' in returnVal)
#         self.assertTrue('matrix_obj_refs' in returnVal)

#         matrix_obj_ref = returnVal.get('matrix_obj_refs')[0]
#         matrix_source = self.dfu.get_objects(
#             {"object_refs": [matrix_obj_ref]})['data'][0]
#         matrix_data = matrix_source.get('data')

#         expected_ids = ['WRI_RS00065_CDS_1', 'WRI_RS00070_CDS_1']
#         self.assertCountEqual(matrix_data['data']['row_ids'], expected_ids)
#         self.assertCountEqual(list(matrix_data['row_mapping'].keys()), expected_ids)
#         self.assertCountEqual(list(matrix_data['feature_mapping'].keys()), expected_ids)
#         self.assertEqual(len(matrix_data['data']['values']), len(expected_ids))

#     def test_filter_matrix_cols(self):
#         self.start_test()

#         params = {'matrix_obj_ref': self.expression_matrix_ref,
#                   'workspace_name': self.wsName,
#                   'filter_ids': 'instance 1, instance 3',
#                   'filtered_matrix_name': 'filtered_test_matrix_cols'}
#         returnVal = self.getImpl().filter_matrix(self.ctx, params)[0]
#         self.assertTrue('report_name' in returnVal)
#         self.assertTrue('report_ref' in returnVal)
#         self.assertTrue('matrix_obj_refs' in returnVal)

#         matrix_obj_ref = returnVal.get('matrix_obj_refs')[0]
#         matrix_source = self.dfu.get_objects(
#             {"object_refs": [matrix_obj_ref]})['data'][0]
#         matrix_data = matrix_source.get('data')

#         expected_ids = ['instance_1', 'instance_3']
#         self.assertCountEqual(matrix_data['data']['col_ids'], expected_ids)
#         self.assertCountEqual(list(matrix_data['col_mapping'].keys()), expected_ids)
#         self.assertEqual(len(matrix_data['data']['values'][0]), len(expected_ids))

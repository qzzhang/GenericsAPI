# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests  # noqa: F401
import inspect
import pandas as pd
import shutil


from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from GenericsAPI.GenericsAPIImpl import GenericsAPI
from GenericsAPI.GenericsAPIServer import MethodContext
from GenericsAPI.authclient import KBaseAuth as _KBaseAuth
from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil


class GenericsAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('GenericsAPI'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'GenericsAPI',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = GenericsAPI(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.dfu = DataFileUtil(cls.callback_url)

        suffix = int(time.time() * 1000)
        cls.wsName = "test_kb_ke_apps_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})
        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):

        # upload genome object
        genbank_file_name = 'minimal.gbff'
        genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

        genome_object_name = 'test_Genome'
        cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
                                                    'workspace_name': cls.wsName,
                                                    'genome_name': genome_object_name,
                                                    'generate_ids_if_needed': 1
                                                    })['genome_ref']

        # upload ConditionSet object
        workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        object_type = 'KBaseExperiments.ConditionSet'
        condition_set_object_name = 'test_condition_set'
        condition_set_data = {'conditions': {'test_condition_1': ['1-1', '1-2', '1-3'],
                                             'test_condition_2': ['2-1', '2-2', '2-3'],
                                             'test_condition_3': ['3-1', '3-2', '3-3']},
                              'factors': [{'factor': 'test_factor_1',
                                           'factor_ont_ref': 'factor_ont_ref_1',
                                           'factor_ont_id': 'factor_ont_id_1'},
                                          {'factor': 'test_factor_2',
                                           'factor_ont_ref': 'factor_ont_ref_2',
                                           'factor_ont_id': 'factor_ont_id_2'},
                                          {'factor': 'test_factor_3',
                                           'factor_ont_ref': 'factor_ont_ref_3',
                                           'factor_ont_id': 'factor_ont_id_3'}],
                              'ontology_mapping_method': 'user curation'}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': condition_set_data,
                         'name': condition_set_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.condition_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        cls.col_ids = ['condition_1', 'condition_2', 'condition_3', 'condition_4']
        cls.row_ids = ['WRI_RS00050_CDS_1', 'WRI_RS00065_CDS_1', 'WRI_RS00070_CDS_1']
        cls.values = [[0.1, 0.2, 0.3, 0.4],
                      [0.3, 0.4, 0.5, 0.6],
                      [None, None, None, None]]
        cls.row_mapping = {'WRI_RS00050_CDS_1': 'test_condition_1',
                           'WRI_RS00065_CDS_1': 'test_condition_2',
                           'WRI_RS00070_CDS_1': 'test_condition_3'}
        cls.col_mapping = {'condition_1': 'test_condition_1',
                           'condition_2': 'test_condition_2',
                           'condition_3': 'test_condition_3',
                           'condition_4': 'test_condition_3'}

        # upload ExpressionMatrix object
        object_type = 'KBaseMatrices.ExpressionMatrix'
        expression_matrix_object_name = 'test_expression_matrix'
        expression_matrix_data = {'scale': 'log2',
                                  'type': 'level',
                                  'col_conditionset_ref': cls.condition_set_ref,
                                  'col_mapping': cls.col_mapping,
                                  'row_conditionset_ref': cls.condition_set_ref,
                                  'row_mapping': cls.row_mapping,
                                  'data': {'row_ids': cls.row_ids,
                                           'col_ids': cls.col_ids,
                                           'values': cls.values
                                           },
                                  'genome_ref': cls.genome_ref}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': expression_matrix_data,
                         'name': expression_matrix_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.expression_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        expression_matrix_object_name = 'test_expression_matrix_no_condition'
        expression_matrix_data = {'scale': 'log2',
                                  'type': 'level',
                                  'data': {'row_ids': cls.row_ids,
                                           'col_ids': cls.col_ids,
                                           'values': cls.values
                                           }}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': expression_matrix_data,
                         'name': expression_matrix_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.expression_matrix_nc_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # upload FitnessMatrix object
        object_type = 'KBaseMatrices.FitnessMatrix'
        fitness_matrix_object_name = 'test_fitness_matrix'
        fitness_matrix_data = {'scale': 'log2',
                               'type': 'level',
                               'row_conditionset_ref': cls.condition_set_ref,
                               'row_mapping': cls.row_mapping,
                               'data': {'row_ids': cls.row_ids,
                                        'col_ids': cls.col_ids,
                                        'values': cls.values
                                        }}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': fitness_matrix_data,
                         'name': fitness_matrix_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.fitness_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # upload DifferentialExpressionMatrix object
        object_type = 'KBaseMatrices.DifferentialExpressionMatrix'
        diff_expr_matrix_object_name = 'test_diff_expr_matrix'
        diff_expr_matrix_data = {'scale': 'log2',
                                 'type': 'level',
                                 'col_conditionset_ref': cls.condition_set_ref,
                                 'col_mapping': cls.col_mapping,
                                 'data': {'row_ids': cls.row_ids,
                                          'col_ids': cls.col_ids,
                                          'values': cls.values
                                          }}
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': diff_expr_matrix_data,
                         'name': diff_expr_matrix_object_name}]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.diff_expr_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    def fail_fetch_data(self, params, error, exception=ValueError,
                        contains=False):
        with self.assertRaises(exception) as context:
            self.getImpl().fetch_data(self.ctx, params)
        if contains:
            self.assertIn(error, str(context.exception.message))
        else:
            self.assertEqual(error, str(context.exception.message))

    def check_fetch_data_output(self, returnVal):
        self.assertTrue('data_matrix' in returnVal)
        data_matrix = json.loads(returnVal.get('data_matrix'))

        col_ids = data_matrix.keys()
        self.assertItemsEqual(col_ids, self.col_ids)
        for col_id in col_ids:
            self.assertItemsEqual(data_matrix.get(col_id).keys(), self.row_ids)

    def check_export_matrix_output(self, returnVal):
        self.assertTrue('shock_id' in returnVal)

        result_dir = os.path.join(self.scratch, 'export_matrix_result')
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        shock_to_file_params = {
            'shock_id': returnVal.get('shock_id'),
            'file_path': result_dir,
            'unpack': 'unpack'}
        shock_file = self.dfu.shock_to_file(shock_to_file_params)['file_path']
        df = pd.read_excel(shock_file[:-4], None)

        return df.keys()

    def test_bad_fetch_data_params(self):
        self.start_test()
        invalidate_params = {'missing_obj_ref': 'obj_ref'}
        error_msg = '"obj_ref" parameter is required, but missing'
        self.fail_fetch_data(invalidate_params, error_msg)

    def test_generate_matrix_html(self):
        self.start_test()

        csv_file_name = 'metadata.csv'
        df = pd.read_csv(os.path.join('data', csv_file_name))

        returnVal = self.getImpl().generate_matrix_html(self.ctx, {'df': df})[0]

        self.assertTrue('html_string' in returnVal)
        self.assertTrue('ADD_COL' not in returnVal.get('html_string'))
        self.assertTrue('ADD_DATA' not in returnVal.get('html_string'))
        self.assertTrue('ADD_FORMATTER' not in returnVal.get('html_string'))

    def test_fetch_data(self):
        self.start_test()
        params = {'obj_ref': self.expression_matrix_ref}
        returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
        print returnVal
        self.check_fetch_data_output(returnVal)

        params = {'obj_ref': self.fitness_matrix_ref}
        returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
        self.check_fetch_data_output(returnVal)

        params = {'obj_ref': self.diff_expr_matrix_ref}
        returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
        self.check_fetch_data_output(returnVal)

        params = {'obj_ref': self.expression_matrix_ref,
                  'generics_module': {'data': 'FloatMatrix2D'}}
        returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
        self.check_fetch_data_output(returnVal)

    def test_export_matrix(self):
        self.start_test()
        params = {'obj_ref': self.expression_matrix_nc_ref}
        returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
        sheet_names = self.check_export_matrix_output(returnVal)
        self.assertItemsEqual(sheet_names, ['data', 'metadata'])

        params = {'obj_ref': self.expression_matrix_ref}
        returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
        sheet_names = self.check_export_matrix_output(returnVal)
        self.assertItemsEqual(sheet_names, ['data', 'col_mapping', 'row_mapping', 'metadata'])

        params = {'obj_ref': self.fitness_matrix_ref}
        returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
        sheet_names = self.check_export_matrix_output(returnVal)
        self.assertItemsEqual(sheet_names, ['data', 'row_mapping', 'metadata'])

        params = {'obj_ref': self.diff_expr_matrix_ref}
        returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
        sheet_names = self.check_export_matrix_output(returnVal)
        self.assertItemsEqual(sheet_names, ['data', 'col_mapping', 'metadata'])

    def test_validate_data(self):
        self.start_test()

        # testing unique
        data = {'data': {'row_ids': ['same_row_id', 'same_row_id'],
                         'col_ids': ['same_col_id', 'same_col_id']}}
        obj_type = 'KBaseMatrices.ExpressionMatrix-1.1'

        params = {'obj_type': obj_type,
                  'data': data}
        returnVal = self.getImpl().validate_data(self.ctx, params)[0]
        self.assertFalse(returnVal.get('validated'))
        expected_failed_constraints = ['data.row_ids', 'data.col_ids']
        self.assertItemsEqual(expected_failed_constraints,
                              returnVal.get('failed_constraints').get('unique'))

        # testing contains
        data = {'data': {'row_ids': ['same_row_id', 'unknown_row_id'],
                         'col_ids': ['same_col_id', 'unknown_col_id']},
                'row_mapping': {'same_row_id': 'condition_1'},
                'col_mapping': {'same_col_id': 'condition_1'},
                'row_conditionset_ref': self.condition_set_ref,
                'col_conditionset_ref': self.condition_set_ref,
                'genome_ref': self.genome_ref}
        obj_type = 'KBaseMatrices.ExpressionMatrix-1.1'
        params = {'obj_type': obj_type,
                  'data': data}
        returnVal = self.getImpl().validate_data(self.ctx, params)[0]
        self.assertFalse(returnVal.get('validated'))
        expected_failed_constraints = ['data.row_ids row_mapping',
                                       'data.col_ids col_mapping',
                                       'values(row_mapping) row_conditionset_ref:conditions',
                                       'values(col_mapping) col_conditionset_ref:conditions',
                                       'data.row_ids genome_ref:features.[*].id genome_ref:mrnas.[*].id genome_ref:cdss.[*].id genome_ref:non_codeing_features.[*].id']
        self.assertItemsEqual(expected_failed_constraints,
                              returnVal.get('failed_constraints').get('contains'))

    def test_import_matrix_from_excel(self):
        self.start_test()

        obj_type = 'ExpressionMatrix'
        params = {'obj_type': obj_type,
                  'matrix_name': 'test_ExpressionMatrix',
                  'workspace_name': self.wsName,
                  'input_file_path': os.path.join('data', 'test_import.xlsx'),
                  'genome_ref': self.genome_ref}
        returnVal = self.getImpl().import_matrix_from_excel(self.ctx, params)[0]
        self.assertTrue('matrix_obj_ref' in returnVal)
        self.assertTrue('report_name' in returnVal)
        self.assertTrue('report_ref' in returnVal)
        print returnVal

    def test_search_matrix(self):
        self.start_test()

        params = {'matrix_obj_ref': self.expression_matrix_ref,
                  'workspace_name': self.wsName}
        returnVal = self.getImpl().search_matrix(self.ctx, params)[0]
        self.assertTrue('report_name' in returnVal)
        self.assertTrue('report_ref' in returnVal)

    def test_filter_matrix(self):
        self.start_test()

        params = {'matrix_obj_ref': self.expression_matrix_ref,
                  'workspace_name': self.wsName,
                  'feature_ids': 'WRI_RS00065_CDS_1,WRI_RS00070_CDS_1',
                  'filtered_matrix_name': 'filtered_test_matrix'}
        returnVal = self.getImpl().filter_matrix(self.ctx, params)[0]
        self.assertTrue('report_name' in returnVal)
        self.assertTrue('report_ref' in returnVal)
        self.assertTrue('matrix_obj_refs' in returnVal)

        matrix_obj_ref = returnVal.get('matrix_obj_refs')[0]
        matrix_source = self.dfu.get_objects(
            {"object_refs": [matrix_obj_ref]})['data'][0]
        matrix_data = matrix_source.get('data')

        feature_ids = matrix_data['data']['row_ids']
        self.assertItemsEqual(feature_ids, ['WRI_RS00065_CDS_1', 'WRI_RS00070_CDS_1'])

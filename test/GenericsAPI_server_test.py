# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests  # noqa: F401
import inspect
import pandas as pd


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
        cls.col_ids = ['condition_1', 'condition_2', 'condition_3', 'condition_4']
        cls.row_ids = ['gene_1', 'gene_2', 'gene_3']
        cls.values = [[0.1, 0.2, 0.3, 0.4],
                      [0.3, 0.4, 0.5, 0.6],
                      [None, None, None, None]]

        # upload ExpressionMatrix object
        workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        object_type = 'KBaseFeatureValues.ExpressionMatrix'
        expression_matrix_object_name = 'test_expression_matrix'
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
        cls.expression_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # upload SingleKnockoutFitnessMatrix object
        workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        object_type = 'KBaseFeatureValues.SingleKnockoutFitnessMatrix'
        fitness_matrix_object_name = 'test_fitness_matrix'
        fitness_matrix_data = {'scale': 'log2',
                               'type': 'level',
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
        workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        object_type = 'KBaseFeatureValues.DifferentialExpressionMatrix'
        diff_expr_matrix_object_name = 'test_fitness_matrix'
        diff_expr_matrix_data = {'scale': 'log2',
                                 'type': 'level',
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
        os.makedirs(result_dir)

        shock_to_file_params = {
            'shock_id': returnVal.get('shock_id'),
            'file_path': result_dir}
        shock_file = self.dfu.shock_to_file(shock_to_file_params)['file_path']
        df = pd.read_excel(shock_file)
        self.assertItemsEqual(df.columns.tolist(), self.col_ids)
        self.assertItemsEqual(df.index.tolist(), self.row_ids)

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
                  'generics_module': {'FloatMatrix2D': 'data'}}
        returnVal = self.getImpl().fetch_data(self.ctx, params)[0]
        self.check_fetch_data_output(returnVal)

    def test_export_matrix(self):
        self.start_test()
        params = {'obj_ref': self.expression_matrix_ref}
        returnVal = self.getImpl().export_matrix(self.ctx, params)[0]
        self.check_export_matrix_output(returnVal)

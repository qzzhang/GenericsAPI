# -*- coding: utf-8 -*-
import inspect
import json  # noqa: F401
import os  # noqa: F401
import unittest
import time
import shutil

import pandas as pd
import numpy as np

try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from GenericsAPI.Utils.CorrelationUtil import CorrelationUtil
from GenericsAPI.GenericsAPIImpl import GenericsAPI
from GenericsAPI.GenericsAPIServer import MethodContext
from GenericsAPI.authclient import KBaseAuth as _KBaseAuth
from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as workspaceService


class GenericsAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
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
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.corr_util = CorrelationUtil(cls.cfg)

        suffix = int(time.time() * 1000)
        cls.wsName = "test_corr_util_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def getCorrUtil(self):
        return self.__class__.corr_util

    def loadDF(self):

        if hasattr(self.__class__, 'test_random_df'):
            return self.__class__.test_random_df

        # Build test DF
        index = ['idx_{}'.format(idx) for idx in range(0, 6)]
        columns = ['col_{}'.format(idx) for idx in range(0, 10)]

        np.random.seed(0)
        test_random_df = pd.DataFrame(np.random.uniform(low=0, high=100,
                                                        size=(len(index), len(columns))),
                                      index=index, columns=columns)

        self.__class__.test_random_df = test_random_df
        print('Created Random DF:\n' + test_random_df.to_string())
        return test_random_df

    def loadExpressionMatrix(self):
        if hasattr(self.__class__, 'expr_matrix_ref'):
            return self.__class__.expr_matrix_ref

        matrix_file_name = 'test_import.xlsx'
        matrix_file_path = os.path.join(self.scratch, matrix_file_name)
        shutil.copy(os.path.join('data', matrix_file_name), matrix_file_path)

        obj_type = 'ExpressionMatrix'
        params = {'obj_type': obj_type,
                  'matrix_name': 'test_ExpressionMatrix',
                  'workspace_name': self.wsName,
                  'input_file_path': matrix_file_path,
                  'scale': "log2",
                  }
        expr_matrix_ref = self.serviceImpl.import_matrix_from_excel(
            self.ctx, params)[0].get('matrix_obj_ref')

        self.__class__.expr_matrix_ref = expr_matrix_ref
        print('Loaded ExpressionMatrix: ' + expr_matrix_ref)
        return expr_matrix_ref

    def fail_df_to_corr(self, df, error, method='pearson', dimension='col',
                        exception=ValueError, contains=False):
        with self.assertRaises(exception) as context:
            self.getCorrUtil().df_to_corr(df, method=method, dimension=dimension)
        if contains:
            self.assertIn(error, str(context.exception.message))
        else:
            self.assertEqual(error, str(context.exception.message))

    def fail_plot_scatter_matrix(self, df, error, alpha=0.2, dimension='col',
                                 exception=ValueError, contains=False):
        with self.assertRaises(exception) as context:
            self.getCorrUtil().plot_scatter_matrix(df, alpha=alpha, dimension=dimension)
        if contains:
            self.assertIn(error, str(context.exception.message))
        else:
            self.assertEqual(error, str(context.exception.message))

    def fail_compute_correlation_matrix(self, params, error, exception=ValueError,
                                        contains=False):
        with self.assertRaises(exception) as context:
            self.getImpl().compute_correlation_matrix(self.ctx, params)
        if contains:
            self.assertIn(error, str(context.exception.message))
        else:
            self.assertEqual(error, str(context.exception.message))

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    def test_compute_correlation_matrix_fail(self):
        self.start_test()

        invalidate_params = {'missing_input_obj_ref': 'input_obj_ref',
                             'workspace_name': 'workspace_name'}
        error_msg = '"input_obj_ref" parameter is required, but missing'
        self.fail_compute_correlation_matrix(invalidate_params, error_msg)

        invalidate_params = {'input_obj_ref': 'input_obj_ref',
                             'missing_workspace_name': 'workspace_name'}
        error_msg = '"workspace_name" parameter is required, but missing'
        self.fail_compute_correlation_matrix(invalidate_params, error_msg)

    def test_comp_corr_matrix_ok(self):
        self.start_test()
        expr_matrix_ref = self.loadExpressionMatrix()

        params = {'input_obj_ref': expr_matrix_ref,
                  'workspace_name': self.wsName,
                  'corr_matrix_name': 'test_corr_matrix',
                  'plot_corr_matrix': True,
                  'plot_scatter_matrix': True,
                  'compute_significance': True}

        ret = self.getImpl().compute_correlation_matrix(self.ctx, params)[0]

        self.assertIn('corr_matrix_obj_ref', ret)
        corr_matrix_obj_ref = ret.get('corr_matrix_obj_ref')

        res = self.dfu.get_objects({'object_refs': [corr_matrix_obj_ref]})['data'][0]
        obj_data = res['data']

        self.assertEqual(obj_data.get('correlation_parameters').get('method'), 'pearson')

        corr_items = ['WRI_RS00010_CDS_1', 'WRI_RS00015_CDS_1', 'WRI_RS00025_CDS_1']
        self.assertItemsEqual(obj_data.get('coefficient_data').get('row_ids'), corr_items)
        self.assertItemsEqual(obj_data.get('coefficient_data').get('col_ids'), corr_items)

        self.assertItemsEqual(obj_data.get('significance_data').get('row_ids'), corr_items)
        self.assertItemsEqual(obj_data.get('significance_data').get('col_ids'), corr_items)

    def test_init_ok(self):
        self.start_test()
        class_attri = ['scratch', 'token', 'callback_url', 'ws_url']

        corr_util = self.getCorrUtil()
        self.assertTrue(set(class_attri) <= set(corr_util.__dict__.keys()))
        self.assertEqual(corr_util.scratch, self.cfg.get('scratch'))

    def test_df_to_corr_fail(self):
        self.start_test()
        df = self.loadDF()

        # unavailable correlation method
        self.fail_df_to_corr(df, 'Input correlation method', method='fake_method', contains=True)

        # unavailable dimension
        self.fail_df_to_corr(df, 'Input dimension', dimension='fake_dimension', contains=True)

    def test_df_to_corr_ok(self):
        self.start_test()
        df = self.loadDF()

        # test default
        corr_df = self.getCorrUtil().df_to_corr(df)
        self.assertItemsEqual(corr_df.index.tolist(), corr_df.columns.tolist())
        self.assertItemsEqual(corr_df.index.tolist(), df.columns.tolist())

        # test correlation on rows
        corr_df = self.getCorrUtil().df_to_corr(df, dimension='row')
        self.assertItemsEqual(corr_df.index.tolist(), corr_df.columns.tolist())
        self.assertItemsEqual(corr_df.index.tolist(), df.index.tolist())

    def test_plot_scatter_matrix_fail(self):
        self.start_test()
        df = self.loadDF()

        # unavailable dimension
        self.fail_plot_scatter_matrix(df, 'Input dimension', dimension='fake_dim', contains=True)

        # fail pd.plotting.scatter_matrix
        self.fail_plot_scatter_matrix(df, 'Running scatter_matrix returned an error', alpha=10, contains=True)

    def test_plot_scatter_matrix_ok(self):
        self.start_test()
        df = self.loadDF()

        # default
        scatter_plot_path = self.getCorrUtil().plot_scatter_matrix(df)
        self.assertTrue(os.path.isfile(scatter_plot_path))
        self.assertGreater(os.path.getsize(scatter_plot_path), 1024)  # file size greate than 1KB

        # scatter plot on rows
        scatter_plot_path = self.getCorrUtil().plot_scatter_matrix(df, dimension='row')
        self.assertTrue(os.path.isfile(scatter_plot_path))
        self.assertGreater(os.path.getsize(scatter_plot_path), 1024)  # file size greate than 1KB

    def test_plot_corr_matrix_ok(self):
        self.start_test()
        df = self.loadDF()
        corr_df = self.getCorrUtil().df_to_corr(df, dimension='col')

        # default
        corr_matrix_plot_path = self.getCorrUtil().plot_corr_matrix(corr_df)
        self.assertTrue(os.path.isfile(corr_matrix_plot_path))
        self.assertGreater(os.path.getsize(corr_matrix_plot_path), 1024)  # file size greate than 1KB
